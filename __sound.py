

    # Transformation du signal binaire en signal audio à 44100 Hz
    # new_Fe = 44100
    # Ns_audio = int(new_Fe / bit_rate)
    # # Map 0 -> -1, 1 -> 1 et doubler chaque bit en Ns_audio échantillons
    # audio_signal = np.repeat(np.array(demodulated_bits) * 2 - 1, Ns_audio).astype(np.float32)
    # print(audio_signal)
    # sd.play(audio_signal, new_Fe)
    # sd.wait()



    # else:
    #     # si l'utilisateur a choisi un fichier audio
    #     # on récupère l'audio et le taux d'échantillonnage
    #     audio, sample_rate = from_audio("audio.wav")
    #     # on calcule le nombre d'échantillons
    #     Porteuse = Ap * np.sin(2 * np.pi * Fp * t)
    #     ASK = Porteuse * audio
    #     # on normalise l'audio entre -1 et 1
    #     audio = audio / np.max(np.abs(audio))
    #     # on quantifie l'audio en binaire
    #     binary_audio = np.unpackbits(np.array(audio * 127, dtype=np.int8).view(np.uint8))
    #     # on encode le signal en NRZ
    #     binary_audio = encode_nrz(binary_audio)
    #     # on duplique le signal binaire
    #     M_dupliquer = np.repeat(binary_audio, int(Fe / bit_rate))
    #     # on crée le signal ASK
    #     ASK = Porteuse * M_dupliquer[:N]

