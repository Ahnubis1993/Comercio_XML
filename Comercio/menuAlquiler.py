import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from menuCoche import buscarCoche
from datetime import datetime

def guardar(documento):
    
    file = open("Alquileres\\alquileres.xml", "w")
    archivoDefinido = prettify(documento)
    
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

def guardarAlquiler(alquileresRaiz, cochesRaiz):
    print("--- Crear Alquiler ---\n")
    fin = False
    while(not fin):
        correcto = False
        intentos = 3

        while(intentos>0 and not correcto):
            # 1 Subelemento Alquiler
            alquiler = ET.SubElement(alquileresRaiz, 'Alquiler')
            # 1.1 ID_Alquiler se hace automaticamente calculando la cantidad de alquileres y asignando el ulitmo +1
            idAlquilerXML = ET.SubElement(alquiler, 'ID_Alquiler')
            idAlquilerXML.text = str(len(alquileresRaiz.findall('alquiler'))+1)
            print("* Creando nuevo alquiler *")
            # 1.2 ID_Coche, llama al metodo buqueda de coche y extraemos el id del mismo
            coche = buscarCoche(cochesRaiz)
            if(coche is not None):
                id = coche.get('id')
                idNum = int(id)
                idAlquilerXML = ET.SubElement(alquiler, 'ID_Coche')
                idAlquilerXML.text = str(idNum)
            
            # 1.3 DN de la persona que alquila
            dni = input("Introduce el DNI del alquiler")
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


            if(correcto):
                
                intentos = 3
                correcto = False
                
                while(not correcto and intentos>0):
                    fecha_str = input("Introduce la fecha de inicio alquiler - (dd/mm/aaaa)")
                    try:
                        fecha = datetime.strptime(fecha_str, '%d/%m/%Y')
                        fecha_formateada = fecha.strftime('%Y-%m-%d')
                        if(fecha_str==fecha_formateada):
                            fechaInicioXML = ET.SubElement(alquiler, 'Fecha_Inicio_Alquiler')
                            fechaInicioXML.text = fecha_str
                            print("Fecha de inicio alquiler valida")
                    except ValueError:
                        print("Fecha no valida")
                    intentos = intentos - 1
                    
            if(correcto):
                
                intentos = 3
                correcto = False
                
                while(not correcto and intentos>0):
                    fecha_str = input("Introduce la fecha de finalizacion alquiler - (dd/mm/aaaa)")
                    try:
                        fecha = datetime.strptime(fecha_str, '%d/%m/%Y')
                        fecha_formateada = fecha.strftime('%Y-%m-%d')
                        if(fecha_str==fecha_formateada):
                            fechaFinXML = ET.SubElement(alquiler, 'Fecha_Finalizacion_Alquiler')
                            fechaFinXML.text = fecha_str
                            print("Fecha de finalizacion alquiler valida")
                    except ValueError:
                        print("Fecha no valida")
                    intentos = intentos - 1
                    
            if(correcto):
                
                intentos = 3
                correcto = False
                
                while(not correcto and intentos>0):
                    kmInicial = input("Introduce el km inicial alquiler - (km)")
                    if(kmInicial.isdigit()):
                        kmXML = ET.SubElement(alquiler, 'Km_Inicial_Alquiler')
                        kmXML.text = str(kmInicial)
                        print("Km_Inicial introducido correctamente")
                    else:
                        print("Km debe ser un numero")
        
    
def modificarAlquiler():
    print("Modificar Alquiler")

def devolverCoche():
    print("Devolver Coche")
    
def consultaAlquiler():
    fin = False 
    while(fin == False):
        print("\n---- Menu Consulta ----\n")
        print("Elige una opcion")
        print("1 - Consultar todos los alquileres")
        print("2 - Consultar alquiler por coche")
        print("3 - Consultar alquiler por Dni")
        print("0 - Salir")
        opcion = input("Elige una opcion")
        if(opcion.isdigit()):
            opcion = int(opcion)
            if(opcion == 1):
                print("Consultando todos")
            elif(opcion == 2):
                print("Consultando idCoches")
            elif(opcion == 3):
                print("Consultando Dni")
            elif(opcion == 0):
                fin = True
                print("Vuelta Menu Alquiler")
            else:
                print("Opcion no valida")
        else:
            print("Opcion no valida")

def menuAlquiler(): 
   
    try:
        alquileresRaiz = ET.parse("Alquileres\\alquileres.xml").getroot()
        cochesRaiz = ET.parse("C:\\Users\\34618\\Desktop\\Nuevo Eclipse 2023\\Proyecto_XML\\Comercio_XML\\Comercio\Coches\\coches.xml").getroot()
    except:
        print("No existe el documento, lo creamos")
        alquileresRaiz = Element('Alquileres')
    
    fin = False 
    while(fin == False):
        print("\n---- Menu Alquiler ----\n")
        print("1 - Crear alquiler")
        print("2 - Modificar alquiler")
        print("3 - Consultar")
        print("4 - Devolver Coche")
        print("0 - Salir")
        opcion = input("Elige una opcion")
        
        if(opcion == "1"):
            guardarAlquiler(alquileresRaiz, cochesRaiz)
        elif(opcion == "2"):
            modificarAlquiler()
        elif(opcion == "3"):
            consultaAlquiler()
        elif(opcion == "4"):
            devolverCoche()
        elif(opcion == "0"):
            fin = True
            print("Vuelta Menu Principal")
        else:
            print("Opcion no valida")