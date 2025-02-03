import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


# params 
carrier_freq = 2000  # Fréquence de la porteuse (Hz)
bit_rate = 100       # Débit binaire (bits/s)
sample_rate = 44100  # Taux d'échantillonnage (Hz)
Fe =  44100
Ns= 220
Fe = 44100
Fp= 2000

def porteuse(t : np.array) -> np.array:
    return np.sin(2 * np.pi * carrier_freq * t)




def main():
    file, sample_rate = sf.read('ask_signal.wav')
    t= np.arange (0.0,len(file))/Fe;
    Porduit = porteuse(t) * file
    y= []    
    for i in range(0,len(file),Ns):
        y.append (np.trapz(Porduit[i:i+Ns],t[i:i+Ns]))
    message_demodule = np.array(y) > 0   #renvoie True (si >0) ou False sinon

# Decodage du signal démodulé

    message_recu_decode= []
    for ii in range (0,len(message_demodule)):
        if message_demodule [ii] == True:
        
            message_recu_decode.extend([int(1)]) 
        else:
             message_recu_decode.extend([int(-1)]) 
    message_recu_bin =  [0 if i==-1 else 1 for i in message_recu_decode]  #
    bin_data = ""
    for elem in message_recu_bin:  
        bin_data += str(elem)
    data_reçu =' '
    for i in range(0, len(bin_data), 8): 
        temp_data = int(bin_data[i+1:i+8])
      
        decimal_data = BinaryToDecimal(temp_data)


        data_reçu = data_reçu + chr(decimal_data) 
    print("Le message reçu est :",   data_reçu) 


# Fonction BinarytoDecimal() function (conversion bianire ==> décimal)
def BinaryToDecimal(binary):  
    binary1 = binary 
    decimal, i, n = 0, 0, 0 #initialisation des variables
    
    while(binary != 0): 
        dec = binary % 10
        decimal = decimal + dec * pow(2, i) 
        binary = binary//10
        i += 1
    return (decimal)







if __name__ == "__main__":
    main()
