from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import specgram
from os import path
from pydub import AudioSegment

class Model:
    def __init__(self, audio):
        self.audio = audio
        self.low = 250
        self.mid = 1000
        self.high = 5000

    @property
    def audio(self):
        return self.__audio

    @audio.setter
    def audio(self, value):
        self.__audio = value

    def convert_file(self, file):
        src = file
        dest = "clap.wav"
        clap = AudioSegment.from_file(src, format="m4a")
        clap.export(dest, format="wav")
        wav_clap_audio = AudioSegment.from_file("clap.wav", format="wav")
        return wav_clap_audio

    def clean_file(self):
      raw_clap = AudioSegment.from_file("clap.wav", format="wav")
      mono_clap = raw_clap.set_channels(1)
      mono_clap.export("clap_mono.wav", format="wav")
      mono_clap_audio = AudioSegment.from_file("clap_mono.wav", format="wav")
      c_count = mono_clap_audio.channels
      return mono_clap_audio

    def data(self, mono_file):
        data = np.array(mono_file.get_array_of_samples())
        samplerate = mono_file.frame_rate
        spectrum, freqs, t = specgram(data, Fs=samplerate, NFFT=1024)
        return samplerate, data, spectrum, freqs, t

    def length_and_max_freq(self, mono_file):
        samp_rate, d, spectrum, freqs, t = self.data(mono_file)
        length = d.shape[0] / samp_rate
        max_intensity_index, max_frequency_index = np.unravel_index(np.argmax(spectrum, axis=None), spectrum.shape)
        max_frequency = freqs[max_frequency_index]
        return length, max_frequency


    def spectrum(self, mono_file):
        f = mono_file
        samp_rate, d, spectrum, freqs, t = self.data(f)
        spectrum, freqs, t, im = plt.specgram(d, Fs=samp_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar = plt.colorbar(im)
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        cbar.set_label('Intensity (dB)')
        plt.show()

    def waveform(self, mono_file):
        samp_rate, d, spectrum, freqs, t = self.data(mono_file)
        plt.hist(d, bins=1000, color='purple')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')

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

    def rt60plot(self, freq, mono_file):
        file = mono_file
        # plt.figure()
        frequency = freq
        data_db, rt_60, iom, iom_5, iom_25 = self.rt60_vals(frequency, file)
        samp_rate, d, spectrum, freqs, t = self.data(file)
        """
        You can call the rt60_vals function 3 times from within the model class using
        the diff frequencies and gather the rt60 values then pass it to the view that way
        """
        # print(f'The RT60 reverb time for {frequency} Hz is {(round(abs(rt_60), 2))} seconds')
        plt.plot(t, data_db, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')
        plt.plot(t[iom], data_db[iom], 'go')
        plt.plot(t[iom_5], data_db[iom_5], 'yo')
        plt.plot(t[iom_25], data_db[iom_25], 'ro')
        plt.grid()
        plt.show()

    def combine(self, mono_file):
        file = mono_file
        samp_rate, d, spectrum, freqs, t = self.data(file)

        low_data = self.frequency_check(self.low, file)
        mid_data = self.frequency_check(self.mid, file)
        high_data = self.frequency_check(self.high, file)

        data_db_l, rt_60_l, iom_l, iom_5_l, iom_25_l = self.rt60_vals(self.low, mono_file)
        data_db_m, rt_60_m, iom_m, iom_5_m, iom_25_m = self.rt60_vals(self.mid, mono_file)
        data_db_h, rt_60_h, iom_h, iom_5_h, iom_25_h = self.rt60_vals(self.high, mono_file)

        plt.figure(figsize=(12, 8))

        plt.plot(t, low_data, label=f'Low Frequency ({self.low} Hz)', linewidth=1, alpha=0.7, color='red')
        plt.plot(t, mid_data, label=f'Mid Frequency ({self.mid} Hz)', linewidth=1, alpha=0.7, color='green')
        plt.plot(t, high_data, label=f'High Frequency ({self.high} Hz)', linewidth=1, alpha=0.7, color='blue')

        plt.plot(t[iom_l], low_data[iom_l], 'go')
        plt.plot(t[iom_5_l], low_data[iom_5_l], 'yo')
        plt.plot(t[iom_25_l], low_data[iom_25_l], 'ro')

        plt.plot(t[iom_m], mid_data[iom_m], 'go')
        plt.plot(t[iom_5_m], mid_data[iom_5_m], 'yo')
        plt.plot(t[iom_25_m], mid_data[iom_25_m], 'ro')

        plt.plot(t[iom_h], high_data[iom_h], 'go')
        plt.plot(t[iom_5_h], high_data[iom_5_h], 'yo')
        plt.plot(t[iom_25_h], high_data[iom_25_h], 'ro')

        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')
        plt.title('Combined RT60 Plot')
        plt.legend()
        plt.grid()
        plt.show()