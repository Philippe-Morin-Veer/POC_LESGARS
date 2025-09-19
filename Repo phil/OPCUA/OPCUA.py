import RPi.GPIO as GPIO
import asyncio
LedR=False
LedB=False
LedG=False


while True:
    lumiere= input("Entrez une couleur de lumiere (r, g, b) ou bien si vous voulez fermer le programme, appuyez sur Entrée: ")
    if lumiere=="r":
        if LedR==False:
           
            LedR=True
        else:

            LedR=False
    elif lumiere=="g":
        if LedG==False:
            
            LedG=True
        else:
            
            LedG=False
    elif lumiere=="b":
        if LedB==False:
        
            LedB=True
        else:
        
            LedB=False
    elif lumiere=="":
        break
    else:
        print("Vous n'avez pas choisi un type de lumiere valide")
