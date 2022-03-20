from scipy.io import wavfile
from .quantif import quantif

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    import plotly.express as px

    use_plotly = False
except Exception as e:

    use_plotly = False


def plot_histo(df: pd.DataFrame, title: str = "Histo", nbins: int = None):
    if use_plotly:
        fig = px.histogram(df, title=title, nbins=nbins)
        fig.show()
        return fig
    else:
        fig = plt.hist(df.values, bins=nbins)
        plt.title(title)
        plt.show()
        return fig


def plot_signal(df: pd.DataFrame, plot_range=300):
    data = df.iloc[:plot_range]
    if use_plotly:
        return data.plot().show()
    else:
        fig = data.plot()
        plt.show()
        return fig


class QuantifierComparator:
    bruit_nom = "Bruit"
    norm_nom = "Normalized"

    def __init__(self, file_path):
        # Chargement du signal
        self.sp_rate, self.base_data = wavfile.read(file_path)
        # sp_rate corresponds a la frequence d'echantillonnage
        # et base_data au signal
        self.data = self.normalised_data = self.base_data / (2 ** 15)
        # On normalise le signal

        self.df = pd.DataFrame()
        self.df[self.norm_nom] = self.data
        self.quant_data = None
        self.quant_step = None
        self.quantized_value = None
        self.f = None
        self.n = 8
        self.a = 1
        self.rsb = None
        self.var_signal = None
        self.var_noice = None

    def quantify(self, n=8, a=1):
        self.n = n
        self.a = a
        [self.quant_data, self.quant_step, self.quantized_value] = quantif(self.normalised_data, a, n)
        return self.quant_data

    def pack_in_df(self):
        """
        Ajoute les nouvelles données dans le dataframe
        """
        self.df[self.norm_nom] = self.data
        if self.quant_data is None:
            print("WARNING : data has not been quantified, using base parameters")
            self.quantify()
        self.df[f"Quantified_n{self.n,}_a{self.a}"] = self.quant_data
        self.df[self.bruit_nom] = self.df[f"Quantified_n{self.n,}_a{self.a}"] - self.df[self.norm_nom]

    def reset_dataframe(self):
        self.df = pd.DataFrame()

    def plot(self, plot_range=300):
        fig = plot_signal(self.df.iloc[:plot_range], plot_range)

    def plot_histo(self, name=None,nbins=20):
        if self.df.empty:
            print("empty dataframe, pack pls")
            return
        if name is not None and name in self.df.columns:
            fig = plot_histo(self.df[name], title=name,nbins=nbins)
        else:
            for _i in self.df.columns:
                fig = plot_histo(self.df[_i], title=_i,nbins=nbins)

    def calc_rsb(self):
        if self.var_signal is None or self.var_noice is None:
            self.calc_metrics()
        self.rsb = self.var_signal / self.var_noice

    def calc_f(self):
        if self.rsb is None:
            self.calc_rsb()
        self.f = self.a / np.sqrt(self.var_signal)

    def calc_metrics(self):
        if self.bruit_nom not in self.df.columns:
            print(self.df)
            self.pack_in_df()
            print("auto_packing")
        self.var_noice = self.df[self.bruit_nom].var()
        self.var_signal = self.df[self.norm_nom].var()
