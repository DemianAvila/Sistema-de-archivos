# Emulación de sistema de archivos con python
Un sistema de archivos con carpetas y subcarpetas con las operaciones básicas implicadas en ello.

### Ejemplo del archivo .txt
<pre><code>
0,/,D
1,carpeta0.1,D
1,carpeta0.2,D
1,texto0.1.txt,F
$$$"""$$$
Contenido
mas contenido
$$$"""$$$
1,carpeta0.3,D
2,carpeta0.3.1,D
3,carpeta0.3.1.1,D
2,texto0.3.1,F
$$$"""$$$
$$$"""$$$
3,carpeta0.3.1.2,D
1,carpeta0.4,D
</code></pre>

### Conversión al arbol de objetos 
<pre><code>
self.nombre=raiz
self.nivel=0
self.puntero=True (el puntero indica la ruta actual en el arbol)
self.contenido=[

  self.nombre=carpeta0.1
  self.nivel=1
  self.puntero=False
  self.contenido=[]

  self.nombre=carpeta0.2
  self.nivel=1
  self.puntero=False
  self.contenido=[]

  self.nombre=texto0.1.txt
  self.nivel=1
  self.contenido="""
  Contenido
  mas contenido
  """

  self.nombre=carpeta0.3
  self.nivel=1
  self.puntero=False
  self.contenido=[
  
    self.nombre=carpeta0.3.1
    self.nivel=2
    self.puntero=False
    self.contenido=[

      self.nombre=carpeta0.3.1.1
      self.nivel=3
      self.puntero=False
      self.contenido=[]

      self.nombre=carpeta0.3.1.2
      self.nivel=3
      self.puntero=False
      self.contenido=[]

    ]

    self.nombre=texto0.3.1
    self.nivel=2
    self.contenido=""

  ]

  self.nombre=carpeta0.4
  self.nivel=1
  self.puntero=False
  self.contenido=[]

]

</code></pre>

### Establecimiento de rutas
**Una ruta puede ser**
- Absoluta desde la raiz con la sintaxis 
  - */>carpeta0.3>carpeta0.3.1*
- Relativa desde el puntero actual
  - Por si sola: (se está en la carpeta0.3) 
    - *carpeta0.3.1*
  - Compuesta de mas subrutas (se está en la carpeta0.3)
    - *carpeta0.3.1>carpeta0.3.1.2*
    - **Las rutas se separan con el picoparentesis >**


