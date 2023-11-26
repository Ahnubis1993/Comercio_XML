def confirmacion(mensaje):
    
    """
    menu que usa los

    :param name: The name of the person to greet.
    :type name: str
    :return: A greeting message.
    :rtype: str
    """
    
    salir = False
    eleccion = False
    while(not salir):
        respuesta = input(mensaje).lower()
        if(respuesta == "s" or respuesta == "si"):
            eleccion = True
            salir = True
        elif(respuesta == "n" or respuesta == "no"):
            eleccion = False
            salir = True
        else:
            print("Opcion incorrecta")
            
    return eleccion