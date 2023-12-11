import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import specgram
from pydub import AudioSegment


class Model:
    def __init__(self):
        self.low = 250
        self.mid = 1000
        self.high = 5000

    def convert_file(self, file):
        src = file
        dest = "audio.wav"
        clap = AudioSegment.from_file(src, format="m4a")
        clap.export(dest, format="wav")

    def clean_file(self):
        raw_clap = AudioSegment.from_file("audio.wav", format="wav")
        mono_clap = raw_clap.set_channels(1)
        mono_clap.export("audio_mono.wav", format="wav")
        mono_clap_audio = AudioSegment.from_file("audio_mono.wav", format="wav")
        return mono_clap_audio

    def data(self, mono_file):
        data = np.array(mono_file.get_array_of_samples())
        samplerate = mono_file.frame_rate
        spectrum, freqs, t = specgram(data, Fs=samplerate, NFFT=1024)
        return samplerate, data, spectrum, freqs, t

    def length_and_max_freq(self, mono_file):
        samp_rate, d, spectrum, freqs, t = self.data(mono_file)
        length = round(d.shape[0] / samp_rate, 2)
        max_intensity_index, max_frequency_index = np.unravel_index(np.argmax(spectrum, axis=None), spectrum.shape)
        max_frequency = max_frequency_index
        return length, max_frequency

    def find_target_freq(self, freqs, freq_range):
        for x in freqs:
            if x > freq_range:
                break
        return x

    def debugg(self, fstring):
        print(fstring)

    def frequency_check(self, freq_range, mono_file):
        file = mono_file
        samp_rate, d, spectrum, freqs, t = self.data(file)
        self.debugg(f'freqs {freqs[:10]}')
        target_frequency = self.find_target_freq(freqs, freq_range)
        self.debugg(f'target_frequency {target_frequency}')
        index_of_freq = np.where(freqs == target_frequency)[0][0]
        self.debugg(f'index_of_frequency {index_of_freq}')

        data_for_freq = spectrum[index_of_freq]
        self.debugg(f'data_for_frequency {data_for_freq[:10]}')

        data_in_db_fun = 10 * np.log10(data_for_freq)
        return data_in_db_fun

    def find_nearest_val(self, array, value):
        array = np.asarray(array)
        self.debugg(f'array {array[:10]}')
        idx = (np.abs(array - value)).argmin()
        self.debugg(f'idx {idx}')
        self.debugg(f'array[idx] {array[idx]}')
        return array[idx]

    def rt60_vals(self, freq_range, mono_file):
        file = mono_file
        samp_rate, d, spectrum, freqs, t = self.data(file)
        rng = freq_range
        data_in_db = self.frequency_check(rng, file)
        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        sliced_array = data_in_db[index_of_max:]
        value_of_max_minus_5 = value_of_max - 5
        value_of_max_minus_5 = self.find_nearest_val(sliced_array, value_of_max_minus_5)
        index_of_max_minus_5 = np.where(data_in_db == value_of_max_minus_5)
        value_of_max_minus_25 = value_of_max - 25
        value_of_max_minus_25 = self.find_nearest_val(sliced_array, value_of_max_minus_25)
        index_of_max_minus_25 = np.where(data_in_db == value_of_max_minus_25)
        rt20 = (t[index_of_max_minus_5] - t[index_of_max_minus_25])[0]
        rt60 = 3 * rt20
        return data_in_db, rt60, index_of_max, index_of_max_minus_5, index_of_max_minus_25

    def rt60diff(self, mono_file):
        dl, rt60_l, ioml, iom_5l, iom_25l = self.rt60_vals(self.low, mono_file)
        dm, rt60_m, iomm, iom_5m, iom_25m = self.rt60_vals(self.mid, mono_file)
        dh, rt60_h, iomh, iom_5h, iom_25h = self.rt60_vals(self.high, mono_file)

        rt60_avg_p5 = ((rt60_l + rt60_m + rt60_h) / 3) - 0.5
        rt60difference = (round(abs(rt60_avg_p5), 2))
        return rt60difference

    def rt60plot(self, freq, mono_file):
        file = mono_file
        # plt.figure()
        frequency = freq
        data_db, rt_60, iom, iom_5, iom_25 = self.rt60_vals(frequency, file)
        samp_rate, d, spectrum, freqs, t = self.data(file)
        plt.plot(t, data_db, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')
        plt.plot(t[iom], data_db[iom], 'go')
        plt.plot(t[iom_5], data_db[iom_5], 'yo')
        plt.plot(t[iom_25], data_db[iom_25], 'ro')
        plt.grid()
        plt.show()
