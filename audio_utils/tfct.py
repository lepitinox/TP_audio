from scipy.io import wavfile
import pandas as pd
import numpy as np
import sounddevice as sd
import plotly.express as px


class TFCT:
    n_win = 1024
    n_hop = 512
    n_fft = n_win
    window_type = "hamming"

    def __init__(self, file_path):
        self.x_mat = None
        self.windowed_trames_specter = []
        self.trames_specter = []
        self.trames = None
        self.windowed_trames = None
        self.freq, self.x_vect = wavfile.read(file_path)
        if len(self.x_vect.shape) != 1:
            self.x_vect = self.x_vect[:, 0]
        self.df_x_vect = pd.DataFrame(self.x_vect, columns=["Base signal"])
        print(f"signal with : {len(self.x_vect)}")

    def run(self):
        self.cut_signal()
        self.apply_fft_on_window()
        self.apply_fft_on_trames()
        self.build_xmat()

    def generate_window(self, len_window=None):
        if len_window is None:
            len_window = self.n_win
        if self.window_type.lower() == "hamming":
            return np.hamming(len_window)

    def cut_one_tram(self, start_point):
        ret = []
        if start_point + self.n_win <= len(self.x_vect):
            for i in range(self.n_win):
                ret.append(self.x_vect[start_point + i])
            return ret
        else:
            print("Warning: last window will be cut")
            for i in range(start_point, len(self.x_vect)):
                ret.append(self.x_vect[start_point + i])
            return ret

    def apply_window(self, trame):
        ret = []
        window = self.generate_window(len(trame))
        for i in range(len(trame)):
            ret.append(trame[i] * window[i])
        return ret

    def apply_fft_on_trames(self):
        self.trames_specter = []
        for i in self.trames:
            self.trames_specter.append(self._apply_fft(i))

    def apply_fft_on_window(self):
        self.windowed_trames_specter = []
        for i in self.windowed_trames:
            self.windowed_trames_specter.append(self._apply_fft(i))

    def _apply_fft(self, signal):
        data = np.fft.fft(signal, n=int(self.n_fft))
        axis = np.fft.fftfreq(int(self.n_fft), 1 / self.freq)
        return data, axis

    def build_xmat(self):
        temp = []
        spec_len = len(self.windowed_trames_specter[0][0])
        if spec_len % 2:
            for i in range(len(self.windowed_trames_specter)):
                temp.append(abs(self.windowed_trames_specter[i][0][:spec_len // 2 + 1]))
        else:
            for i in range(len(self.windowed_trames_specter)):
                try:
                    temp.append(abs(self.windowed_trames_specter[i][0][:int(spec_len / 2)]))
                except Exception as e:

                    print(spec_len)
                    print(e)
                    exit()
        print(f" nb Trames in xmat : {len(self.windowed_trames_specter)}")
        self.x_mat = pd.DataFrame(temp)
        self.x_mat.columns.name = "Frequency"
        self.x_mat.columns = self.x_mat.columns.map(lambda x: x * self.freq/1000)
        self.x_mat.index.name = "Trames"
        return temp

    def plot_specter(self):

        fig = px.imshow(self.x_mat, aspect=self.x_mat.columns[-1] / self.x_mat.index[-1])
        fig.show()

    def cut_signal(self):
        self.trames = []
        self.windowed_trames = []
        for i in range(0, len(self.x_vect) - self.n_win, self.n_hop):
            tmp_tram = self.cut_one_tram(i)
            self.trames.append(tmp_tram)
            self.windowed_trames.append(self.apply_window(tmp_tram))

    def change_params(self, n_win=None, n_hop=None, n_fft=None):
        if n_win is not None:
            self.n_win = n_win
        if n_hop is not None:
            self.n_hop = n_hop
        if n_fft is not None:
            self.n_fft = n_fft

    def plot_signal(self, plot_range=None):
        if plot_range is None:
            data = self.df_x_vect
        else:
            data = self.df_x_vect.iloc[:plot_range]
        data.plot().show()

    def plot_trames(self):
        df = pd.DataFrame(self.trames)
        for i in range(len(self.trames)):
            df[f"{i}"] = self.trames[i]
        df.plot().show()

    def play_sound(self, nb_point=None):
        if nb_point is None:
            sd.play(self.x_vect, self.freq)
        else:
            sd.play(self.x_vect[:nb_point], self.freq)
