import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import scipy.signal as signal


bit_rate = 200       # Correct bit rate to 200 bits/s
Fe = 96_000           # Update sample rate to 96 kHz for proper carrier synthesis
Ap = 1 
Fp = 30_000  # set carrier frequency to 30 kHz (inaudible)

def from_text(text):
    # conversion de texte en binare sur 8 bit
    return [int(bit) for c in text for bit in format(ord(c), '08b')]

def binary_string_to_array(s):
    return [int(c) for c in s]

def from_audio(path : str):
    audio_data, sample_rate = sf.read('audio.wav')
    if len(audio_data.shape) > 1:
        audio_data = audio_data[:, 0]
    return audio_data, sample_rate



def lowpass_filter(data, cutoff, fs, order=5):
    for i in range(2):
        b, a = signal.butter(order, cutoff / (fs / 2), btype='low', analog=False)
        data = signal.filtfilt(b, a, data)
    return data

    

def text_to_binary(text) -> list[int]:
    return [int(bit) for char in text for bit in format(ord(char), '08b')]

def encode_nrz(binary: list[int]) -> np.array:
    return np.array([1 if bit == 1 else -1 for bit in binary])


def binary_to_text(binary: list[int]) -> str:
    binary_str = ''.join(map(str, binary))
    # Pad the binary string to ensure it's a multiple of 8 bits
    padded_binary_str = binary_str + '0' * ((8 - len(binary_str) % 8) % 8)
    return ''.join(chr(int(padded_binary_str[i:i+8], 2)) for i in range(0, len(padded_binary_str), 8))


if __name__ == "__main__":
    Itype = "audio"
    if Itype == "text":
        binary = from_text("amaury, j'adore ramsez le chat de feu vert")
        binary = encode_nrz(binary)
        Nbis = len(binary)
        Ns = int(Fe / bit_rate)    
        N = Nbis * Ns
        M_dupliquer = np.repeat(binary, Ns)
        t = np.linspace(0, N/Fe, N, endpoint=False)
        Porteuse = Ap * np.sin(2 * np.pi * Fp * t)
        ASK = Porteuse * M_dupliquer
    else:
        # Use audio file directly
        audio, sample_rate = from_audio("audio.wav")
        # le fichier audio est en stéréo, on prend le canal gauche
        if len(audio.shape) > 1:
            audio = audio[:, 0]
        #  il a une Fe = 44100 Hz
        N = len(audio)
        t = np.linspace(0, N/sample_rate, N, endpoint=False)
        Porteuse = Ap * np.sin(2 * np.pi * Fp * t)
        ASK = Porteuse * audio
    # ...existing code for plotting...
    plt.plot(t[:1000], ASK[:1000])
    plt.show()
    sf.write('ask_signal.wav', ASK, Fe)



