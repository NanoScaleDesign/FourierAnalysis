#!/usr/bin/env python3
import sounddevice as sd
import numpy as np
import plotly
import plotly.graph_objs as go
from scipy.io import wavfile

def main():
    fs = 44100

    # Record or load audio
    #rec = record(fs=fs, duration=20) # <- Not required unless you want to record audio
    rec = load_audio('bbcnews181210.noisy.wav') # Load audio

    # Play back and plot magnitude graph
    playback(rec.real,fs)
    mag = calc_mag(rec) # Edit this function
    plotgraph(rec=mag,fs=fs,fname='audio_output.html',title='Original audio output',xtitle='Time (s)',ytitle='Amplitude')

    #return # You can use this to stop the program here until you're ready to move on.
    
    # Calculate FFT and display frequency graph
    fft = calc_fft(rec) # Edit this function
    mag = calc_mag(fft)
    plotgraph(rec=mag,fs=1,fname='fft.html',title='Noisy signal spectrum',xtitle='Frequency (Hz)',ytitle='Magnitude')
    
    # Clean the signal and plot the frequency graph of the new signal
    fft_clean = clean_spectrum(fft) # Edit this function
    mag = calc_mag(fft_clean)
    plotgraph(rec=mag,fs=1,fname='fft_clean.html',title='Clean signal spectrum',xtitle='Frequency (Hz)',ytitle='Magnitude')
   
    # Perform inverse FFT, plot magnitudes and play back again
    ifft = calc_ifft(fft) # Edit this function
    mag = calc_mag(ifft)
    plotgraph(rec=mag,fs=fs,fname='ifft.html',title='Clean audio output',xtitle='Time (s)',ytitle='Amplitude')
    playback(ifft.real,fs)

    # Save resulting audio to file
    wavfile.write('bbcnews181210.mediaformat.clean.wav',fs,ifft.real)

    return


def calc_mag(fft):
    """
    Given a complex frequency spectrum, calculate and return the magnitude of the
    spectrum at each frequency

    Useful functions: np.real, np.imag
    """

    # Your code here

    return mag    


def calc_fft(rec):
    """
    Given an audio sample, calculate the DFT of the sample

    Useful function: np.fft.fft
    """

    # Your code here

    return fft


def clean_spectrum(fft):
    """
    Remove unwanted frequencies from the FFT spectrum
    """

    # Your code here

    return fft



def calc_ifft(fft):
    """
    Perform inverse Fourier transform

    See list of np.fft.* functions at https://docs.scipy.org/doc/numpy-1.15.0/reference/routines.fft.html
    """

    # Your code here

    return ifft


def record(fs=44100,duration=5): # Hz, seconds
    """
    Record a wave-file and save it as an array of magnitudes
    """
    print('\a')
    rec = sd.rec(int(duration * fs), samplerate=fs, channels=1, blocking=True)
    print('\a')
    rec = rec.T[0]
    np.savetxt('bbcnews181210.wav',rec)
    return rec


def load_audio(fname):
    """
    Load audio from a given filename
    """

    rec = np.loadtxt(fname,dtype=np.complex128)

    return rec


def playback(rec,fs):
    """
    Play audio
    """

    sd.play(rec,fs,blocking=True)

    return rec


def plotgraph(rec=None,fs=1,fname=None,title=None,xtitle=None,ytitle=None):

    x = np.arange(len(rec)) / fs
    y = rec
    trace = go.Scatter(x=x,y=y)
    data = [trace]

    layout = go.Layout(
        title=title,
        xaxis=dict(
            title=xtitle,
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title=ytitle,
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )


    fig = go.Figure(data=data,layout=layout)
    plotly.offline.plot(fig, filename=fname)
    return


if __name__ == '__main__':
    main()
