#MODULO DE OPERACIONES ALEJANDRO
#FUNCIONES VARIAS PARA LA VIDA
from math import *
#FUNCION PARA VER SI LO QUE INGRESA ES ENTERO
def leer_entero(mensaje):
    valido = False
    while not valido:
        try:
            entero = int(raw_input(mensaje))
            valido = True
        except:
            print "El dato no es un entero"
    return entero
 
#FUNCION PARA INGRESAR ALGO Y VER SI ES CADENA O STRING 

def leer_texto(mensaje):
    valido = false
    while not valido:
        try:
            texto = str(raw_input(mensaje))
            valido = true
        except:
            print "El dato no es texto"
    return texto

#FUNCION PARA INGRESAR ALGO Y ASEGURARSE QUE ES DECIMA

def leer_decimal(mensaje):
    valido = false
    while not valido:
        try:
            decimal = float(raw_input(mensaje))
            valido = true
        except:
            print "El dato no es un entero"
    return decimal

#FUNCION PARA SUMARLE A UN NUMERO +100
def suma_100(x):
    print "El valor inicial de x es: ",x
    x=x+100
    print "El nuevo valor de x es: ", x
    return x
#FUNCION PARA SACAR EL SENO EN GRADOS

def sin_grados(x):
    grados=sin((pi*x)/180)
    return grados

#FUNCION PARA SACAR EL COSENO EN GRADOS

def cos_grados(x):
    grados=cos((pi*x)/180)
    return grados

#FUNCION PARA SACAR EL FACTORIAL DE UN NUMERO
def factorial(num):#definimos la funcion de factorial
        if num<0:#si el numero que se necesita el factorial es menor a 0 devuelve -1
                return -1 #retornamos menos 1
        else:#De lo contrario si es mayor a 0
                resultado=1#La variable resultado va a ser 1 ya que el factorial es multiplicacion
                for i in range(num):#for [Variable I] in range(de 0-valor de num se va a repetir)
                        resultado *=(i+1)#resultado que valia 1 va a ser igual a la multiplicacion de i+1
                return resultado#se retorna resultado
#FUNCION PARA LEER 
def pasar_archivo_lista(nombre_archivo):
    archivo= open(nombre_archivo)#Importamos los  archivos de texto
    for patito in archivo:#Creamos un ciclo que recorra la variable que contiene la lectura del archivo
        alumnos.append(patito)#Guardamos en una lista vacia los valores del archivo de texto
    return alumnos
