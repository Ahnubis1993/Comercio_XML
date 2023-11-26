from Coche import menuCoches
from Alquiler import menuAlquiler

fin = False 
while(not fin):
    print("\n---- Menu Principal Comercio ----\n")
    print("Elige una opcion")
    print("1 - Menu Coches")
    print("2 - Menu Alquiler")
    print("0 - Salir")
    opcion = input("Elige una opcion: ")
    
    if(opcion == "1"):
        menuCoches()
    elif(opcion == "2"):
        menuAlquiler()
    elif(opcion == "0"):
        fin = True
        print("Fin de gestion del Comercio de alquileres de coches")
    else:
        print("Opcion no valida")

