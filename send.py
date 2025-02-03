import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


carrier_freq = 2000  # Fréquence de la porteuse (Hz)
bit_rate = 100       # Débit binaire (bits/s)
sample_rate = 44100  # Taux d'échantillonnage (Hz)
Fe =  44100


def from_text(text):
    print("Hello World!")
    Duration = 10
    encoded = text_to_binary(text)
    return encoded

def from_audio(path : str):
    audio_data, sample_rate = sf.read('audio.wav')
    if len(audio_data.shape) > 1:
        audio_data = audio_data[:, 0]
    return audio_data
    



# 


def text_to_binary(text) -> str:
    return ''.join(format(ord(c), "08b") for c in text)

def binary_to_text(binary) -> str:
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)) 

def encode_nrz(binary : str) -> np.array:
    return np.array([1 if bit == '1' else -1 for bit in binary])


def decode_nrz(signal : np.array) -> str:
    return ''.join('1' if bit == 1 else '0' for bit in signal)


def porteuse(t : np.array) -> np.array:
    return np.sin(2 * np.pi * carrier_freq * t)






if __name__ == "__main__":
    Itype = "text"
    if Itype:
        binary = from_text("Hello World!")
    else:
        binary = from_audio("audio.wav");
    

    t = np.arange(0, len(binary) / sample_rate, 1/Fe)

    nrz_encoded = encode_nrz(binary)
    
    print(nrz_encoded)
    carrier = porteuse(t)
    print(carrier)   
    

    ask_signal = nrz_encoded * carrier
    plt.plot(t[:1000], ask_signal[:1000])
    plt.show()
    sf.write('ask_signal.wav', ask_signal, sample_rate)
    