import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


# params 
Fp = 2000
Fe = 44100
bit_rate = 100
def demodulate_ask(signal: np.array, carrier_freq: int, sample_rate: int) -> np.array:
    t = np.arange(len(signal)) / sample_rate
    carrier = np.sin(2 * np.pi * carrier_freq * t)
    demodulated = signal * carrier
    return demodulated

def decode_demodulated_signal(demodulated: np.array, bit_rate: int, sample_rate: int) -> str:
    Ns = int(sample_rate / bit_rate)
    bits = []
    for i in range(0, len(demodulated), Ns):
        bit_chunk = demodulated[i:i+Ns]
        bit = 1 if np.mean(bit_chunk) > 0 else 0
        bits.append(bit)
    return ''.join(map(str, bits))

def binary_to_text(binary) -> str:
    binary = ''.join(binary)
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))


def main():
    ASK, sample_rate = sf.read('ask_signal.wav')
    demodulated_signal = demodulate_ask(ASK, Fp, sample_rate)
    binary_string = decode_demodulated_signal(demodulated_signal, bit_rate, sample_rate)
    decoded_text = binary_to_text(binary_string)
    print("Decoded text:", decoded_text)
    size = 1000
    t = np.arange(len(demodulated_signal)) / sample_rate
    plt.plot(t[:size], demodulated_signal[:size])
    plt.show()

if __name__ == "__main__":
    main()
