import turtle as t
import sys

# Errores posibles
class Errores(Exception):
    pass

class FormatoIncorrectoError(Errores):
    pass

class nadaOespacios (Errores):
    pass

class Invalido (Errores):
    pass


def main():
    """ Organiza el flujo principal del programa"""
    
    # Recoleccion y validacion de datos importados desde archivos externos
    diccio_datos = validaDatos()
    diccio_color = validaColor()
    
    # Recoleccion y validacion de la configuracion del grafico
    paleta_colores = solicitaPaletaColores(diccio_color)
    tipo_grafico = solicitaTipoGrafico()

    # Solicita titulo no vacío, detectando si ingresa puros espacios o Enter
    titulo = solicitaTitulo()
    
    # Generacion del grafico
    t.setup(750,500,50,50)
    t.setworldcoordinates(0,0,750,500)
    t.speed("fast")
    t.ht() # Con esto se esconde la tortuga
    
    opcion_color = diccio_color[paleta_colores]
    print("Generando gráfico...")
    
    if(tipo_grafico == "barras"):
        grafBarra(diccio_datos , opcion_color , titulo)
        
    elif(tipo_grafico == "línea"):
        grafLinea(diccio_datos , opcion_color , titulo)
        
    else: # Si se salta el if y elif anteriores, es porque es grafico de torta
        creaTorta(diccio_datos , opcion_color, titulo)

def validaDatos(): 
    """
    Valida el nombre del archivo, valida el formato y retorna el contenido 
    del archivo en un diccionario
    """
    
    finaliza = False # da la posibilidad de salir del programa presionando Enter
    condicion = True 
    while(condicion):
        try:
            nom = input("Ingrese nombre del archivo de datos: ")
            
            if(finaliza and nom == ""): # finaliza el programa
                sys.exit()
                
            nom = nom.strip()
            lineasDatos = {} # Contenedor de informacion
            
            if (nom == ""):
                raise nadaOespacios
                
            with open(nom) as archivo:
                for fila in archivo:
                    fila = fila.strip("\n") 
                    y = fila.split(',')
                    
                    # formato requerido de dos columnas y columna 2 de numeros positivos
                    if(len(y) != 2 or int(y[1]) <= 0): # la segunda condicion se lee SOLO si la primera es falsa
                        raise Invalido
                    
                    lineasDatos[y[0]] = int(y[1]) # formato de entero para el segundo elemento
                        
                condicion = False # el archivo es valido
                    
        except(FileNotFoundError):
            print("   No existe un archivo con ese nombre, inténtelo nuevamente")
            print("   Ingrese un nuevo nombre o presione ENTER para abandonar el programa.")
            finaliza = True
            
        except(ValueError,Invalido):
            print("   El archivo no tiene el formato requerido, inténtelo nuevamente")
            print("   Ingrese un nuevo nombre o presione ENTER para abandonar el programa.")
            finaliza = True
            
        except(nadaOespacios):
            print("   Nada ingresó, intentélo nuevamente")
            
    return lineasDatos


def validaColor(): 
    """
    valida el nombre del archivo para los colores, valida el formato y retorna 
    lo que contiene el archivo en un diccionario
    """
    
    finaliza = False # da la posibilidad de salir del programa
    condicion = True
    
    while(condicion):
        try:
            nom = input("Ingrese nombre del archivo de colores: ")
            
            if(finaliza and nom == ""): # finaliza el programa
                sys.exit()
                
            nom = nom.strip()
            cont = 0 # identificador de fila (par o impar)
            diccio = {}
            
            if(len(nom) == 0):
                raise nadaOespacios
                
            with open(nom) as archivo:
                lineas = archivo.readlines()
                
                if(len(lineas)%2 != 0): # validacion el número de filas es par
                    raise Invalido
                    
                # validacion del formato fila por fila
                for fila in lineas:
                    fila = fila.strip("\n")
                    
                    if(cont == 0): # validacion forma: >nombre
                        if (fila[0] != '>'): 
                            raise Invalido
                            
                        y = fila 
                        cont = 1
                        
                    elif(cont == 1): # validacion forma: hex1,hex2,hex3...
                        x = fila.split(',')
                        for i in range(0,len(x)):
                            if(len(x[i]) != 6): # validacion rango: 000000 - FFFFFF
                                raise Invalido
                            num = int(str(x[i]), 16) # validacion: hexadecimal
                            
                        diccio[y.lstrip('>')] = tuple(x)
                        cont = 0
                        
                    condicion = False
                    
        except(FileNotFoundError):
            print("   No existe un archivo con ese nombre, inténtelo nuevamente")
            print("   Ingrese un nuevo nombre o presione ENTER para abandonar el programa.")
            finaliza = True
            
        except(ValueError, Invalido):
            print("   El archivo no tiene el formato requerido, inténtelo nuevamente")
            print("   Ingrese un nuevo nombre o presione ENTER para abandonar el programa.")
            finaliza = True
            
        except(nadaOespacios):
            print("   Nada ingresó, intentélo nuevamente")
            
    return diccio


def solicitaTipoGrafico():
    tipo_grafico = ["barras", "torta", "línea"] # graficos disponibles
    print("\nSelecciona el tipo de gráfico:")
    # Enumerate: enumera cada elemento del iterador, funciona como contador
    for i, tipo in enumerate(tipo_grafico):
        print(f"   {i+1}) {tipo}") 
    
    condicion = True
    while(condicion):
        try:
            opcion = int(input("Ingrese opción: ").strip())
            if(opcion < 1 or opcion > len(tipo_grafico)):
                raise Invalido
            condicion = False
            
        except:
            print("   Opción no disponible")
    
    return tipo_grafico[opcion-1]



def solicitaPaletaColores(colores): # Funcion que solicita los colores para el gráfico
    colores_lista = list(colores.keys())
    print("\nSeleccione paleta de colores para su gráfico:")
    for i, color in enumerate(colores_lista):
        print(f"   {i+1}) {color}")
        
    condicion = True
    while(condicion):
        try:
            opcion = int(input("Ingrese opción: ").strip())
            if(opcion < 1 or opcion > len(colores_lista)):
                raise Invalido
            condicion = False
            
        except (Invalido, ValueError):
            print("   Opción no disponible")
    
    return colores_lista[opcion-1]


def solicitaTitulo(): # funcion que solicita titulo para el grafico, no se permite un string vacío.
    t = input("Ingrese un título para el gráfico: ").strip()
    while(t == ""):
        t = input("Error, Ingrese título nuevamente: ").strip()
        
    return t

""" Grafico de Barras """
""" Se llama a esta funcion para crear el grafico de barras """
def grafBarra(diccio,colors,titulo):
  t.up()
  t.goto(100,100)
  t.down()
  pos = 0       #pos sirve para ir cambiando el color
  cont = 0      #cont sirve para ajustar el tamaño del grafico de acuerdo a la cantidad de paises
  for pais in diccio:
    if(pos == len(colors)):
      pos = 0
    creaBarra(pais,diccio[pais],colors[pos])
    pos += 1
    cont += 1
  t.up()
  # Se crean los ejes X e Y del grafico
  t.goto(80,400)
  t.down()
  t.setheading(270)
  t.color("black")
  t.write("600",False,"center")
  t.fd(300)
  t.left(90)
  t.fd(cont*65)
  t.up()
  # Con esto el titulo queda centrado siempre
  xtitle = ((cont*65)/2)+80
  t.goto(xtitle,410)
  t.write(titulo,False,"center",font=("Verdana",13,"normal"))
  t.done()

""" Crea cada barra y escribe su pais correspondiente """
def creaBarra(pais,alt,clr):
  alt = int(alt)/2  # La altura la divido por 2 para ajustar proporciones
  t.begin_fill()
  t.color("#"+clr)
  # Escribe nombre del pais
  t.up()
  t.setheading(-45)
  t.fd(2**(1/2)*20) # avanza el equivalente a una diagonal de cuadrado 20x20
  t.color("black")
  t.write(pais, align="center")
  t.color("#"+clr)
  t.bk(2**(1/2)*20)
  t.setheading(90)
  t.down()
  # Crea barra
  t.fd(alt)
  t.right(90)
  t.color("black")
  t.fd(20)
  t.write(int(alt)*2,False, align="center")
  t.bk(20)
  t.color("#"+clr)
  t.fd(40)
  t.right(90)
  t.fd(alt)
  t.left(90)
  t.penup()
  t.fd(20)
  t.pendown()
  t.end_fill()

""" Grafico de Lineas """
""" Se llama a esta funcion para crear el grafico de lineas """
def grafLinea(diccio,colors,titulo):
  t.up()
  t.goto(80,100)
  t.down()
  cont = 0
  x = 150
  for pais in diccio:
    if(cont == 0):
      y = int(diccio[pais])/2
      # Grafica del primer pais, para evitar que salga una linea desde origen
      t.begin_fill()
      t.up()
      t.goto(x,y+110)
      t.color("black")
      # Escribe el valor y el circulo
      t.up()
      t.goto(x,y+80)
      t.write(diccio[pais],False,"center", font=("verdana", 11))
      t.goto(x,y+110)
      t.down()
      t.color("#"+colors[0])
      t.circle(4)
      t.end_fill()
      # Escribe primer Pais
      t.up()
      t.color("black")
      t.goto(x,70)
      t.write(pais,False,"center", font=("verdana", 11))
      t.goto(x,y+110)
    else:
      creaLinea(pais,diccio[pais],colors[0],x)
    x += 100
    cont += 1
  t.up()
  # Se crean los ejes X e Y del grafico
  t.goto(90,400)
  t.down()
  t.setheading(270)
  t.color("black")
  t.write("600",False,"center", font=("verdana", 11))
  t.fd(300)
  t.left(90)
  t.fd(cont*105)
  t.up()
  # Con esto el titulo queda centrado siempre
  xtitle = ((cont*105)/2)+90
  t.goto(xtitle,450)
  t.write(titulo,False,"center",font=("Verdana",14,"normal"))
  t.done()

def creaLinea(pais,alt,clr,x):
  # La esquina inferior izquierda es 0,0
  alt = int(alt)/2
  t.down()
  t.begin_fill()
  t.color("#"+clr)
  # Crea linea y circulito
  t.goto(x,alt+110)
  t.circle(4)
  t.end_fill()
  # Escribe el valor
  t.up()
  t.goto(x,alt+80)
  t.down()
  t.color("black")
  t.write(int(alt*2),False,"center", font=("verdana", 11))
  t.up()
  t.goto(x,alt + 110)
  # Escribe pais
  t.up()
  t.goto(x,70)
  t.write(pais,False,"center", font=("verdana", 11))
  t.goto(x,alt+110)

""" Grafico de Torta """
""" Se llama a esta funcion para crear el grafico de torta """
def creaTorta(diccio, colorsR,titulo):
    radius = 200
    t.up()
    t.forward(radius)
    t.down()
    t.circle(radius)
    t.up()
    t.setheading(90)
    t.forward(radius)
    divideTorta(diccio ,colorsR)
    colocaNombresTorta(diccio)
    # titulo
    t.goto(200,410)
    t.write(titulo,False,"center",font=("Verdana", 14,"normal"))
    t.done()

def divideTorta(diccio,colorsR):
    perc = 0
    radius = 200
    total = sum(list(diccio.values())) # suma las claves del diccio dentro de una lista
    contador = 0
    for percent in diccio:
        x = (diccio[percent] * 100) / total 
        porciento  = (x * 360)/100
        perc += porciento
        t.color("black")
        t.setheading(perc)
        t.down()
        t.forward(radius)
        t.forward(-radius)
        t.up()
        t.up()
        if(contador == len(colorsR)):
          contador = 0
        t.color("#" + colorsR[contador])
        contador += 1
        t.begin_fill()
        t.setheading(perc)
        t.forward(radius)
        t.left(-90)
        t.down()
        t.circle(-radius, porciento)
        t.end_fill()
        t.setheading(perc-porciento)
        t.forward(-radius)
        t.up()
        t.right(-90)
        
def colocaNombresTorta(diccio):
    perc = 0
    radius = 200
    total = sum(list(diccio.values())) # suma las claves del diccio
    for percent in diccio:
        x = (diccio[percent] * 100) / total
        porciento  = (x * 360) / 100
        perc += porciento
        t.color("black")
        t.setheading(perc-(porciento/2))
        t.forward(radius/1.5)
        t.write(percent, align="center", font=("arial", 14, "normal"))
        t.setheading(-90)
        t.forward(25)
        t.write(str(round(x,1))+"%", align="center", font=("arial", 14, "normal"))
        t.forward(-25)
        t.setheading(perc-(porciento/2))
        t.forward(-radius/1.5)

def colocaNombresTortad(diccio):
    radio = 200
    total = sum(list(diccio.values()))
    t.goto(radio, radio)
    for key, val in diccio.items():
        grad = val * 360 / 100
        t.write(key, font=("arial", 14))

main()
