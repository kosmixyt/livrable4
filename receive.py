import numpy as np
import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# params 
Fp = 10     # fréquence de la porteuse
bit_rate = 200  # bit_rate = 200 bits/s
Fe = 44100     # Fe = 44100 Hz

def binary_to_text(binary: list[int]) -> str:
    binary_str = ''.join(map(str, binary))
    # Pad the binary string to ensure it's a multiple of 8 bits
    padded_binary_str = binary_str + '0' * ((8 - len(binary_str) % 8) % 8)
    return ''.join(chr(int(padded_binary_str[i:i+8], 2)) for i in range(0, len(padded_binary_str), 8))


def main():
    binary, samplerate = sf.read("ask_signal.wav")
    modulText = ("Quelle type de modulation voulez vous utilisez")
    mod = input(modulText)
    while mod not in ["FSK", "ASK"]:
        mod = input(modulText)
    demodulated_bits = []
    print("Modulation type:", mod)
    if mod == "ASK":  
        N = len(binary)
        Ns = int(Fe / bit_rate)
        t = np.arange(N) / Fe
        carrier = np.sin(2 * np.pi * Fp * t)
        demodulated = binary * carrier
        for i in range(0, N, Ns):
            segment = demodulated[i:i+Ns]
            if len(segment) < Ns:
                break
            demodulated_bits.append(np.trapz(segment, dx=1/Fe))
    else:
        Ns = int(Fe/bit_rate)
    # compute number of bits from total samples
        Nbits = len(binary) // Ns
        N = Ns * Nbits
        M_duplique = np.repeat(binary, Ns)
        t1 = np.linspace(0, Ns/Fe, Ns)
        t = np.linspace(0, N/Fe, N)
        A1 = 1
        A2 = 1
        fp1 = 500
        fp2 = 2000
        P1 = A1 * np.sin(2 * np.pi * fp1 * t1)
        # use P1 for bit1
        P2 = A2 * np.sin(2 * np.pi * fp2 * t1)
        Porteuse1 = np.tile(P1, Nbits)
        # use P2 for bit0
        Porteuse2 = np.tile(P2, Nbits)
        bit1 = binary * Porteuse1
        bit0 = binary * Porteuse2
        y1 = []
        y2 = []
        for i in range(0, N, Ns):
            y1.append(np.trapz(bit1[i:i+Ns]))
            y2.append(np.trapz(bit0[i:i+Ns]))
        demodulated_bits = []
        for ii in range(len(y1)):
            if abs(y1[ii]) > abs(y2[ii]):
                demodulated_bits.append(1)
            else:
                demodulated_bits.append(0)
    demodulated_bits = [1 if value > 0 else 0 for value in demodulated_bits]
    chars = []
    for i in range(0, len(demodulated_bits), 8):
        byte = demodulated_bits[i:i+8]
        if len(byte) < 8:
            break
        byte_str = ''.join(map(str, byte))
        chars.append(chr(int(byte_str, 2)))
    print("Decoded text:", ''.join(chars))
if __name__ == "__main__":
    main()
