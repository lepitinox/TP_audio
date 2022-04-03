import copy

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


class ITFCT:
    def __init__(self, signal, nhop, nfft, freq):
        self.xmat = signal
        self.nhop = nhop
        self.nfft = nfft
        self.freq = freq
        self.y_len = self.calc_vector_length()
        self.y = [0] * self.y_len
        self.df_y = self.build_base_trames()
        self.offset_trams()

    def calc_vector_length(self):
        """
        On considérant que Nfft = Nwin, on peut déterminé la longeur du signal de base
        comme étant le nombre de trames mulitplié par la longeur d'une trame moins le chevauchement entre deux trames
        (ou la plus la distance si Nhop > Nwin)
        """
        nb_trams = len(self.xmat)
        tram_len = self.nfft
        tram_step = self.nhop

        return nb_trams * (tram_len - (tram_len - tram_step)) * 2

    def build_base_trames(self):
        """
        on construit un Dataframe avec toutes les demi trames (n trames)
        """
        tmp = pd.DataFrame(self.xmat)
        values = pd.concat([tmp, tmp.iloc[:, 1:-1]], axis=1)

        basedf = pd.DataFrame(index=list(range(len(self.xmat))), columns=list(range(len(self.y))))
        basedf.iloc[values.index, values.columns] = values
        b = basedf.T
        b = b.apply(lambda x: x.shift(int(x.name) * self.nhop))
        b = b.fillna(0)
        b.T.abs().sum().plot()
        plt.show()

    def offset_trams(self):
        """
        On va offset les trams de nhop * n (avec n l'index de la tram)
        """

    def add_suff(self):
        return self.df_y_decal.sum(axis=1)

    def normalisation(self):
        k = sum(np.hamming(self.nfft) / self.nhop)
        return self.df_y / k


if __name__ == '__main__':
    xmat = np.load("files\\xmat.npy")
    nhop = 128
    nfft = 668
    freq = 16000
    a = ITFCT(xmat, nhop, nfft, freq)
