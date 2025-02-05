import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import scipy.signal as signal


bit_rate = 200       # Correct bit rate to 200 bits/s
Fe = 44100           # Update sample rate to Fe 44100 for proper carrier synthesis
Ap = 1 
Fp = 10  # set carrier frequency to 30 kHz (inaudible)
def from_text(text):
    # conversion de texte en binare sur 8 bit
    #  itération du texte pour chaque caractère et conversion d'abords
    # en ascii et après en binaire 
    # on converti le bit en int car format retourne un string
    return [int(bit) for c in text for bit in format(ord(c), '08b')]


def from_audio(path : str):
    # on lis le fichier audio puis on récupère l'audio et le taux d'échantillonnage
    audio_data, sample_rate = sf.read('audio.wav')
    # si le fichier audio est en stéréo, on prend le canal gauche
    if len(audio_data.shape) > 1:
        # récupère uniquement le canal gauche car un seul canal est nécessaire
        audio_data = audio_data[:, 0]
        # on retourne l'audio et le taux d'échantillonnage
    return audio_data, sample_rate


# encodage NRZ (Non-Return-to-Zero)
def encode_nrz(binary: list[int]) -> np.array:
    # on itère le binaire et on remplace les 0 par -1 
    return np.array([1 if bit == 1 else -1 for bit in binary])


if __name__ == "__main__":
    # on demande à l'utilisateur de choisir le type de signal à envoyer
    binary = from_text(input("Texte à envoyer : "))
    ModulationText = "Quel de Type de modulation voulez vous faire"
    modulation = ""
    while modulation not in ["ASK", "FSK"]:
        modulation = input(ModulationText)
    OUTPUT = []
    binary = encode_nrz(binary)
    if modulation == "FSK":
        Nbits = len(binary)
        Ns = int(Fe/bit_rate)
        N = Ns * Nbits
        M_duplique = np.repeat(binary, Ns)
        t1 = np.linspace(0, Ns/Fe, Ns)
        t = np.linspace(0, N/Fe, N)
        A1 = 1
        A2 = 1
        fp1 = 500
        fp2 = 2000
        P1 = A1 * np.sin(2 * np.pi * fp1 * t1)
        P2 = A2 * np.sin(2 * np.pi * fp2 * t1)
        OUTPUT = []
        for i in binary:
            if i == 1:
                OUTPUT.extend(P1)
            else:
                OUTPUT.extend(P2)   
    elif modulation == "ASK":
        Nbis = len(binary)
        #  on calcule le nombre d'échantillons par bit
        Ns = int(Fe / bit_rate)    
        # on calcule le nombre total d'échantillons
        N = Nbis * Ns
        # on duplique le signal binaire
        M_dupliquer = np.repeat(binary, Ns)
        # on crée le vecteur de temps
        t = np.linspace(0, N/Fe, N)
        # on crée le signal porteuse
        Porteuse = Ap * np.sin(2 * np.pi * Fp * t)
        # on crée le signal ASK
        print(M_dupliquer)
        OUTPUT = Porteuse * M_dupliquer
    print("ASK signal generated in ask_signal.wav" )
    sf.write('ask_signal.wav', OUTPUT, Fe)




        # 
        # # texte à envoyer
        # binary = from_text("amaury, j'adore ramsez le chat de feu vert")
        # # on encode le signal en NRZ
        # binary = encode_nrz(binary)
        # # on récupère le nombre de bits
        # Nbis = len(binary)
        # #  on calcule le nombre d'échantillons par bit
        # Ns = int(Fe / bit_rate)    
        # # on calcule le nombre total d'échantillons
        # N = Nbis * Ns
        # # on duplique le signal binaire
        # M_dupliquer = np.repeat(binary, Ns)
        # # on crée le vecteur de temps
        # t = np.linspace(0, N/Fe, N)
        # # on crée le signal porteuse
        # Porteuse = Ap * np.sin(2 * np.pi * Fp * t)
        # # on crée le signal ASK
        # print(M_dupliquer)
        # ASK = Porteuse * M_dupliquer