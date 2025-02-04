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
    #  itération du texte pour chaque caractère et conversion d'abords
    # en ascii et après en binaire
    return [int(bit) for c in text for bit in format(ord(c), '08b')]


def from_audio(path : str):
    # on lis le fichier audio puis on récupère l'audio et le taux d'échantillonnage
    audio_data, sample_rate = sf.read('audio.wav')
    # si le fichier audio est en stéréo, on prend le canal gauche
    if len(audio_data.shape) > 1:
        # récupère uniquement le canal gauche
        audio_data = audio_data[:, 0]
        # on retourne l'audio et le taux d'échantillonnage
    return audio_data, sample_rate


# encodage NRZ (Non-Return-to-Zero)
def encode_nrz(binary: list[int]) -> np.array:
    # on itère le binaire et on remplace les 0 par -1
    return np.array([1 if bit == 1 else -1 for bit in binary])


if __name__ == "__main__":
    # on demande à l'utilisateur de choisir le type de signal à envoyer
    Itype = "text"
    # si c'est du texte
    if Itype == "text":
        # texte à envoyer
        binary = from_text("amaury, j'adore ramsez le chat de feu vert")
        # on encode le signal en NRZ
        binary = encode_nrz(binary)
        # on récupère le nombre de bits
        Nbis = len(binary)
        #  on calcule le nombre d'échantillons par bit
        Ns = int(Fe / bit_rate)    
        # on calcule le nombre total d'échantillons
        N = Nbis * Ns
        # on duplique le signal binaire
        M_dupliquer = np.repeat(binary, Ns)
        # on crée le vecteur de temps
        t = np.linspace(0, N/Fe, N, endpoint=False)
        # on crée le signal porteuse
        Porteuse = Ap * np.sin(2 * np.pi * Fp * t)
        # on crée le signal ASK
        print(M_dupliquer)
        ASK = Porteuse * M_dupliquer
    else:
        # si l'utilisateur a choisi un fichier audio
        # on récupère l'audio et le taux d'échantillonnage
        audio, sample_rate = from_audio("audio.wav")
        
        # on calcule le nombre d'échantillons
        Porteuse = Ap * np.sin(2 * np.pi * Fp * t)
        ASK = Porteuse * audio
        # on normalise l'audio entre -1 et 1
        audio = audio / np.max(np.abs(audio))
        # on quantifie l'audio en binaire
        binary_audio = np.unpackbits(np.array(audio * 127, dtype=np.int8).view(np.uint8))
        # on encode le signal en NRZ
        binary_audio = encode_nrz(binary_audio)
        # on duplique le signal binaire
        M_dupliquer = np.repeat(binary_audio, int(Fe / bit_rate))
        # on crée le signal ASK
        ASK = Porteuse * M_dupliquer[:N]

    # ...existing code for plotting...
    plt.plot(t[:1000], ASK[:1000])
    plt.show()
    sf.write('ask_signal.wav', ASK, Fe)



