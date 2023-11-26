import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from Utilidades import confirmacion

def guardarCoches(cochesRaiz):
    
    """
    menu que usa los

    :param name: The name of the person to greet.
    :type name: str
    :return: A greeting message.
    :rtype: str
    """
    
    file = open("Comercio_XML\\Comercio\Coches\\coches.xml", "w")
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
    menu que usa los

    :param name: The name of the person to greet.
    :type name: str
    :return: A greeting message.
    :rtype: str
    """
    
    from xml.etree import ElementTree
    from xml.dom import minidom
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Hecho
def crearCoche(cochesRaiz):
    
    """
    menu que usa los

    :param name: The name of the person to greet.
    :type name: str
    :return: A greeting message.
    :rtype: str
    """
    
    print("\n--- Alta Coche ---\n")
    
    fin = False
    while(not fin):
        
        correcto = False
        intentos = 3
        
        # 1 Subelemento Coche
        # Buscar devuelve la longitud de todos los coches creados y le suma uno, asi establece id
        coche = ET.SubElement(cochesRaiz, 'Coche', {'id':str(len(cochesRaiz.findall('Coche'))+1)})
        print("* Creando nuevo coche *")
        
        while(intentos>0 and not correcto):
            
            # 1.1 Subelemento matricula
            matricula = input("\nIntroduce matricula: ").strip()
            if(len(matricula) == 7):
                numeros = matricula[:4]
                letras = matricula[4:]
                if(numeros.isdigit and letras.isalpha):
                    # Compruebo que no este repetida, que lea en mayus, ya que los insertamos en mayus
                    if(not repetido(cochesRaiz, matricula.upper())):
                        matriculaXML = ET.SubElement(coche, 'Matricula')
                        matriculaXML.text = matricula.upper()
                        correcto = True
                        print("Matricula correcta")
                    else: 
                        print("Matricula repetida")
                else:
                    print("Formato incorrecto")
            else:
                print("Longitud no valida")
            intentos = intentos - 1 
        
        if(correcto): 
            
            intentos = 3
            correcto = False
             
            # 1.2 Subelemento descripcion
            descripcion = ET.SubElement(coche, 'Descripcion')
            
            # 1.2.1 Subelement modelo
            marca = input("\nIntroduce marca: ").strip().lower()
            marcaXML = ET.SubElement(descripcion,'Marca')
            marcaXML.text = marca
            print("Marca correcto")
            # 1.2.2 Subelement modelo
            modelo = input("\nIntroduce modelo: ").strip().lower()
            modeloXML = ET.SubElement(descripcion,'Modelo')
            modeloXML.text = modelo
            print("Modelo correcto")
            
            # 1.3 Subelemento anio fabricacion
            while(intentos>0 and not correcto):
                anio = input("\nIntroduce anio de fabricacion: ").strip()
                if(anio.isdigit()):
                    anioXML = ET.SubElement(coche, 'AnioFabricacion')
                    anioXML.text = anio
                    print("Anio de fabricacion correcto")
                    correcto = True
                else:
                    print("Error. El anio debe ser un numero")
        
        if(correcto):
            
            intentos = 3
            correcto = False
            
            # 1.4 tarifa por dia
            while(intentos>0 and not correcto):
                tarifa = input("\nIntroduce tarifa por dia: ").strip()
                if(tarifa.isdecimal):
                    tarifaXML = ET.SubElement(coche, 'TarifaPorDia')
                    tarifaXML.text = tarifa
                    print("Tarifa por dia correcto")
                    correcto = True
                else:
                    print("Error. Debes introducir un numero")
            
            #1.5 estado coche, cuando se crea siempre esta diponible 
            estadoXML = ET.SubElement(coche, 'Estado')
            estadoXML.text = "disponible"
                
        
        # Al final se pregunta si se quiere introducir otro coche independiente de si se ha dado de alta
        if(correcto):
            print("\nAlta realizada correctamente")
            if(not confirmacion("Desea introducir otro coche? S/N: ")):
                fin = True
        else:
            print("\nAlta no realizada")
            if(not confirmacion("Desea introducir otro coche? S/N: ")):
                fin = True

# Hecho
def eliminarCoche(cochesRaiz):
    print("\n--- Eliminar Coche ---\n")
    coche=buscarCoche(cochesRaiz)
    if(coche is not None):
        if(confirmacion("Estas seguro que deseas eliminar el coche"+coche[0].text+" (S/N)")):
            cochesRaiz.remove(coche)
            print("\nCoche eliminado exitosamente.")
        else:
            print("Borrado de coche ha sido cancelado")
        

    else:
        print("Borrado de coche ha sido cancelado")
    
def buscarCoche(cochesRaiz):
    
    """
    menu que usa los

    :param name: The name of the person to greet.
    :type name: str
    :return: A greeting message.
    :rtype: str
    """
    
    cochesEncontrados = []
    cocheDevuelto = None
    salir = False
    if(len(cochesRaiz.findall('Coche'))>0):
        
        while(not salir):
            opcion = menuAtributos()

            if(opcion == "1"):
                matricula = input("\nIntroduce matricula a buscar: ").strip().upper()
                coche = cochesRaiz.find(f"Coche[Matricula='{matricula}']")                
                if(coche is not None):
                    cochesEncontrados.append(coche)
                    
            elif(opcion=="2"):
                marca = input("\nIntroduce marca a buscar: ").strip().lower()
                for coche in cochesRaiz:
                    marcaEncontrada = coche.find('.//Marca')
                    if(marcaEncontrada.text==marca.upper()):
                        cochesEncontrados.append(coche)
                    
            elif(opcion=="3"):
                modelo = input("\nIntroduce modelo a buscar: ").strip().lower()
                for coche in cochesRaiz:
                    modeloEncontrado = coche.find('.//Modelo')
                    if(modeloEncontrado.text==modelo.upper()):
                        cochesEncontrados.append(coche)
                    
            elif(opcion=="4"):
                anio = input("\nIntroduce anio de fabricacion a buscar: ").strip()
                if(anio.isdigit()):
                    for coche in cochesRaiz:
                        anioEncontrado = coche.find('AnioFabricacion')
                        if(anioEncontrado.text==anio.upper()):
                            cochesEncontrados.append(coche)
                else:
                    print("Error. Debes introducir un numero")
            
            elif(opcion=="5"):
                tarifa = input("\nIntroduce tarifa por dia a buscar: ").strip()
                if(tarifa.isdigit()):
                    for coche in cochesRaiz:
                        tarifaEncontrado = coche.find('TarifaPorDia')
                        if(tarifaEncontrado.text==tarifa.upper()):
                            cochesEncontrados.append(coche)
                else:
                    print("Error. Debes introducir un numero")
            elif(opcion=="6"):
                estado = input("\nIntroduce estado de vehiculo a buscar (disponible, alquilado, en taller): ").strip().lower()
                if(estado=="disponible" or estado=="alquilado" or estado=="en taller"):
                    for coche in cochesRaiz:
                        estadoEncontrado = coche.find('Estado')
                        if(estadoEncontrado.text==estado.lower()):
                            cochesEncontrados.append(coche)
                else:
                    print("Error. Debes introducir un estado valido")
            
            elif(opcion=="0"):
                salir = True
            
            else:
                print("Opcion incorrecta")
                
            if(not salir):
                print("\n--- Resultado busqueda ---")
                for coche in cochesEncontrados:
                    idCoche = coche.get('id')
                    # Restamos porque el id siempre es +1 mayor a la posicion del archivo
                    mostrarCoches(cochesRaiz, int(idCoche)-1)
                if(len(cochesEncontrados)>1):
                    # Seleccionar la posicion
                    salirPosicion = False
                    while(not salirPosicion):
                        # Para el usuario la posicion empezara desde 1
                        posicionCoche = input("Introduce numero de coche a buscar: ").strip()
                        if(posicionCoche.isdigit() and 0<int(posicionCoche)<=len(cochesEncontrados)):
                            # Restamos 1 a la eleccion del usuario para coger la posicion correcta en el archivo
                            cocheDevuelto = cochesEncontrados[int(posicionCoche)-1]
                            salir = True
                            salirPosicion = True
                        else:
                            print("Error. Debes introducir un numero entre 1 y " + str(len(cochesEncontrados)))
                elif(len(cochesEncontrados)==1):
                    cocheDevuelto=cochesEncontrados[0]
                    salir = True
                else:
                    if(not confirmacion("No se han encontrado resultados, quieres buscar de nuevo (S/N)")):
                        salir=True
                
    # sale si no hay coches que buscar
    else:
        print("No hay coche en la base de datos")
        
    return cocheDevuelto


def modificarCoche(cochesRaiz):
    
    """
    menu que usa los

    :param name: The name of the person to greet.
    :type name: str
    :return: A greeting message.
    :rtype: str
    """    

    print("\n--- Modificacion Coche ---\n")
    coche = buscarCoche(cochesRaiz)
   
    if(coche is not None):
        finModificar = False
        while(not finModificar):
            opcion = menuAtributos()
            
            if(opcion == "1"):
                nuevaMatricula = input("\nIntroduce nueva matricula: ").strip()
                if(nuevaMatricula.isalnum and len(nuevaMatricula) == 7):
                    numeros = nuevaMatricula[:4]
                    letras = nuevaMatricula[4:]
                    if(numeros.isdigit() and letras.isalpha):
                        if(not repetido(cochesRaiz, nuevaMatricula.upper())):
                            if(confirmacion("Estas seguro que deseas modificar la matricula? S/N")):
                                coche.find('matricula').text = nuevaMatricula.upper()
                                print("\nMatricula modificada correctamente")
                            else:
                                print("Modificacion cancelada")
                        else: 
                            print("Matricula repetida")
                    else:
                        print("Formato incorrecto")
                else:
                    print("Matricula incorrecta")
                    
            elif(opcion=="2"):
                nuevaMarca = input("\nIntroduce nueva marca: ").strip()
                if(len(nuevaMarca) > 0):
                    if(confirmacion("Estas seguro que deseas modificar el marca? S/N")):
                        coche.find('.//Marca').text = nuevaMarca.upper()
                        print("\nMarca modificada correctamente")
                    else:
                        print("Modificacion cancelada")
                else:
                    print("Marca no puede estar vacia")
       
            elif(opcion=="3"):
                nuevoModelo = input("\nIntroduce nueva modelo: ").strip()
                if(len(nuevoModelo) > 0):
                    if(confirmacion("Estas seguro que deseas modificar el modelo? S/N")):
                        coche.find('.//Modelo').text = nuevoModelo.upper()
                        print("\nModelo modificada correctamente")
                    else:
                        print("Modificacion cancelada")
                else:
                    print("Nuevo modelo no puede estar vacio")
                    
            elif(opcion=="4"):
                nuevoAnio = input("\nIntroduce nueva anio de fabricacion: ").strip()
                if(nuevoAnio.isdigit()):
                   if(confirmacion("Estas seguro que deseas modificar el anio de fabricacion? S/N")):
                       coche.find('anio').text = nuevoAnio.upper()
                       print("\nAnio modificada correctamente")
                else:
                    print("Error. Debes introducir un numero") 
            
            elif(opcion=="5"):
                nuevaTarifa = input("\nIntroduce nueva tarifa por dia: ").strip()
                if(nuevaMatricula.isdigit()):
                    if(confirmacion("Estas seguro que deseas modificar el tarifa por dia? S/N")):
                        coche.find('tarifaPorDia').text = nuevaTarifa.upper()
                        print("\nTarifa modificada correctamente")
                else:
                    print("Error. Debes introducir un numero")
            elif():
                nuevoEstado = input("\nIntroduce nueva estado de vehiculo: ").strip().lower()
                if(nuevoEstado=="disponible" or nuevoEstado=="alquilado" or nuevoEstado=="en taller"):
                    if(confirmacion("Estas seguro que deseas modificar el estado de vehiculo? S/N")):
                        coche.find('Estado').text = nuevoEstado.lower()
                        print("\nEstado modificado correctamente")
                    else:
                        print("Modificacion cancelada")
                        	
            elif(opcion=="0"):
                finModificar = True
                print("\n--- Modificacion cancelada ---")
            else:
                print("Opcion incorrecta")
             
            if(not finModificar):
                 if(not confirmacion("Quieres modificar algo mas de este coche? S/N")):
                     finModificar = True
                     print("\n--- El usuario ha cancelado seguir modificando el actual coche ---")
         
         
    else:
        print("Modificacion cancelada")
    
# Hecho
def mostrarCoches(cochesRaiz, posicion):
    
    """
    menu que usa los

    :param name: The name of the person to greet.
    :type name: str
    :return: A greeting message.
    :rtype: str
    """
    
    numeroCoche = 1
    if(posicion==-1):
        print("\n--- Mostrar todos los Coches ---\n")
        ## Elemento Coche en coches
        for coche in cochesRaiz:
            print("\nCoche:",numeroCoche)
            # Primera fila de atributos
            for atributo in coche:
                if(atributo.tag == "Descripcion"):
                    print("\t" + atributo.tag + ":", atributo.text, end='')  # Sin salto de línea aquí
                    # 2 fila de atributos en descripcion
                    for descripcion in atributo:
                        print("\t\t"+descripcion.tag,":", descripcion.text)
                else:    
                    print("\t"+atributo.tag,":",atributo.text)
                    
            numeroCoche = numeroCoche + 1
    else:
        # Coge el coche en la posicion que se le envia por 2 parametro
        coche = cochesRaiz[posicion]
        print("\nCoche:",posicion+1)
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
    menu que usa los

    :param name: The name of the person to greet.
    :type name: str
    :return: A greeting message.
    :rtype: str
    """
    
    fin = False
    while(not fin):
        print("Elige atributo")
        print("\n--- Atributos ---\n")
        print("1 - Matricula")
        print("2 - Marca")
        print("3 - Modelo")
        print("4 - Anio de fabricacion")
        print("5 - Tarifa por dia")
        print("6 - Estado Coche")
        print("0 - Salir")
        opcion = input("Introduce una opcion: ")
        if(opcion.isdigit() and int(opcion) >= 0 and int(opcion) <6):
            fin = True          
        else:
            print("Opcion no valida")
    return opcion

def repetido(cochesRaiz, matricula):
    
    """
    menu que usa los

    :param name: The name of the person to greet.
    :type name: str
    :return: A greeting message.
    :rtype: str
    """
    
    repetido = False
    for coche in cochesRaiz:
        if(coche.find('matricula') is not None and coche[0].text==matricula):
            repetido=True
    
    return repetido


def menuCoches():  
    
    """
    menu que usa los

    :param name: The name of the person to greet.
    :type name: str
    :return: A greeting message.
    :rtype: str
    """
    
    try:
        # Si hay archivo, coge la raiz 'Coches'
        cochesRaiz = ET.parse("Comercio_XML\\Comercio\Coches\\coches.xml").getroot()
    except:
        print("No existe el documento, lo creamos")
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
        opcion = input("Elige una opcion")

        if(opcion == "1"):
            crearCoche(cochesRaiz)
        elif(opcion == "2"):
            eliminarCoche(cochesRaiz)
        elif(opcion == "3"):
            buscarCoche(cochesRaiz)
        elif(opcion == "4"):
            modificarCoche(cochesRaiz)
        elif(opcion == "5"):
            mostrarCoches(cochesRaiz,-1)
        elif(opcion == "0"):
            guardarCoches(cochesRaiz)
            fin = True
            print("Vuelta Menu Principal")
        else:
            print("Opcion no valida")