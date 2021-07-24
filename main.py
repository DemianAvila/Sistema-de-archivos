#importa las funciones
from funciones import *

#crea el arbol de archvos de acuerdo al archivo
arbol=insertarSubcarpetas()
#define el padre de cada elemento del arbol (enlaza haci arriba)
establecePadres(arbol)

#imprime las opciones una vez para indicar el funcionamiento del programa
opciones()

#bandera de salida del programa
salida=False
#mientras no se indique la salida pide entrada de comando
while not salida:
    print("Introduce comando:")
    comando=input()
    parametrosComando=comando.split(",")

    if parametrosComando[0]=="salir":
        salida=True

    elif parametrosComando[0]=="opciones":
        opciones()

    elif parametrosComando[0]== "crearF":
        #se pasa nombre ruta y contenido
        if len(parametrosComando)==4:
            crearElemento(arbol, parametrosComando[1], ruta=parametrosComando[2], contenido=parametrosComando[3], archivo=True)
        #solo se pasa nombre y ruta
        elif len(parametrosComando)==3:
            crearElemento(arbol, parametrosComando[1], ruta=parametrosComando[2], archivo=True)
        #solo se pasa nombre
        elif len(parametrosComando)==1:
            crearElemento(arbol, parametrosComando[1], archivo=True)
        else:
            print("Numero de parametros incorrectos")

    elif parametrosComando[0]=="crearD":
        #solo se pasa nombre y ruta
        if len(parametrosComando)==3:
            crearElemento(arbol, parametrosComando[1], ruta=parametrosComando[2], carpeta=True)
        #solo se pasa nombre
        elif len(parametrosComando)==1:
            crearElemento(arbol, parametrosComando[1], carpeta=True)
        else:
            print("Numero de parametros incorrectos")

    elif parametrosComando[0]=="eliminar":
        #se pasa comando y nombre
        if len(parametrosComando)==2:
            eliminaElemento(arbol, parametrosComando[1])
        else:
            print("Numero de parametros incorrectos")

    elif parametrosComando[0]=="nombre":
        #se pasa comando y nombre(o ruta) y nuevo nombre
        if len(parametrosComando)==3:
            cambiarNombre(arbol, parametrosComando[1], parametrosComando[2])
        else:
            print("Numero de parametros incorrectos")

    elif parametrosComando[0]=="copiar":
        #se pasa comando y ruta destino y ruta origen
        if len(parametrosComando)==3:
            copiar(arbol, parametrosComando[1], parametrosComando[2])
        else:
            print("Numero de parametros incorrectos")

    elif parametrosComando[0]=="mover":
        #se pasa comando y nombre
        if len(parametrosComando)==3:
            cortar(arbol, parametrosComando[1], parametrosComando[2])
        else:
            print("Numero de parametros incorrectos")

    elif parametrosComando[0]=="editar":
        #se pasa comando y nombre
        if len(parametrosComando)==2:
            editar(arbol, parametrosComando[1])
        else:
            print("Numero de parametros incorrectos")

    elif parametrosComando[0]=="print":
        #se pasa comando y nombre
        if len(parametrosComando)==2:
            cat(arbol, parametrosComando[1])
        else:
            print("Numero de parametros incorrectos")

    elif parametrosComando[0]=="cd":
        #se pasa comando y nombre
        if len(parametrosComando)==2:
            cd(arbol, parametrosComando[1])
        else:
            print("Numero de parametros incorrectos")

    elif parametrosComando[0]=="atras":
        #se pasa comando
        if len(parametrosComando)==1:
            atras(arbol)
        else:
            print("Numero de parametros incorrectos")

    elif parametrosComando[0]=="/":
        #se pasa comando
        if len(parametrosComando)==1:
            cd(arbol, "/")
        else:
            print("Numero de parametros incorrectos")

    elif parametrosComando[0]=="actual":
        #se pasa comando
        if len(parametrosComando)==1:
            cadena=""
            for i in rutaActual(arbol):
                cadena=f"{cadena}{i.getNombre()}>"
            cadena=cadena.rstrip(">")
            print(cadena)
        else:
            print("Numero de parametros incorrectos")

    elif parametrosComando[0]=="ls":
        #se pasa comando
        if len(parametrosComando)==1:
            subCarp=mostrarSC(arbol)
            if subCarp==[]:
                print("Directorio vacío")
            else:
                for i in subCarp:
                    print(i.getNombre())
        #se pasa comando y ruta
        elif len(parametrosComando)==2:
            subCarp=mostrarSC(arbol, parametrosComando[1])
            if subCarp==[]:
                print("Directorio vacío")
            elif subCarp==None:
                print("No se puede examinar ese elemento")
            else:
                for i in subCarp:
                    print(i.getNombre())
        else:
            print("Numero de parametros incorrectos")

    else:
        print("Comando no reconocido")

    establecePadres(arbol)
