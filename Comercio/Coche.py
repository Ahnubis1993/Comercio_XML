import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from Utilidades import confirmacion

def guardarCoches(cochesRaiz):
    
    """
    Guarda la estructura XML completa en el fichero coches.xml.

    Args:
        cochesRaiz (Element): El elemento raiz XML de los coches que seran guardados.
    
    Returns:
        None
    """
    
    file = open("Comercio\\Coches\\coches.xml", "w")
    archivoDefinido = prettify(cochesRaiz)
    
    lineas = archivoDefinido.split("\n")
    textoCorreecto=""
    
    for i in lineas:
        if i.strip()!="":
            textoCorreecto=textoCorreecto+str(i)+"\n"
    
    file.writelines(textoCorreecto)
    file.close()


def prettify(elem):
    
    """
    Retorna una cadena XML con formato para el elemento.

    Args:
        elem (Element): El elemento XML que se formateara.

    Returns:
        str: Una cadena con formato XML facil de leer.
    """
    
    from xml.etree import ElementTree
    from xml.dom import minidom
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def crearCoche(cochesRaiz):
    
    """
    Crea un nuevo coche en la estructura XML. Pide al usuario que introduzca la Matricula, 
    Marca, Modelo, Anio de fabricacion y Tarifa por dia.

    Args:
        cochesRaiz (Element): El elemento raiz que contiene la informacion de los coches.
    
    Returns:
        None
    """
    
    print("\n--- Alta Coche ---")
    
    fin = False
    while(not fin):
        
        correcto = False
        intentos = 3
        
        # 1 Subelemento Coche
        # Se busca el id del ultimo coche para incrementarlo para el nuevo coche
        ultimoCoche = cochesRaiz.find(".//Coche[last()]")
        ultimoId = int(ultimoCoche.get("id"))
        coche = ET.SubElement(cochesRaiz, 'Coche', {'id':str(ultimoId+1)})
        print("* Creando nuevo coche *")
        
        while(intentos>0 and not correcto):
            
            # 1.1 Subelemento matricula
            matricula = input("\nIntroduce matricula: ").strip()
            if(len(matricula) == 7):
                numeros = matricula[:4]
                letras = matricula[4:]
                if(numeros.isdigit() and letras.isalpha()):
                    # Compruebo que no este repetida, que lea en mayus, ya que los insertamos en mayus
                    if(not repetido(cochesRaiz, matricula.upper())):
                        matriculaXML = ET.SubElement(coche, 'Matricula')
                        matriculaXML.text = matricula.upper()
                        print("Matricula correcta")
                        correcto = True
                    else: 
                        print("Matricula repetida")
                else:
                    print("Formato incorrecto")
            else:
                print("Longitud no valida")
            intentos = intentos - 1 
        
        if(correcto): 
            
            # 1.2 Subelemento descripcion
            descripcion = ET.SubElement(coche, 'Descripcion')
            
            intentos = 3
            correcto = False
             
            # 1.2.1 Subelement marca
            while(intentos>0 and not correcto):
                marca = input("\nIntroduce marca: ").strip()
                if (marca != ""):
                    marcaXML = ET.SubElement(descripcion,'Marca')
                    marcaXML.text = marca
                    print("Marca correcto")
                    correcto = True
                else:
                    print("La marca no puede estar vacia")
                    intentos -= 1

        if (correcto):
            intentos = 3
            correcto = False
            # 1.2.2 Subelement modelo
            while(intentos>0 and not correcto):
                modelo = input("\nIntroduce modelo: ").strip()
                if (modelo != ""):
                    modeloXML = ET.SubElement(descripcion,'Modelo')
                    modeloXML.text = modelo
                    print("Modelo correcto")
                    correcto = True
                else:
                    print("El modelo no puede estar vacio")
                    intentos -= 1
            
        if (correcto):
            intentos = 3
            correcto = False
            # 1.3 Subelemento anio fabricacion
            while(intentos>0 and not correcto):
                anio = input("\nIntroduce anio de fabricacion: ").strip()
                if(anio.isdigit()):
                    anioXML = ET.SubElement(coche, 'AnioFabricacion')
                    anioXML.text = anio
                    print("Anio de fabricacion correcto")
                    correcto = True
                else:
                    intentos -= 1
                    print("El anio debe ser un numero")
        
        if(correcto):
            
            intentos = 3
            correcto = False
            
            # 1.4 tarifa por dia
            while(intentos>0 and not correcto):
                tarifa = input("\nIntroduce tarifa por dia: ").strip()
                if(tarifa.isdigit() and tarifa != ""):
                    tarifaXML = ET.SubElement(coche, 'TarifaPorDia')
                    tarifaXML.text = tarifa
                    print("Tarifa por dia correcto")
                    correcto = True
                else:
                    intentos -= 1
                    print("Debes introducir un numero")
            
            #1.5 estado coche, cuando se crea siempre esta diponible 
            estadoXML = ET.SubElement(coche, 'Estado')
            estadoXML.text = "disponible"
                
        
        # Al final se pregunta si se quiere introducir otro coche independiente de si se ha dado de alta
        if(correcto):
            print("\nAlta coche realizada correctamente")
        else:
            cochesRaiz.remove(coche)
            print("\nAlta coche no realizada")
        if(not confirmacion("Desea introducir otro coche? S/N: ")):
            fin = True


def eliminarCoche(cochesRaiz):
    
    """
    Elimina un registro de coche de la estructura XML. Invoca la funcion buscar para que 
    devuelva un unico coche y pregunta confirmacion al usuario

    Args:
        cochesRaiz (Element): El elemento raiz que contiene la informacion de los coches.

    Returns:
        None
    """
    
    print("\n--- Eliminar Coche ---")
    coche=buscarCoche(cochesRaiz, True)
    if(coche is not None):
        #no se puede eliminar un coche que se encuentra en alquiler o en el taller
        if(coche.find('Estado').text != "disponible" and coche.find('Estado').text!= "en taller"):
            if(confirmacion("Estas seguro que deseas eliminar el coche con matricula '"+coche[0].text+"' (S/N)")):
                cochesRaiz.remove(coche)
                print("\nCoche eliminado exitosamente.")
            else:
                print("La eliminacion del coche ha sido cancelada")
        else:
            print("Un coche que se encuentra en alquiler o en el taller no puede ser eliminado")
    else:
        print("Borrado de coche ha sido cancelado")
    
    
def buscarCoche(cochesRaiz, devolverUnico):
    
    """
    Busca coches en la estructura XML. Permite buscar por cualquier parametro.
    La busqueda es difusa para todos los campos excepto Matricula y no es case sensitive.

    Args:
        cochesRaiz (Element): El elemento raiz que contiene la informacion de los coches.
        devolverUnico (bool): Indica si se debe devolver un unico coche (True) o una lista de coches (False).

    Returns:
        None: Si no se encuentra ningún coche o si devolverUnico es False
        Element: Si se encuentra un coche y devolverUnico es True.
    """
    
    cochesEncontrados = []
    cocheDevuelto = None
    cancelar = False
    if(len(cochesRaiz.findall('Coche'))>0):
        while(not cancelar):
            print("--- Busqueda de coches ---")
            opcion = menuAtributos()

            if(opcion == "1"):
                matricula = input("\nIntroduce matricula a buscar: ").strip().upper()
                coche = cochesRaiz.find(f"Coche[Matricula='{matricula}']")                
                if(coche is not None):
                    cochesEncontrados.append(coche)
                    
            elif(opcion=="2"):
                marca = input("\nIntroduce marca a buscar: ").strip().lower()
                for coche in cochesRaiz:#Por cada coche se toma la marca
                    marcaEncontrada = coche.find('.//Marca')
                    if(marca in marcaEncontrada.text.lower()):# Si la marca del coche iterado contiene el input, se aniade el coche a los resultados
                        cochesEncontrados.append(coche)
                    
            elif(opcion=="3"):
                modelo = input("\nIntroduce modelo a buscar: ").strip().lower()
                for coche in cochesRaiz:
                    modeloEncontrado = coche.find('.//Modelo')
                    if(modelo in modeloEncontrado.text.lower()):
                        cochesEncontrados.append(coche)
                    
            elif(opcion=="4"):
                anio = input("\nIntroduce anio de fabricacion a buscar: ").strip()
                if(anio.isdigit()):
                    for coche in cochesRaiz:
                        anioEncontrado = coche.find('AnioFabricacion')
                        if(anio in anioEncontrado.text):
                            cochesEncontrados.append(coche)
                else:
                    print("Error. Debes introducir un numero")
            
            elif(opcion=="5"):
                tarifa = input("\nIntroduce tarifa por dia a buscar: ").strip()
                if(tarifa.isdigit()):
                    for coche in cochesRaiz:
                        tarifaEncontrado = coche.find('TarifaPorDia')
                        if(tarifa in tarifaEncontrado.text):
                            cochesEncontrados.append(coche)
                else:
                    print("Error. Debes introducir un numero")
            elif(opcion=="6"):
                estado = input("\nIntroduce estado de vehiculo a buscar (disponible, alquilado, en taller): ").strip().lower()
                if(estado=="disponible" or estado=="alquilado" or estado=="en taller"):
                    for coche in cochesRaiz:
                        estadoEncontrado = coche.find('Estado')
                        if(estado in estadoEncontrado.text):
                            cochesEncontrados.append(coche)
                else:
                    print("Error. Debes introducir un estado valido")
            elif(opcion=="0"):
                cancelar = True
            else:
                print("Opcion incorrecta")
                
            if(not cancelar):#Si el usuario no ha cancelado se muestran los resultados
                print("\n--- Resultados de la busqueda ---")
                for coche in cochesEncontrados:
                    mostrarCoches(cochesRaiz, coche)
                if(len(cochesEncontrados)>1 and devolverUnico):
                    salirId = False
                    while(not salirId):
                        idCoche = input("Introduce numero de coche a buscar: ").strip()
                        cocheDevuelto = [coche for coche in cochesEncontrados if(coche.get("id") == idCoche)]#FIXME
                        if (cocheDevuelto is not None):
                            cancelar = True
                            salirId = True
                        else:
                            print("Introduce un identificador de coche valido")
                elif(len(cochesEncontrados)==1):
                    cocheDevuelto=cochesEncontrados[0]
                    cancelar = True
                else:
                    if(not confirmacion("No se han encontrado resultados, quieres buscar de nuevo (S/N)")):
                        cancelar=True
    else:   # sale si no hay coches que buscar
        print("No hay coche en la base de datos")
        
    return cocheDevuelto[0]


def modificarCoche(cochesRaiz):  

    """
    Modifica un campo de un coche encontrado por la funcion buscarCoche.
    El usuario puede elegir que campo modificar y se le pide confirmacion.

    Args:
        cochesRaiz (Element): El elemento raiz que contiene la informacion de los coches.

    Returns:
        None
    """
    
    print("\n--- Modificacion Coche ---")
    coche = buscarCoche(cochesRaiz, True)
   
    if(coche is not None):
        cancelado = False
        while(not cancelado):
            opcion = menuAtributos()
            
            if(opcion == "1"):
                nuevaMatricula = input("\nIntroduce la nueva matricula: ").strip().upper()
                if(len(nuevaMatricula) == 7):
                    numeros = nuevaMatricula[:4]
                    letras = nuevaMatricula[4:]
                    if(numeros.isdigit() and letras.isalpha):
                        if(not repetido(cochesRaiz, nuevaMatricula)):
                            if(confirmacion("Estas seguro de que deseas modificar la matricula? (S/N): ")):
                                coche.find('Matricula').text = nuevaMatricula
                                print("\nMatricula modificada correctamente")
                            else:
                                print("Modificacion cancelada")
                        else: 
                            print("Ya existe un coche con esa matricula")
                    else:
                        print("Formato no valida")
                else:
                    print("Matricula no valida")
                    
            elif(opcion=="2"):
                nuevaMarca = input("\nIntroduce la nueva marca: ").strip()
                if(nuevaMarca != ""):
                    if(confirmacion("Estas seguro de que deseas modificar la marca? (S/N): ")):
                        coche.find('.//Marca').text = nuevaMarca
                        print("\nMarca modificada correctamente")
                    else:
                        print("Modificacion cancelada")
                else:
                    print("La marca no puede estar vacia")
       
            elif(opcion=="3"):
                nuevoModelo = input("\nIntroduce el nuevo modelo: ").strip()
                if(nuevoModelo != ""):
                    if(confirmacion("Estas seguro de que deseas modificar el modelo? (S/N): ")):
                        coche.find('.//Modelo').text = nuevoModelo
                        print("\nModelo modificado correctamente")
                    else:
                        print("Modificacion cancelada")
                else:
                    print("El modelo no puede estar vacio")
                    
            elif(opcion=="4"):
                nuevoAnio = input("\nIntroduce un nuevo anio de fabricacion: ").strip()
                if(nuevoAnio.isdigit() and nuevoAnio != ""):
                    if(confirmacion("Estas seguro de que deseas modificar el anio de fabricacion? (S/N): ")):
                       coche.find('AnioFabricacion').text = nuevoAnio
                       print("\nAnio modificado correctamente")
                    else:
                        print("Modificacion cancelada")
                else:
                    print("Debes introducir un numero") 
            
            elif(opcion=="5"):
                nuevaTarifa = input("\nIntroduce la nueva tarifa por dia: ").strip()
                if(nuevaTarifa.isdigit() and nuevaTarifa != ""):
                    if(confirmacion("Estas seguro de que deseas modificar la tarifa por dia? (S/N): ")):
                        coche.find('TarifaPorDia').text = nuevaTarifa
                        print("\nTarifa modificada correctamente")
                    else:
                        print("Modificacion cancelada")
                else:
                    print("Debes introducir un numero")
            elif(opcion=="6"):
                nuevoEstado = input("\nIntroduce el nuevo estado de vehiculo (disponible/en taller): ").strip().lower()
                if(nuevoEstado=="disponible" or nuevoEstado=="en taller"):
                    if(confirmacion("Estas seguro que deseas modificar el estado de vehiculo? S/N")):
                        coche.find('Estado').text = nuevoEstado
                        print("\nEstado modificado correctamente")
                    else:
                        print("Modificacion cancelada")
                elif(nuevoEstado=="alquilado"):
                    print("No se puede establecer un coche como alquilado. Para ello crea un alquiler con este coche.")
                else:
                    print(nuevoEstado,"no es un estado valido.")
            elif(opcion=="0"):
                cancelado = True
                print("\nModificacion cancelada")
            else:
                print("Opcion incorrecta")
             
            if(not cancelado):
                 if(not confirmacion("Quieres modificar algo mas de este coche? S/N")):
                     cancelado = True
                     print("\n--- Has terminado de modificar el coche actual ---")
    else:
        print("Modificacion cancelada")
    
    
def mostrarCoches(cochesRaiz, coche):
    
    """
    Muestra los coches del elemento XML. Muestra solo un coche si lo recibe por parametro

    Args:
        cochesRaiz (Element): El elemento raiz que contiene la informacion de los coches que se mostraran.
        coche (Element): El coche especifico que se desea mostrar. Si es None, se muestran todos los coches.

    Returns:
        None
    """
    
    if(coche is None):
        print("\n--- Mostrar todos los Coches ---")
        ## Elemento Coche en coches

        for coche in cochesRaiz:
            print("\nCoche:",coche.get("id"))
            # Primera fila de atributos
            for atributo in coche:
                if(atributo.tag == "Descripcion"):
                    print("\tDescripcion:")  # Sin salto de línea aquí
                    # 2 fila de atributos en descripcion
                    for campo in atributo:
                        print("\t\t"+campo.tag,":", campo.text)
                else:    
                    print("\t"+atributo.tag,":",atributo.text)
    else:
        # Coge el coche en la posicion que se le envia por 2 parametro
        print("\nCoche:",coche.get("id"))
        # Primera fila de atributos
        for atributo in coche:
            if(atributo.tag == "Descripcion"):
                print("\t" + atributo.tag + ":", atributo.text, end='')  # Sin salto de línea aquí
                # 2 fila de atributos en descripcion
                for descripcion in atributo:
                    print("\t\t"+descripcion.tag,":",descripcion.text)
            else:    
                print("\t"+atributo.tag,":",atributo.text)
    
    
def menuAtributos():
    
    """
    Muestra un menu de atributos de coche y solicita al usuario que elija una opcion.

    Returns:
        str: La opción elegida por el usuario (del '0' al '6').
    """
    
    fin = False
    while(not fin):
        print("Elige un atributo de los siguientes: ")
        print("--- Atributos ---")
        print("1 - Matricula")
        print("2 - Marca")
        print("3 - Modelo")
        print("4 - Anio de fabricacion")
        print("5 - Tarifa por dia")
        print("6 - Estado Coche")
        print("0 - Salir")
        opcion = input("Introduce una opcion: ")
        if(opcion.isdigit() and 0 <= int(opcion) <=6):
            fin = True          
        else:
            print("Opcion no valida")
    return opcion

def repetido(cochesRaiz, matricula):
    
    """
    Verifica si una matricula dada ya esta registrada en la estructura XML de coches.

    Args:
        cochesRaiz (Element): El elemento raiz que contiene la informacion de los coches.
        matricula (str): La matricula que se desea verificar.

    Returns:
        bool: True si la matricula esta repetida, False si no lo esta.
    """
    
    repetido = False
    for coche in cochesRaiz:
        if(coche.find('matricula') is not None and coche[0].text==matricula):
            repetido=True
    
    return repetido


def menuCoches():  
    
    """
    Menu principal para realizar operaciones con la informacion de coches. 
    Al salir de este menu se guardan los datos en el fichero.

    Args:
        None

    Returns:
        None
    """
    
    try:
        # Si hay archivo, coge la raiz 'Coches'
        cochesRaiz = ET.parse("Comercio\\Coches\\coches.xml").getroot()
    except:
        print("No existe el documento coches.xml\nSe ha creado automaticamente")
        # Si no hay archivo, crea la raiz 'Coches'
        cochesRaiz = ET.Element('Coches')
      
    fin = False 
    while(fin == False):
        print("\n---- Menu Coches ----\n")
        print("1 - Crear Coches")
        print("2 - Eliminar Coches")
        print("3 - Buscar Coches")
        print("4 - Modificar Coches")
        print("5 - Mostrar Coches")
        print("0 - Menu Principal")
        opcion = input("Elige una opcion: ")

        if(opcion == "1"):
            crearCoche(cochesRaiz)
        elif(opcion == "2"):
            eliminarCoche(cochesRaiz)
        elif(opcion == "3"):
            buscarCoche(cochesRaiz, False)
        elif(opcion == "4"):
            modificarCoche(cochesRaiz)
        elif(opcion == "5"):
            mostrarCoches(cochesRaiz, None)
        elif(opcion == "0"):
            #Se guarda al salir de este menu
            guardarCoches(cochesRaiz)
            fin = True
            print("Vuelta Menu Principal")
        else:
            print("Opcion no valida")