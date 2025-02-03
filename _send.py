import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

carrier_freq = 20000  # Fréquence de la porteuse (Hz)
bit_rate = 100       # Débit binaire (bits par seconde)
sample_rate = 44100  # Taux d'échantillonnage (Hz)

# Lire le fichier audio
audio_data, sample_rate = sf.read('audio.wav')

if len(audio_data.shape) > 1:
    audio_data = audio_data[:, 0]

# Normaliser les données audio et les convertir en binaire (0 ou 1)
binary_data = (audio_data > 0).astype(int)

#porteuse
t = np.arange(0, len(binary_data) / bit_rate, 1 / sample_rate)
carrier = np.sin(2 * np.pi * carrier_freq * t)

# ASK
ask_signal = carrier * binary_data[:len(t)]

# ASK
plt.figure(figsize=(12, 6))
plt.plot(t[:1000], ask_signal[:1000])  # Afficher les 1000 premiers échantillons
plt.title('Signal ASK')
plt.xlabel('Temps (s)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()

sf.write('ask_signal.wav', ask_signal, sample_rate)