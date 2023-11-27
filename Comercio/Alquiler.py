import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from Coche import buscarCoche
from Coche import guardarCoches
from Utilidades import confirmacion
from datetime import datetime

def guardarAlquiler(alquileresRaiz):
    
    file = open("Comercio_XML\\Comercio\\Alquileres\\alquileres.xml", "w")
    archivoDefinido = prettify(alquileresRaiz)
    
    lineas = archivoDefinido.split("\n")
    textoCorreecto=""
    
    for i in lineas:
        if i.strip()!="":
            textoCorreecto=textoCorreecto+str(i)+"\n"
    
    file.writelines(textoCorreecto)
    file.close()

def prettify(elem):
    
    from xml.etree import ElementTree
    from xml.dom import minidom
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def crearAlquiler(alquileresRaiz, raizDocumentoCoche):
    
    if(len(raizDocumentoCoche.findall('Coche'))>0):
    
        fin = False
        while(not fin):
            #se declara aqui en caso que el usuario quiera crear otro alquiler, y los anteriores datos no fueron correctos
            correcto = True

            alquiler = ET.SubElement(alquileresRaiz, 'Alquiler', {'id':str(len(alquileresRaiz.findall('Alquiler'))+1)})
            print("\n--- Creando nuevo alquiler ---\n")  
            
            #No hace falta comprobar 'correcto', aqui siempre sera True
            print("--- Buscando coche para asignar ID ---\n")
            correcto, coche = obtenerIdCoche(raizDocumentoCoche, alquiler)

            if(correcto):
                correcto = obtenerDni(correcto, alquiler)
                
            if(correcto):
                
                correcto, fechaInicio = obtenerFechaInicio(correcto, alquiler)
    
            if(correcto):

                correcto = obtenerFechaFinAlquiler(correcto, alquiler, fechaInicio)
                
            if(correcto):
                
                correcto = obtenerKmInicial(correcto, alquiler)

                if(correcto):
                    #Si se da de alta el alquiler, cambiamos valor del vehiculo a alquilado
                    coche.find('Estado').text="alquilado"
                    if(not confirmacion("Alquiler realizado correctamente. Desea introducir otro alquiler? S/N: ")):
                        fin = True                    
                
                else:
                    if(not confirmacion("Alquiler no realizado con exito. Desea introducir otro alquiler? S/N: ")):
                        fin = True
            else:
                fin = True

def obtenerIdCoche(raizDocumentoCoche, alquiler): 
    coche = buscarCoche(raizDocumentoCoche, True)
    if(coche is not None): 
        if(coche.find('Estado').text=="disponible"):
            id = coche.get('id')
            idNum = int(id)
            idAlquilerXML = ET.SubElement(alquiler, 'IDCoche')
            idAlquilerXML.text = str(idNum)
            correcto = True
        else:
            correcto = False
            print("El coche debe estar disponible")
    else:
        correcto = False
        print("Busqueda de coche no realizada")

    return correcto, coche
        
      
def obtenerDni(correcto, alquiler):  
    
    intentos = 3
    correcto = False
    
    while(not correcto and intentos>0):
        dni = input("\nIntroduce el DNI del alquiler: ").strip().upper()
        if(dni.isalnum and len(dni) == 9):
            numero = dni[:8]
            letras = dni[8]
            if(numero.isdigit() and letras.isalpha):
                dniXML = ET.SubElement(alquiler, 'DNI')
                dniXML.text = str(dni)
                correcto = True
                print("DNI valido")
            else:
                print("Formato DNI no valido")
        else:
            print("DNI no valido")
    return correcto
        

def obtenerFechaInicio(correcto, alquiler):
    
    intentos = 3
    correcto = False

    while(not correcto and intentos>0):
        print("Fecha de inicio alquiler")
        try:
            dia = int(input("Introduce el día: "))
            mes = int(input("Introduce el mes (numerico): "))
            anio = int(input("Introduce el año: "))
            
            # Formar la fecha y verificar su validez
            fechaInicio = f"{dia:02d}/{mes:02d}/{anio}"
            fecha = datetime.strptime(fechaInicio, '%d/%m/%Y')
            fecha_formateada = fecha.strftime('%d/%m/%Y')
                
            if(fechaInicio==fecha_formateada):
                fechaInicioXML = ET.SubElement(alquiler, 'FechaInicioAlquiler')
                fechaInicioXML.text = fechaInicio
                correcto = True
                print("Fecha de inicio alquiler valida")
            else:
                print("Formato Fecha inicio alquiler no valido")
        except ValueError:
            print("Fecha no valida")
        intentos = intentos - 1 
    
    return correcto, fechaInicio
    

def obtenerFechaFinAlquiler(correcto, alquiler, fechaInicio):
    
    intentos = 3
    correcto = False

    while(not correcto and intentos>0):
        print("Fecha de finalizacion alquiler: ")
        try:
            dia = int(input("Introduce el día: "))
            mes = int(input("Introduce el mes (numerico): "))
            anio = int(input("Introduce el año: "))
            
            # Formar la fecha y verificar su validez
            fechaFin = f"{dia:02d}/{mes:02d}/{anio}"
            fecha = datetime.strptime(fechaFin, '%d/%m/%Y')
            fecha_formateada = fecha.strftime('%d/%m/%Y')
            fechaInicio_dt = datetime.strptime(fechaInicio, '%d/%m/%Y')
            if fechaFin == fecha_formateada and fechaInicio_dt < fecha:
                fechaFinXML = ET.SubElement(alquiler, 'FechaFinalizacionAlquiler')
                fechaFinXML.text = fechaFin
                correcto = True
                print("Fecha de finalización de alquiler válida")
            else:
                if fechaFin != fecha_formateada:
                    print("La fecha de finalización de alquiler no coincide con el formato esperado.")
                else:
                    print("La fecha de finalización de alquiler no puede ser menor que la fecha de inicio de alquiler.") 
        
        except ValueError:
            print("Fecha no valida")
        intentos = intentos - 1
    
    return correcto
                 
     
def obtenerKmInicial(correcto, alquiler):

    intentos = 3
    correcto = False

    while(not correcto and intentos>0):
        kmInicial = input("Introduce el km inicial alquiler - (km): ")
        if(kmInicial.isdigit()):
            kmXML = ET.SubElement(alquiler, 'KmInicialAlquiler')
            kmXML.text = str(kmInicial)
            correcto = True
            print("Km_Inicial introducido correctamente")
        else:
            print("Km debe ser un numero")
        intentos = intentos - 1
    
    return correcto  
                     
def modificarAlquiler(): #TODO
    print("Modificar Alquiler")

def devolverCoche(alquileresRaiz, raizDocumentoCoche):
    print("--- Devolviendo Coche ---")
    dni = input("Introduce el DNI del alquiler: ").strip().upper()
    #buscamos los alquiler con el Dni introducido, obviando los ya entregados
    alquiler = [alquiler for alquiler in alquileresRaiz if alquiler.find('DNI').text == dni and alquiler.find('TarifaFinal') is None]
    
    if(alquiler):
        print("--- Resultado ---")
        for elemento in alquiler:
            id = elemento.get('id')
            print("Alquiler ID: " + id)
            for elementos2 in elemento:
                print("\t", elementos2.tag,":", elementos2.text)
        
        #importante hay que extraer el elemento de la lista, para pasarlo por parametro como 1 solo elemento
        if(len(alquiler) > 1):
            fin = False
            while(not fin):
                posicion = input("Introduce posicion del alquiler a elegir")
                if(posicion.isdigit() and 0<int(posicion) <= len(alquiler)):
                    alquiler=alquiler[int(posicion)-1]
                    fin = True
                else:
                    print("Posicion no valida")
        else:
            alquiler = alquiler[0]      
        #O se hace todo o nada
        try:
            #Obtengo datos kmfinal y fechaDevolucion
            alquiler = obtenerFechaDevolucion(alquiler)
            alquiler = obtenerKmFinal(alquiler)
            
            #Obtengo fechas para el calculo tarifa 
            fechaInicio = alquiler.find('FechaInicioAlquiler').text
            fechaDevolucion = alquiler.find('FechaDevolucionAlquiler').text
            fechaFromateadaInicio = datetime.strptime(fechaInicio, '%d/%m/%Y')
            fechaFormateadaDevo = datetime.strptime(fechaDevolucion, '%d/%m/%Y')
            
            #calculo numero dias de diferencia entre fecha Inicio y Devolucion
            diasDiferencia = (fechaFormateadaDevo - fechaFromateadaInicio).days
            
            #obtengo coche por ID_Coche de alquiler para recoger su tarifa diaria
            idCocheAlquiler = alquiler.find('IDCoche').text
            coche = raizDocumentoCoche.find(f"Coche[@id='{idCocheAlquiler}']")
            
            #dias diferencia por la tarifa que tenga dicho coche + recargo (si hay)
            tarifaFinal = diasDiferencia*int(coche.find('TarifaPorDia').text)
            tarifaFinal = tarifaFinal + int(alquiler.find('Recargo').text)
            
            tarifaFinalXML = ET.SubElement(alquiler, 'TarifaFinal')
            tarifaFinalXML.text = str(tarifaFinal)  
            
        except ValueError as e:
            print("Error al convertir fechas")
        except Exception as e:
            print("Ocurrió un error en el proceso de devolucion de coche")
        else:
            print("Tarifa final calculada correctamente.")
    else:
        print("No hay alquiler con el DNI introducido")

def obtenerFechaDevolucion(alquiler):
    correcto = False
    while(not correcto):
        print("Fecha devolucion alquiler: ")
        try:

            dia = int(input("Introduce el día: "))
            mes = int(input("Introduce el mes (numerico): "))
            anio = int(input("Introduce el año: "))
            
            # Formar la fecha y verificar su validez
            fechaDevolucion = f"{dia:02d}/{mes:02d}/{anio}"
            fechaDandoFormato = datetime.strptime(fechaDevolucion, '%d/%m/%Y')
            fecha_formateada = fechaDandoFormato.strftime('%d/%m/%Y')
            
            #divido la fechaInicioaAlquiler para formartearla a fecha y comparar
            fechaI = alquiler.find('FechaInicioAlquiler').text.split('/')
            fechaInicioConFormato = f"{int(fechaI[0]):02d}/{int(fechaI[1]):02d}/{int(fechaI[2])}"
            
            #misma funcion que fechaInicio
            fechaF = alquiler.find('FechaFinalizacionAlquiler').text.split('/')
            fechaFinalizacionConFormato = f"{int(fechaF[0]):02d}/{int(fechaF[1]):02d}/{int(fechaF[2])}"
            
            #la fecha devolucion no puede ser menor que la fecha de inicio de alquiler
            if fechaDevolucion == fecha_formateada and fechaInicioConFormato < fechaDevolucion:
                
                fechaDevoXML = ET.SubElement(alquiler, 'FechaDevolucionAlquiler')
                fechaDevoXML.text = fechaDevolucion
                
                #calculo recargo aqui para luego aplicar a tarifa final en caso que haya
                if(fechaFinalizacionConFormato < fechaDevolucion):
                    recargoXML = ET.SubElement(alquiler, 'Recargo')
                    recargoXML.text = "150"
                else:
                    recargoXML = ET.SubElement(alquiler, 'Recargo')
                    recargoXML.text = "0"
                    

                correcto = True
                print("Fecha devolucion alquiler válida")
            else:
                if fechaDevolucion != fecha_formateada:
                    print("La fecha devolucion alquiler no coincide con el formato esperado.")
                else:
                    print("La fecha devolucion alquiler no puede ser menor que la fecha de inicio de alquiler.") 
        
        except ValueError:
            print("Fecha no valida")
            
    return alquiler

def obtenerKmFinal(alquiler):
    correcto = False
    while(not correcto):
        kmFinal = input("Introduce km final alquiler - (km): ")
        if(kmFinal.isdigit()):
            kmFinalXML = ET.SubElement(alquiler, 'KmFinalAlquiler')
            kmFinalXML.text = str(kmFinal)
            correcto = True
            print("KmFinalAlquiler introducido correctamente")
        else:
            print("Km debe ser un numero")
            
    return alquiler

def consultaAlquiler(alquileresRaiz, raizDocumentoCoche):
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
            cochesMatricula = [coche for coche in raizDocumentoCoche.findall('Coche') if coche.find('Matricula').text == matricula]

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
   
   #Cogemos los archivos en caso que existan
    try:
        alquileresRaiz = ET.parse("Comercio_XML\\Comercio\\Alquileres\\alquileres.xml").getroot()
    except:
        print("No existe el documento alquileres, lo creamos")
        alquileresRaiz = ET.Element('Alquileres')

    try:
        raizDocumentoCoche = ET.parse("Comercio_XML\\Comercio\Coches\\coches.xml").getroot()
    except:
        print("No existe el documento coches")
        raizDocumentoCoche = Element('Coches')

    
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
            crearAlquiler(alquileresRaiz, raizDocumentoCoche)
        elif(opcion == "2"):
            modificarAlquiler()
        elif(opcion == "3"):
            consultaAlquiler(alquileresRaiz, raizDocumentoCoche)
        elif(opcion == "4"):
            devolverCoche(alquileresRaiz, raizDocumentoCoche)
        elif(opcion == "0"):
            #Se gurdan coches tambien por los posibles cambios del elemento 'Estado' del coche
            guardarCoches(raizDocumentoCoche)
            guardarAlquiler(alquileresRaiz)
            fin = True
            print("Vuelta Menu Principal")
        else:
            print("Opcion no valida")