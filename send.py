import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


bit_rate = 200       # Débit binaire (bits/s) baud
sample_rate = 44100  # Taux d'échantillonnage (Hz)
Fe =  44100
Ap = 1 
Fp = 10  # Set carrier frequency to 25 kHz, which is inaudible to humans

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
        binary = from_text("salut la terre comment va tu j'aime tout ce que tu dis")
    else:
        binary = from_audio("audio.wav")
    # binary = encode_nrz(binary)
    Nbis = len(binary)
    Ns = int(sample_rate / bit_rate)    
    N = Nbis * Ns
    print(type (binary))
    M_dupliquer = np.repeat(binary, Ns)
    
    t = np.linspace(0, N/Fe, N)
    

    Porteuse = P  = Ap*np.sin(2*np.pi*Fp*t)

    ASK = P * M_dupliquer
    print(len(ASK), binary[0])
    size = 1000
    plt.plot(t[:size], ASK[:size])
    plt.show()
    sf.write('ask_signal.wav', ASK, sample_rate)



