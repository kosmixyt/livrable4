import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


bit_rate = 100       # Débit binaire (bits/s) baud
sample_rate = 44100  # Taux d'échantillonnage (Hz)
Fe =  44100


def from_text(text):
    return [int(bit) for c in text for bit in format(ord(c), '08b')]

def binary_string_to_array(s):
    return [int(c) for c in s]

def from_audio(path : str):
    audio_data, sample_rate = sf.read('audio.wav')
    if len(audio_data.shape) > 1:
        audio_data = audio_data[:, 0]
    return audio_data
    

def text_to_binary(text) -> list[int]:
    return (''.join(format(ord(char), '08b') for char in text)).split()

def binary_to_text(binary) -> str:
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)) 

def encode_nrz(binary : str) -> np.array:
    return np.array([1 if bit == '1' else -1 for bit in binary])


def decode_nrz(signal : np.array) -> str:
    return ''.join('1' if bit == 1 else '0' for bit in signal)




if __name__ == "__main__":
    Itype = "text"
    if Itype:
        binary = from_text("Helloworld")
    else:
        binary = from_audio("audio.wav")
    Nbis = len(binary)
    Ns = int(sample_rate / bit_rate)    
    N = Nbis * Ns
    print(type (binary))
    M_dupliquer = np.repeat(binary, Ns)
    
    t = np.linspace(0, N/Fe, N)
    

    Ap = 1 
    Fp = 20000
    Porteuse = P  = Ap*np.sin(2*np.pi*Fp*t)

    ASK = P * M_dupliquer
    print(len(ASK), binary[0])
    size = 1000
    plt.plot(t[:size], ASK[:size])
    plt.show()
    sf.write('ask_signal.wav', ASK, sample_rate)



