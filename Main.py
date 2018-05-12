#Hoja de Trabajo 10, Algoritmos y estructuras de datos
#Consultas en Neo4j
#------------------Integrates------------------
# - Diego Sevilla 17348
# - David Soto 17551
# - Alejandro Tejada 17854

from Funciones import *

desicion = 0

while desicion != 6:
    print ("\nQue desea hacer?\n1.Ingresar Doctores, con los datos de su especialidad y como contactarlo\n2.Ingresar Pacientes, con sus datos.\n3.Ingresar que un paciente dado, visita a un doctor especifico. Indicar la fecha de visita y la medicina que le receta.\n4.Consultar cuales doctores tienen una especialidad dada.\n5.Ingresar que una persona conoce a otra persona.\n6.Salir\n")
    desicion = int(input("Ingrese su elecccion: "))
    
    if(desicion == 1):
        nombreDoc = raw_input("Ingrese el nombre del doctor: ")
        colegiado = raw_input("Ingrese el numero de colegiado del doctor: ")
        especialidad = raw_input("Ingrese el nombre de su especialidad: ")
        contacto = raw_input("Ingrese el telefono del doctor: ")
        
        ingresarDoctor(nombreDoc,colegiado,especialidad,contacto)

    if(desicion == 2):
        nombrePac = raw_input("Ingrese el nombre del paciente: ")
        telefono = raw_input("Ingrese el numero de telefono del paciente: ")

        ingresarPaciente(nombrePac,telefono)

    if(desicion == 3):
        relacionVisita()

    if(desicion == 4):
        especialidadDada = raw_input("Ingrese la especialidad que desea buscar: ")
        consultarEspecialidad(especialidadDada)

    if(desicion == 5):
        relacionarPersonas()

    
