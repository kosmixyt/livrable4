import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# params 
Fp = 10
bit_rate = 200

# def low_pass_filter(signal: np.array, cutoff_freq: int, sample_rate: int) -> np.array:
#     nyquist_rate = sample_rate / 2.0
#     normal_cutoff = cutoff_freq / nyquist_rate
#     b, a = butter(1, normal_cutoff, btype='low', analog=False)
#     filtered_signal = lfilter(b, a, signal)
#     return filtered_signal

def demodulate_ask(signal: np.array, carrier_freq: int, sample_rate: int) -> np.array:
    t = np.arange(len(signal)) / sample_rate
    carrier = np.sin(2 * np.pi * carrier_freq * t)
    demodulated = signal * carrier
    return demodulated

def decode_demodulated_signal(demodulated: np.array, bit_rate: int, sample_rate: int) -> list[int]:
    Ns = int(sample_rate / bit_rate)
    bits = []
    for i in range(0, len(demodulated) - Ns + 1, Ns):
        bit_chunk = demodulated[i:i+Ns]
        bit = 1 if np.mean(bit_chunk) > 0 else 0
        bits.append(bit)
    return bits


def binary_to_text(binary: list[int]) -> str:
    binary_str = ''.join(map(str, binary))
    return ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))


def main():
    ASK, sample_rate = sf.read('ask_signal.wav')
    demodulated_signal = demodulate_ask(ASK, Fp, sample_rate)
    binary_list = decode_demodulated_signal(demodulated_signal, bit_rate, sample_rate)
    Itype = "audio"
    if Itype == "text":
        decoded_text = binary_to_text(binary_list)
        print("Decoded text:", decoded_text)
    else:
        audio = np.array(binary_list)
        # audio from int64 to float64
        audio = audio.astype(np.float64)
        sf.write('received_audio.wav', audio, sample_rate)
    size = 1000
    t = np.arange(len(demodulated_signal)) / sample_rate
    plt.plot(t[:size], demodulated_signal[:size])
    plt.show()

if __name__ == "__main__":
    main()
