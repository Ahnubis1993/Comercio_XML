import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree

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

def guardarAlquiler(alquileresRaiz):
    print("Crear Alquiler")
    
def modificarAlquiler():
    print("Modificar Alquiler")
    
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
    except:
        print("No existe el documento, lo creamos")
        alquileresRaiz = Element('Alquileres')
    
    fin = False 
    while(fin == False):
        print("\n---- Menu Alquiler ----\n")
        print("1 - Guardar alquiler")
        print("2 - Modificar alquiler")
        print("3 - Consultar")
        print("0 - Salir")
        opcion = input("Elige una opcion")
        
        if(opcion.isdigit()):
            opcion = int(opcion)
            if(opcion == 1):
                guardarAlquiler(alquileresRaiz)
            elif(opcion == 2):
                modificarAlquiler()
            elif(opcion == 3):
                consultaAlquiler()
            elif(opcion == 0):
                fin = True
                print("Vuelta Menu Principal")
            else:
                print("Opcion no valida")
        else:
            print("Opcion no valida")