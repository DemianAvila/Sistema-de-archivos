from functools import reduce

#objeto para clasificar los directorios
class Directorio:
    def __init__(self, nombre, nivel):
        self.nombre=nombre
        self.nivel=nivel
        self.puntero=False
        self.contenido=[]

    def aniadirSubElemento(self, subElem):
        self.contenido.append(subElem)

    def getSubElementos(self):
        return self.contenido

    def eliminarSubElemento(self, nombre):
        sinElemento=list(filter(lambda x: nombre!=x.nombre))
        self.contenido=sinElemento

    def getNombre(self):
        return self.nombre

    def setNombre(self, newNombre):
        self.nombre=newNombre

    def getNivel(self):
        return self.nivel

    def setNivel(self, nivel):
        self.nivel=nivel

    def getPuntero(self):
        return self.puntero

    def setPuntero(self, valor):
        self.puntero=valor

    def getTipo(self):
        return "D"

#objeto para clasificar los archivos
class Archivo:
    def __init__(self, nombre, nivel, contenido):
        self.nombre=nombre
        self.nivel=nivel
        self.contenido=contenido

    def getSubElementos(self):
        return ([])

    def getNombre(self):
        return self.nombre

    def setNombre(self, newNombre):
        self.nombre=newNombre

    def getContenido(self):
        return self.contenido

    def setContenido(self, newContenido):
        self.contenido=newContenido

    def getNivel(self):
        return self.nivel

    def setNivel(self, newNivel):
        self.nivel=newNivel

    def getTipo(self):
        return "F"

    #el puntero no puede estar en un archivo
    def getPuntero(self):
        return False

#retorna una lista con los archivos convertidos a objetos y el txt sin estos
def archivosAObjetos(lineasA):
    lineasArchivo=lineasA.copy()
    #iterar en el archivo, ignora la primera linea
    ignoraLinea=True
    #variable que permite verificar si se está leyendo un archivo
    lecturaArchivo=False
    #lista que guarda los archivos en objetos
    archivosNoOrden=[]
    #cuenta el separador de contenido de archivo
    contadorArchivo=0
    #lista sin los archivos del txt
    listaSinArchivos=[]
    #deshazte de los archivos
    for linea in lineasArchivo:
        if ignoraLinea:
            ignoraLinea=False
            continue
        data=linea.split(",")
        if len(data)==3:
            if data[2].strip()=="F":
                lecturaArchivo=True
                nuevoArchivo=Archivo(data[1], int(data[0]), "")
                continue
        if lecturaArchivo:
            if linea.strip()=="$$$\"\"\"$$$":
                contadorArchivo+=1
                pass
            if contadorArchivo==2:
                archivosNoOrden.append(nuevoArchivo)
                lecturaArchivo=False
                contadorArchivo=0
                continue
            if linea.strip()!="$$$\"\"\"$$$":
                nuevoArchivo.setContenido(nuevoArchivo.getContenido()+linea)
        else:
            listaSinArchivos.append(linea)

    return {
        'archivosObjeto':archivosNoOrden,
        'listaSinArchivos':listaSinArchivos
    }

#retorna solo la lista de carpetas convertidas en objeto
def directoriosAObjetos(listaSinA):
    #convertir todas las lineas a directorios
    carpetasObjeto=[]
    for linea in listaSinA:
        data=linea.split(",")
        nuevaCarpeta=Directorio(data[1], int(data[0]))
        carpetasObjeto.append(nuevaCarpeta)

    return carpetasObjeto

#leer el txt y retornar la lista
def archivoALista(contenidoArchivos):
    file=open("./FileTree.txt", 'r')
    lines=file.readlines()
    file.close()
    if contenidoArchivos==False:
        return lines
    else:
        contadorArchivo=0
        listaSinArchivos=[]
        lecturaArchivo=False
        for linea in lines:
            data=linea.split(",")
            if len(data)==3:
                if data[2].strip()=="F":
                    listaSinArchivos.append(linea)
                    lecturaArchivo=True
                    continue
            if lecturaArchivo:
                if linea.strip()=="$$$\"\"\"$$$":
                    contadorArchivo+=1
                    pass
                if contadorArchivo==2:
                    lecturaArchivo=False
                    contadorArchivo=0
                    continue
            else:
                listaSinArchivos.append(linea)
        return listaSinArchivos




#la definición de objetos revisa todo el arbol de archivos y lo vacia todo en los objetos
#retorna la raiz, los archivos y las carpetas en formato objetos
def definicionObjetos ():
    #abrir el archivo para leerlo
    lines=archivoALista(False)
    #obtener la primera linea para crear el objeto padre, la raiz
    if lines[0].split(",")[1]=="/":
        raiz= Directorio('/', 0)
        actual=raiz
        raiz.setPuntero(True)
    else:
        return None

    archivosObjeto=archivosAObjetos(lines)
    directoriosObjeto=directoriosAObjetos(archivosObjeto["listaSinArchivos"])

    retorno={
        'raiz': raiz,
        'directorios': directoriosObjeto,
        'archivos': archivosObjeto['archivosObjeto'],
    }

    return retorno




#esta función debe retornar el arbol con las subcarpetas y archivos en su lugar determinado
def insertarSubcarpetas():
    defObj=definicionObjetos()
    lines=archivoALista(True)
    #obtiene la profundidad mas alta
    def profMasAlta(inicio, siguiente):
        if siguiente>=inicio:
            return siguiente
        else:
            return inicio
    profundidadMasAlta=reduce(profMasAlta, list(map(lambda x: int(x.split(",")[0]), lines)), 0)
    elementosPorNivel=[]
    #separa los elementos de acuerdo a la profundidad en la que estan, de atras hacia adelante
    for i in range(profundidadMasAlta, 1, (-1)):
        elementos=list(filter(lambda x: i==int(x.split(",")[0]), lines))
        elementosPorNivel.append(elementos)
    #encuentra el padre del elemento que se busca, relaconalos, e inserta el objeto dentro
    #por cada hijo encuentra el padre
    listaTmp=[]
    for subnivel in elementosPorNivel:
        for hijo in subnivel:
            hijoData=hijo.split(",")
            for elemento in lines:
                elementoData=elemento.split(",")
                #ve escribiendo una lista temporal que se pueda recorrer hacia atras
                #cuando encuentres al hijo en el archivo, termina este ciclo y comienza a recorrer la lista al reves
                if hijoData==elementoData:
                    break
                else:
                    listaTmp.append(elemento)
            #recorre la lista al reves
            for elemento in reversed(listaTmp):
                elementoData=elemento.split(",")
                #encuentra al directorio inmediato anterior, es decir, el que tenga una profundidad menor
                if (int(hijoData[0])-1)==int(elementoData[0]) and elementoData[2].strip()=="D":
                    #cuando lo encuentres, busca al hijo y al padre en la lista de objetos
                    #si es archivo buscalo en la lista de objetos y archivos
                    if hijoData[2].strip()=="F":
                        objetoHijo=list(filter(lambda x: x.getNivel()==int(hijoData[0]) and x.getNombre()==hijoData[1], defObj["archivos"]))
                    #si es directorio buscalo en la lista de directorios
                    if hijoData[2].strip()=="D":
                        objetoHijo=list(filter(lambda x: x.getNivel()==int(hijoData[0]) and x.getNombre()==hijoData[1], defObj["directorios"]))
                    #obtener el objeto padre
                    objetoPadre=list(filter(lambda x: x.getNivel()==int(elementoData[0]) and x.getNombre()==elementoData[1], defObj["directorios"]))
                    #insertar al objeto hijo en el objeto padre y terminar con el ciclo
                    objetoPadre[0].aniadirSubElemento(objetoHijo[0])
                    break
    #añadir los niveles 1 a la raiz
    niveles1=list(filter(lambda x: int(x.getNivel())==1, defObj["directorios"]))
    niveles1txt=list(filter(lambda x: int(x.getNivel())==1, defObj["archivos"]))
    niveles1.extend(niveles1txt)
    for i in niveles1:
        defObj["raiz"].aniadirSubElemento(i)

    #retornar el arbol, es decir, la raiz con cada hijo añadido
    return defObj["raiz"]


#recorrer el arbol de forma recursiva
def recorreArbol(inicio):
    if inicio.getSubElementos()==[]:
        return []
    else:
        for a in inicio.getSubElementos():
            print(f"Nivel= {a.getNivel()} Nombre= {a.getNombre()}")
            recorreArbol(a)

#recorrer el arbol de forma recursiva para encontrar el puntero de ruta actual
def buscaPuntero(inicio):
    if inicio.getPuntero()==True:
        return inicio
    if inicio.getSubElementos()==[]:
        return []
    else:
        for a in inicio.getSubElementos():
            if a.getPuntero()==True:
                return a
            else:
                recorreArbol(a)


#------------------------inicio funciones de sistema de archivos----
#-----navegación--------

#regresa falso o verdadero dependiendo si existe o no
#tambien retorna la ruta absoluta desde la raiz
#soporta ruta absoluta y relativa

def existeRuta (arbol, ruta, archivo):
    #bandera que indica si una ruta esta disponible
    disponible=False
    #verificar si la ruta es absoluta
    if ruta.startswith("/"):
        #copiar el arbol pata trabajar con el
        tmp=arbol.getSubElementos()
        rutaObjetos=[]
        #separar las rutas requeridas con el picoparentesis
        rutaRequerida=ruta.split(">")
        #añadir la raiz
        rutaObjetos.append("/")
        ignoraLinea=True
        for elemento in rutaRequerida:
            #ignora la primer linea
            if ignoraLinea:
                ignoraLinea=False
                continue
            #si en el elemento de analisis actual coincide con el nombre, entonces si existe, cambia al siguiente subnivel
            if archivo:
                existe=list(filter(lambda x: elemento==x.getNombre(), tmp))
            #si los archivos no son requeridos entonces solo verifica si existe el directorio
            if archivo==False:
                existe=list(filter(lambda x: elemento==x.getNombre(), tmp))
                if existe[0].getTipo()=="F":
                    existe.pop(0)
            if len(existe)==1:
                rutaObjetos.append(elemento)
                try:
                    tmp=tmp.getSubElementos()
                except: break
        #al final del ciclo deben ambas listas deben tener la misma longitud
        if rutaObjetos==rutaRequerida:
            disponible=True

    #rutas relativas
    else:
        #lista para almacenar
        rutaObjetos=[]
        #separar las rutas requeridas con el picoparentesis
        rutaRequerida=ruta.split(">")
        #buscar la ruta con el puntero activo
        puntero=buscaPuntero(arbol)
        print(puntero.getSubElementos())
        #el primer elemento es el puntero en si mismo, tiene condiciones diferentes de busqueda
        ignoraLinea=True
        #buscar la ruta a partir del puntero
        for elemento in rutaRequerida:
            if ignoraLinea:
                ignoraLinea=False
                if puntero.getNombre()==elemento:
                    rutaObjetos.append(elemento)
                    tmp=puntero.getSubElementos()
                    continue
                else:
                    continue
            #si en el elemento de analisis actual coincide con el nombre, entonces si existe, cambia al siguiente subnivel
            if archivo:
                existe=list(filter(lambda x: elemento==x.getNombre(), tmp))
            #si los archivos no son requeridos entonces solo verifica si existe el directorio
            if archivo==False:
                existe=list(filter(lambda x: elemento==x.getNombre(), tmp))
                if existe[0].getTipo()=="F":
                    existe.pop(0)
            if len(existe)==1:
                rutaObjetos.append(elemento)
                try:
                    tmp=tmp.getSubElementos()
                except: break
        #al final del ciclo deben ambas listas deben tener la misma longitud
        if rutaObjetos==rutaRequerida:
            disponible=True


    retorno={
        "disponible":disponible,
        "rutaObjetos":rutaObjetos,
    }
    return retorno
