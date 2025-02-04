import numpy as np
import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# params 
Fp = 30_000     # fréquence de la porteuse
bit_rate = 200  # bit_rate = 200 bits/s
Fe = 96_000     # Fe = 96 kHz

def binary_to_text(binary: list[int]) -> str:
    binary_str = ''.join(map(str, binary))
    # Pad the binary string to ensure it's a multiple of 8 bits
    padded_binary_str = binary_str + '0' * ((8 - len(binary_str) % 8) % 8)
    return ''.join(chr(int(padded_binary_str[i:i+8], 2)) for i in range(0, len(padded_binary_str), 8))


def main():
    file, samplerate = sf.read("ask_signal.wav")
    # assume samplerate now equals Fe=96000; otherwise, use Fe for consistency
    N = len(file)
    Ns = int(Fe / bit_rate)
    t = np.arange(N) / Fe
    carrier = np.sin(2 * np.pi * Fp * t)
    demodulated = file * carrier
    Res = []
    for i in range(0, N, Ns):
        segment = demodulated[i:i+Ns]
        if len(segment) < Ns:
            break
        # integrate the segment (using dx=1/Fe)
        Res.append(np.trapz(segment, dx=1/Fe))
    # Determine each bit using a 0 threshold
    demodulated_bits = [1 if value > 0 else 0 for value in Res]
    print(demodulated_bits)
    # Transformation du signal binaire en signal audio à 44100 Hz
    new_Fe = 44100
    Ns_audio = int(new_Fe / bit_rate)
    # Map 0 -> -1, 1 -> 1 et doubler chaque bit en Ns_audio échantillons
    audio_signal = np.repeat(np.array(demodulated_bits) * 2 - 1, Ns_audio).astype(np.float32)
    print(audio_signal)
    sd.play(audio_signal, new_Fe)
    sd.wait()

    
    # for text
    # chars = []

    # for i in range(0, len(demodulated_bits), 8):
    #     byte = demodulated_bits[i:i+8]
    #     if len(byte) < 8:
    #         break
    #     byte_str = ''.join(map(str, byte))
    #     chars.append(chr(int(byte_str, 2)))
    # print("Decoded text:", ''.join(chars))
if __name__ == "__main__":
    main()
