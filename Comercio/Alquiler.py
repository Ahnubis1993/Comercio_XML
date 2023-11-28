import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from Coche import buscarCoche, guardarCoches
from Utilidades import confirmacion
from datetime import datetime

def guardarAlquiler(alquileresRaiz):
    
    """
    Guarda la estructura XML de alquileres en el archivo alquileres.xml.

    Args:
        alquileresRaiz (Element): El elemento raiz del documento XML de alquileres.

    Returns:
        None
    """
    
    file = open("Comercio\\Alquileres\\alquileres.xml", "w")
    archivoDefinido = prettify(alquileresRaiz)
    
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

def crearAlquiler(alquileresRaiz, cochesRaiz):
    
    """
    Crea un nuevo registro de alquiler en la estructura XML. 
    Se debe buscar un coche para alquilarlo.

    Args:
        alquileresRaiz (Element): El elemento raiz que contiene la informacion de los alquileres.
        cochesRaiz (Element): El elemento raiz que contiene la informacion de los coches.

    Returns:
        None
    """
    
    if(len(cochesRaiz.findall('Coche'))>0):
    
        fin = False
        while(not fin):
            #se declara aqui en caso que el usuario quiera crear otro alquiler, y los anteriores datos no fueron correctos
            correcto = True

            #Como los alquileres no se pueden eliminar, el id de un alquiler siempre corresponde a su posicion en el fichero + 1
            alquiler = ET.SubElement(alquileresRaiz, 'Alquiler', {'id':str(len(alquileresRaiz.findall('Alquiler'))+1)})
            print("\n--- Creando nuevo alquiler ---\n")  
            
            #No hace falta comprobar 'correcto', aqui siempre sera True
            print("--- Buscando coche para asignar ID ---")
            correcto, coche = obtenerIdCoche(cochesRaiz, alquiler)

            if(correcto):
                correcto = obtenerDni(alquiler)
                
            if(correcto):
                correcto, fechaInicio = obtenerFechaInicio(alquiler)
    
            if(correcto):
                correcto = obtenerFechaFinAlquiler(alquiler, fechaInicio)
                
            if(correcto):
                correcto = obtenerKmInicial(alquiler)

            #Si se ha creado toto correctamente y confirmas la creacion
            if(correcto and confirmacion("Estas seguro que deseas crear el alquiler? (S/N): ")):
                    #Si se da de alta el alquiler, cambiamos valor del vehiculo a alquilado
                    coche.find('Estado').text="alquilado"
                    print("Alta alquiler realizada correctamente")        
            else:
                alquileresRaiz.remove(alquiler)
                print("Alta del alquiler no realizada")

            if(not confirmacion("Desea introducir otro alquiler? (S/N): ")):
                fin = True
    else:
        print("No hay coches guardados. No se puede crear un alquiler sin un coche.")

def obtenerIdCoche(cochesRaiz, alquiler):
    
    """
    Obtiene el ID de un coche para ser asignado a un alquiler.

    Args:
        cochesRaiz (Element): El elemento raiz que contiene la informacion de los coches.
        alquiler (Element): El elemento de alquiler al que se asignara el ID del coche.

    Returns:
        Tuple[bool, Element]: Una tupla donde el primer elemento indica si la operacion fue exitosa y el segundo
        elemento es el coche seleccionado. Si la operacion no fue exitosa, el segundo elemento es None.
    """
    
    coche = buscarCoche(cochesRaiz, True)
    if(coche is not None): 
        if(coche.find('Estado').text=="disponible"):
            id = coche.get('id')
            idCocheXML = ET.SubElement(alquiler, 'IDCoche')
            idCocheXML.text = id
            correcto = True
        else:
            correcto = False
            print("Este coche no esta disponible para alquilar")
    else:
        correcto = False
        print("Busqueda de coche no realizada")

    return correcto, coche
        
      
def obtenerDni(alquiler):  
    
    """
    Obtiene y valida el DNI para ser asignado a un alquiler.

    Args:
        alquiler (Element): El elemento de alquiler al que se asignara el DNI.

    Returns:
        bool: True si el DNI es valido y se ha asignado correctamente, False en caso contrario.
    """
    
    intentos = 3
    correcto = False
    
    while(not correcto and intentos>0):
        dni = input("\nIntroduce el DNI del propietario del alquiler: ").strip().upper()
        if(len(dni) == 9 and dni[:8].isdigit() and dni[8].isalpha):
            dniXML = ET.SubElement(alquiler, 'DNI')
            dniXML.text = dni
            correcto = True
            print("DNI valido")
        else:
            print("El formato del DNI no es valido")
        intentos -= 1
    return correcto
        

def obtenerFechaInicio(alquiler):
    
    """
    Obtiene y valida la fecha de inicio del alquiler.

    Args:
        alquiler (Element): El elemento de alquiler al que se asignara la fecha de inicio.

    Returns:
        Tuple[bool, datetime]: Una tupla donde el primer elemento indica si la operacion fue exitosa y el segundo
        elemento es la fecha de inicio del alquiler. Si la operacion no fue exitosa, el segundo elemento es None.
    """
    
    intentos = 3
    correcto = False

    while(not correcto and intentos>0):
        fechaInicio = None
        print("Fecha de inicio alquiler")
        try:
            dia = int(input("Introduce el día: "))
            mes = int(input("Introduce el mes (numerico): "))
            anio = int(input("Introduce el año: "))
            
            # Formar la fecha y verificar su validez
            fechaInput = f"{dia:02d}/{mes:02d}/{anio:04d}"
            fechaInicio = datetime.strptime(fechaInput, '%d/%m/%Y')
            fechaFormateada = fechaInicio.strftime('%d/%m/%Y')
                
            if(fechaInput==fechaFormateada):#Si los dias y los meses han sido validos para una fecha
                fechaInicioXML = ET.SubElement(alquiler, 'FechaInicioAlquiler')
                fechaInicioXML.text = str(fechaInput)
                correcto = True
                print("Fecha de inicio alquiler valida")
            else:
                print("Formato Fecha inicio alquiler no valido")
        except ValueError:
            print("Fecha no valida")
        intentos -= 1
    
    return correcto, fechaInicio
    

def obtenerFechaFinAlquiler(alquiler, fechaInicio):
    
    """
    Obtiene y valida la fecha de finalizacion del alquiler.

    Args:
        alquiler (Element): El elemento de alquiler al que se asignara la fecha de finalizacion.
        fechaInicio (datetime): La fecha de inicio del alquiler.

    Returns:
        bool: True si la fecha de finalizacion es valida y se ha asignado correctamente, False en caso contrario.
    """
    
    intentos = 3
    correcto = False

    while(not correcto and intentos>0):
        print("Fecha de finalizacion alquiler: ")
        try:
            dia = int(input("Introduce el día: "))
            mes = int(input("Introduce el mes (numerico): "))
            anio = int(input("Introduce el año: "))
            
            # Formar la fecha y verificar su validez
            fechaInput = f"{dia:02d}/{mes:02d}/{anio:04d}"
            fechaFin = datetime.strptime(fechaInput, '%d/%m/%Y')
            fechaFormateada = fechaFin.strftime('%d/%m/%Y')
            if (fechaInput == fechaFormateada and fechaInicio < fechaFin):
                fechaFinXML = ET.SubElement(alquiler, 'FechaFinalizacionAlquiler')
                fechaFinXML.text = str(fechaInput)
                correcto = True
                print("Fecha de finalización de alquiler válida")
            elif (fechaInput != fechaFormateada):
                print("La fecha de finalización de alquiler no coincide con el formato esperado.")
            else:
                print("La fecha de finalización de alquiler no puede ser anterior a que la fecha de inicio de alquiler.") 
        except ValueError:
            print("Fecha no valida")
        intentos -= 1
    
    return correcto
                 
     
def obtenerKmInicial(alquiler):

    """
    Obtiene y valida el kilometraje inicial del coche para el alquiler.

    Args:
        alquiler (Element): El elemento de alquiler al que se asignars el kilometraje inicial.

    Returns:
        bool: True si el kilometraje inicial es valido y se ha asignado correctamente, False en caso contrario.
    """

    intentos = 3
    correcto = False

    while(not correcto and intentos>0):
        kmInicial = input("Introduce el km inicial del coche - (km): ")
        if(kmInicial.isdigit()):
            kmXML = ET.SubElement(alquiler, 'KmInicialAlquiler')
            kmXML.text = kmInicial
            correcto = True
            print("Km inicial introducido correctamente")
        else:
            print("Km debe ser un numero")
        intentos -= 1
    
    return correcto  
                     
def modificarAlquiler(alquileresRaiz):
    
    """
    Modifica las fechas de inicio o finalizacion de un alquiler existente. 
    Para conseguir el alquiler se usa la funcion buscarAlquileres.

    Args:
        alquileresRaiz (Element): El elemento raiz que contiene todos los alquileres.

    Returns:
        None
    """
    
    print("--- Modificacion Alquiler ---")
    alquiler = busquedaAlquiler(alquileresRaiz)
    if(alquiler is not None):
        finModificar = False
        while(not finModificar):
            
            #cogemos fechas del alquiler para comparar
            fechaInicio = alquiler.find('FechaInicioAlquiler').text.split("/")
            fechaInputInicio = f"{int(fechaInicio[0]):02d}/{int(fechaInicio[1]):02d}/{int(fechaInicio[2]):04d}"
            fechaInicioFormateDate= datetime.strptime(fechaInputInicio, '%d/%m/%Y')
        
            fechaFinalizacion = alquiler.find('FechaFinalizacionAlquiler').text.split("/")
            fechaInputFinalizacion = f"{int(fechaFinalizacion[0]):02d}/{int(fechaFinalizacion[1]):02d}/{int(fechaFinalizacion[2]):04d}"
            fechaFinalizacionFormatoDate= datetime.strptime(fechaInputFinalizacion, '%d/%m/%Y')
                
            print("Elige una opcion para modificar el alquiler: ")
            print("1 - Fecha de inicio alquiler")
            print("2 - Fecha de finalizacion alquiler")
            opcion = input("Introduce la opcion a modificar: ")
            
            if(opcion== "1"):
                
                dia = int(input("Introduce el dia: "))
                mes = int(input("Introduce el mes (numerico): "))
                anio = int(input("Introduce el anio: "))
                
                # Formar la fecha y verificar su validez
                fechaInicioNueva= f"{dia:02d}/{mes:02d}/{anio:04d}"
                fechaInicioNuevaDate = datetime.strptime(fechaInicioNueva, '%d/%m/%Y')
                fechaInicioNuevaFormato = fechaInicioNuevaDate.strftime('%d/%m/%Y')
                
                #que tenga formato y que la fecha finalizacion sea mayor a la nueva de inicio
                if(fechaInicioNueva==fechaInicioNuevaFormato and fechaFinalizacionFormatoDate>fechaInicioNuevaDate):
                    alquiler.find('FechaInicioAlquiler').text = fechaInicioNueva
                    print("Fecha de inicio introducida correctamente")
                elif(fechaInicioNueva!=fechaInicioNuevaFormato):
                    print("Formato de fecha introducido no valido")
                else:
                    print("La fecha de inicio de alquiler no puede ser anterior a que la fecha de finalizacion")
                    
            elif(opcion== "2"):
                
                dia = int(input("Introduce el día: "))
                mes = int(input("Introduce el mes (numerico): "))
                anio = int(input("Introduce el año: "))
                
                # Formar la fecha y verificar su validez
                fechaFinNueva= f"{dia:02d}/{mes:02d}/{anio:04d}"
                fechaFinNuevaDate = datetime.strptime(fechaFinNueva, '%d/%m/%Y')
                fechaFinNuevaFormato = fechaFinNuevaDate.strftime('%d/%m/%Y')
                
                #que tenga formato y que la fecha finalizacion sea mayor a la nueva de inicio
                if(fechaFinNueva==fechaFinNuevaFormato and fechaInicioFormateDate<fechaFinNuevaDate):
                    alquiler.find('FechaFinalizacionAlquiler').text = fechaFinNueva
                    print("Fecha de finalización introducida correctamente")
                elif(fechaFinNueva!=fechaFinNuevaFormato):
                    print("Formato de fecha introducido no valido")
                else:
                    print("La fecha de finalizacion de alquiler debe ser mayor que la fecha de inicio")
                    
            elif(opcion== "0"):
                finModificar = True
                print("Fin modificacion")
            else:
                print("Opcion no valida")
                
            if(not finModificar):
                 if(not confirmacion("Quieres modificar algo mas de este alquiler? S/N")):
                     finModificar = True
                     print("\n--- Has terminado de modificar el alquiler actual ---")   

def busquedaAlquiler(alquileresRaiz):
    
    """
    Busca un alquiler en la lista de alquileres por el DNI del cliente.

    Args:
        alquileresRaiz (Element): El elemento raiz que contiene todos los alquileres.

    Returns:
        Element: El elemento alquiler correspondiente al DNI proporcionado, o None si no se encontro ningún alquiler.
    """
    
    alquiler = None
    if(len(alquileresRaiz.findall('Alquiler')) > 0):
        dni = input("Introduce el DNI del propietario del alquiler: ").strip().upper()
        #buscamos los alquiler con el Dni introducido, obviando los ya entregados
        alquileres = [alquiler for alquiler in alquileresRaiz if alquiler.find('DNI').text == dni and alquiler.find('TarifaFinal') is None]
        
        #si hay alquiler con ese dni entramos a mostrar resultado
        if(alquileres):
            print("--- Resultado ---")
            for alquiler in alquileres:
                id = alquiler.get('id')
                print("Alquiler ID: " + id)
                for atributo in alquiler:
                    print("\t", atributo.tag,":", atributo.text)
            
            #importante hay que extraer el elemento de la lista, para pasarlo por parametro como 1 solo elemento
            if(len(alquileres) > 1):
                finIdAlquiler = False
                while(not finIdAlquiler):
                    idAlquiler = input("Introduce id del alquiler a elegir")
                    alquileresId = [alquiler for alquiler in alquileres if alquiler.get('id') == idAlquiler]
                    if(alquileresId is not None):
                        alquiler = alquileresId[0]
                        finIdAlquiler = True
                    else:
                        print("Introduce un identificador de alquiler valido")
            else:
                alquiler = alquileres[0]
        else:
            print("No se encontraron alquileres con el DNI introducido")
    else:
        print("No hay alquileres registrados")
            
    return alquiler

def devolverCoche(alquileresRaiz, cochesRaiz):
    
    """
    Realiza el proceso para registrar la devolucion de un coche despues de un alquiler.

    Args:
        alquileresRaiz (Element): El elemento raiz que contiene todos los alquileres.
        cochesRaiz (Element): El elemento raiz que contiene todos los coches.

    Returns:
        None
    """
    
    print("--- Devolviendo Coche ---")
    alquiler = busquedaAlquiler(alquileresRaiz)
        #O se hace todo o nada
    if(alquiler is not None):
        try:
            #Obtengo datos kmfinal y fechaDevolucion
            alquiler, correcto = obtenerFechaDevolucion(alquiler)
            
            if(correcto):
                alquiler, correcto = obtenerKmFinal(alquiler)
                
                if(correcto):   
                    #Obtengo fechas para el calculo tarifa 
                    fechaInicio = alquiler.find('FechaInicioAlquiler').text
                    fechaDevolucion = alquiler.find('FechaDevolucionAlquiler').text
                    #para comparar, necesario formato datetime
                    fechaFromateadaInicio = datetime.strptime(fechaInicio, '%d/%m/%Y')
                    fechaFormateadaDevo = datetime.strptime(fechaDevolucion, '%d/%m/%Y')
                    
                    #calculo numero dias de diferencia entre fecha Inicio y Devolucion
                    diasDiferencia = (fechaFormateadaDevo - fechaFromateadaInicio).days
                    
                    #obtengo coche por ID_Coche de alquiler para recoger su tarifa diaria
                    idCocheAlquiler = alquiler.find('IDCoche').text
                    coche = cochesRaiz.find(f"Coche[@id='{idCocheAlquiler}']")
                    
                    #dias diferencia por la tarifa que tenga dicho coche + recargo (si hay)
                    tarifaFinal = diasDiferencia*int(coche.find('TarifaPorDia').text)
                    if(alquiler.find('Recargo') is not None):
                        tarifaFinal = tarifaFinal + int(alquiler.find('Recargo').text)
                    
                    tarifaFinalXML = ET.SubElement(alquiler, 'TarifaFinal')
                    tarifaFinalXML.text = str(tarifaFinal)
                    print("Tarifa final calculada correctamente.")
                    
                    #cambio estado a disponible al final, cuando se ha creado la tarifa
                    coche.find('Estado').text="disponible" 
                    print("La tarifa final del coche ha sido ", alquiler.find('TarifaFinal').text, "€.")
                    if(alquiler.find('Recargo') is not None):
                        print("Incluido el recargo de", alquiler.find('Recargo').text, "€ por devolver el coche despues de la fecha de finalizacion")
                #si se ha introducido la fecha pero no los km, destruye el objeto y sale
                else:
                    alquiler.remove(alquiler.find('FechaDevolucionAlquiler'))
                    print("El coche no ha sido devuelto. Fin de devolucion de coche")

            else:
                print("El coche no ha sido devuelto. Fin de devolucion de coche")
    
        except Exception:
            # no borro tarifa final porque si se pone se crearia todo correctamente
            if(alquiler.find('FechaDevolucionAlquiler') is not None):
                alquiler.remove(alquiler.find('FechaDevolucionAlquiler'))
            if(alquiler.find('KmFinalAlquiler') is not None): 
                alquiler.remove(alquiler.find('KmFinalAlquiler'))
            if(alquiler.find('Recargo') is not None):
                alquiler.remove(alquiler.find('Recargo'))  
            print("Ocurrió un error en el proceso de devolucion de coche")


def obtenerFechaDevolucion(alquiler):
    
    """
    Solicita y valida la fecha de devolucion para un alquiler.

    Args:
        alquiler (Element): El elemento XML que representa el alquiler.

    Returns:
        Element: El elemento XML actualizado con la fecha de devolucion.
    """
    
    correcto = False
    intentos = 3
    while(not correcto and intentos>0):
        print("Fecha devolucion alquiler: ")
        try:

            dia = int(input("Introduce el día: "))
            mes = int(input("Introduce el mes (numerico): "))
            anio = int(input("Introduce el año: "))
            
            # Formar la fecha y verificar su validez
            fechaInput = f"{dia:02d}/{mes:02d}/{anio:04d}"
            fechaDevolucion = datetime.strptime(fechaInput, '%d/%m/%Y')
            fecha_formateada = fechaDevolucion.strftime('%d/%m/%Y')
            
            #divido la fechaInicioaAlquiler para formartearla a fecha y comparar
            fechaI = alquiler.find('FechaInicioAlquiler').text.split('/')
            #creamos formato dd/mm/aaaa
            fechaInicio = f"{int(fechaI[0]):02d}/{int(fechaI[1]):02d}/{int(fechaI[2]):04d}"
            #y lo hacemos datatime para poder comparar fechas
            fechaInicioFormato = datetime.strptime(fechaInicio, '%d/%m/%Y')
            
            #misma funcion que fechaInicio
            fechaF = alquiler.find('FechaFinalizacionAlquiler').text.split('/')
            fechaFinali = f"{int(fechaF[0]):02d}/{int(fechaF[1]):02d}/{int(fechaF[2]):04d}"
            fechaFinalizacionFormato = datetime.strptime(fechaFinali, '%d/%m/%Y')
            
            #la fecha devolucion no puede ser menor que la fecha de inicio de alquiler
            if fechaInput == fecha_formateada and fechaInicioFormato < fechaDevolucion:
                
                fechaDevoXML = ET.SubElement(alquiler, 'FechaDevolucionAlquiler')
                fechaDevoXML.text = str(fechaInput)
                
                #calculo recargo aqui para luego aplicar a tarifa final en caso que haya
                if(fechaFinalizacionFormato < fechaDevolucion):
                    recargoXML = ET.SubElement(alquiler, 'Recargo')
                    recargoXML.text = "150"
                    
                correcto = True
                print("Fecha devolucion alquiler válida")
            else:
                if fechaInput != fecha_formateada:
                    print("La fecha devolucion alquiler no coincide con el formato esperado.")
                else:
                    print("La fecha devolucion alquiler no puede ser menor que la fecha de inicio de alquiler.") 
        
        except ValueError:
            print("Debes introducir numeros en la fecha")
        except Exception:
            print("Ocurrió un error en el proceso de devolucion de coche.")
        intentos -= 1
            
    return alquiler, correcto

def obtenerKmFinal(alquiler):
    
    """
    Solicita y valida la cantidad de kilometros al final del alquiler.

    Args:
        alquiler (Element): El elemento XML que representa el alquiler.

    Returns:
        Element: El elemento XML actualizado con la cantidad de kilometros finales.
    """
    
    correcto = False
    intentos = 3
    kmInicial = alquiler.find('KmInicialAlquiler').text
    while(not correcto and intentos>0):
        kmFinal = input("Introduce km final alquiler - (km): ")
        if(kmFinal.isdigit()):
            if(int(kmFinal) > int(kmInicial)):
                kmFinalXML = ET.SubElement(alquiler, 'KmFinalAlquiler')
                kmFinalXML.text = kmFinal
                correcto = True
                print("KmFinalAlquiler introducido correctamente")
            else:
                print("Los kilometros finales no se pueden ser menores que los kilometros iniciales")
        else:
            print("Km debe ser un numero")
        intentos -= 1
            
    return alquiler, correcto

def consultaAlquiler(alquileresRaiz, cochesRaiz):
    
    """
    Permite al usuario consultar informacion sobre alquileres.

    Muestra un menu de opciones que incluye la consulta de todos los alquileres,
    la consulta de alquileres por matricula de coche y la consulta de alquileres por DNI del cliente.

    Args:
        alquileresRaiz (Element): El elemento XML que contiene la informacion de los alquileres.
        cochesRaiz (Element): El elemento XML que contiene la informacion de los coches.

    Returns:
        None
    """
    
    fin = False 
    while(fin == False):
        print("\n---- Menu Consulta ----\n")
        print("Elige una opcion")
        print("1 - Consultar todos los alquileres")
        print("2 - Consultar alquiler por matricula coche")
        print("3 - Consultar alquiler por Dni")
        print("0 - Salir")
        opcion = input("Elige una opcion: ")
        #Mostramos todos los alquileres
        if(opcion == "1"):

            for alquiler in alquileresRaiz.findall('Alquiler'):
                idAlquiler = alquiler.get('id')
                print("Alquiler id: ",idAlquiler)
                for elemento2 in alquiler:
                    print("\t"+elemento2.tag, ":",elemento2.text)

        #Moatramos alquiler por matricula coche            
        elif(opcion == "2"):
            #se pone en mayus porque las letras de la matricual del coche estan en mayus
            matricula = input("Introduce la matricula del coche: ").strip().upper()
            #itera los coches y busca la matricula introducida
            cochesMatricula = [coche for coche in cochesRaiz.findall('Coche') if coche.find('Matricula').text == matricula]

            if(cochesMatricula):
                for alquiler in alquileresRaiz:
                    idCoche = alquiler.find('IDCoche').text
                    #texto idCoche busca textoAtributo id coche
                    if(idCoche in [coche.get('id') for coche in cochesMatricula]):
                        print("Alquiler id: ",idCoche)
                        for elemento2 in alquiler:
                            print("\t"+elemento2.tag, ":",elemento2.text)

            else:
                print("No hay alquileres con la matricula introducida")

        #Mostramos alquiler por DNI cliente        
        elif(opcion == "3"):
            dni = input("Introduce el DNI del cliente: ").strip().upper()
            alquiler
            for alquiler in alquileresRaiz: 
                idAlquiler = alquiler.get('id')
                if(alquiler.find('DNI').text == dni):
                    print("Alquiler id: ",idAlquiler)
                    for elemento2 in alquiler:
                        print("\t"+elemento2.tag, ":",elemento2.text)

        elif(opcion == "0"):
            fin = True
            print("Vuelta Menu Alquiler")
        else:
            print("Opcion no valida")

def menuAlquiler(): 
   
    """
    Funcion principal que gestiona el menu de operaciones relacionadas con los alquileres.
    La funcion interactua con el usuario y realiza acciones en funcion de la opcion seleccionada.
    Al salir del menu se guardan los alquileres y los coches en los ficheros.

    Args:
        None

    Returns:
        None
    """
    
    #Cogemos los archivos en caso que existan
    try:
        alquileresRaiz = ET.parse("Comercio\\Alquileres\\alquileres.xml").getroot()
    except:
        print("No existe el documento alquileres, lo creamos")
        alquileresRaiz = ET.Element('Alquileres')

    try:
        cochesRaiz = ET.parse("Comercio\Coches\\coches.xml").getroot()
    except:
        print("No existe el documento coches")
        cochesRaiz = Element('Coches')

    
    fin = False 
    while(fin == False):
        print("\n---- Menu Alquiler ----\n")
        print("1 - Crear alquiler")
        print("2 - Modificar alquiler")
        print("3 - Consultar")
        print("4 - Devolver Coche")
        print("0 - Salir")
        opcion = input("Elige una opcion: ")
        
        if(opcion == "1"):
            crearAlquiler(alquileresRaiz, cochesRaiz)
        elif(opcion == "2"):
            modificarAlquiler(alquileresRaiz)
        elif(opcion == "3"):
            consultaAlquiler(alquileresRaiz, cochesRaiz)
        elif(opcion == "4"):
            devolverCoche(alquileresRaiz, cochesRaiz)
        elif(opcion == "0"):
            #Se gurdan los alquileres y los coches tambien por los posibles cambios del elemento 'Estado' del coche
            guardarCoches(cochesRaiz)
            guardarAlquiler(alquileresRaiz)
            fin = True
            print("Vuelta Menu Principal")
        else:
            print("Opcion no valida")