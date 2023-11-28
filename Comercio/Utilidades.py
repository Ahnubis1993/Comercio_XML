def confirmacion(mensaje):
    
    """
    Solicita al usuario una confirmacion mediante un mensaje.

    Args:
        mensaje (str): El mensaje que se mostrara al usuario.

    Returns:
        bool: True si la respuesta es afirmativa, False si es negativa.
    """
    
    salir = False
    eleccion = False
    while(not salir):
        respuesta = input(mensaje).strip().lower()
        if(respuesta.startswith("s")):
            eleccion = True
            salir = True
        elif(respuesta.startswith("n")):
            eleccion = False
            salir = True
        else:
            print("Opcion incorrecta")
            
    return eleccion