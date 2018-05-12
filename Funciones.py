#Hoja de Trabajo 10, Algoritmos y estructuras de datos
#Consultas en Neo4j
#------------------Integrates------------------
# - Diego Sevilla 17348
# - David Soto 17551
# - Alejandro Tejada 17854

from neo4jrestclient.client import GraphDatabase    
from neo4jrestclient import client

db = GraphDatabase("http://localhost:7474", username="neo4j", password="1234567")

#_________Se crean las etiquetas________#
Doctores = db.labels.create("Doctores")
Pacientes = db.labels.create("Pacientes")
Drogas = db.labels.create("Drogas")

#_________Metodo para ingresar un doctor a la base en Neo4j________#
def ingresarDoctor(nombre,colegia,esp,tel):
    nuevoDoctor = db.nodes.create(name=nombre,colegiado=colegia,especialidad=esp,telefono=tel)
    Doctores.add(nuevoDoctor)
    print ("\nSe ha ingresado al Doctor correctamente\n")

#_________Metodo para ingresar un paciente a la base en Neo4j________#
def ingresarPaciente(nombre,tel):
    nuevoPaciente = db.nodes.create(name=nombre,telefono=tel)
    Pacientes.add(nuevoPaciente)
    print ("\nSe ha ingresado al Paciente correctamente\n")

#_________Metodo para ingresar la relacion de visita entre Paciente a Doctor, la prescripcion de Doctor a Medicina y de Paciente a Medicina________#
def relacionVisita():
    print("\nEstas son los pacientes disponibles en la base de datos\n")
    q = 'MATCH (u: Pacientes) RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    for r in results:
        print("%s" % (r[0]["name"]))
    nomPaciente = raw_input("Ingrese el nombre del Paciente que desea relacionar: \n")
    print("\nEstos son los doctores disponibles en la base de datos\n")
    q = 'MATCH (u: Doctores) RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    for r in results:
        print("%s" % (r[0]["name"]))
    nomDoctor = raw_input("Ingrese el nombre del Doctor que desea relacionar: \n")
    q = 'MATCH (u: Doctores) WHERE u.name="'+nomDoctor+'" RETURN u'
    results1 = db.query(q, returns=(client.Node))
    largo1 = len(results1)
    q = 'MATCH (u: Pacientes) WHERE u.name="'+nomPaciente+'" RETURN u'
    results2 = db.query(q, returns=(client.Node))
    largo2 = len(results2)
    if(largo1>0 and largo2>0):
        date = raw_input("Ingrese la fecha en la que el paciente visito al doctor(YYYYMMDD): \n")
        med = raw_input("Ingrese el nombre de la medicina que el doctor prescribio: \n")
        dateStart = raw_input("Ingrese la fecha en la cual debe iniciar el tratamoiento (YYYYMMDD): \n")
        dateFinish = raw_input("Ingrese la fecha en la cual debe terminar el tratamoiento (YYYYMMDD): \n")
        dosificacion = raw_input("Ingrese la dosis (cantidad y cada cuanto) que debe tomar el paciente: \n")
        nuevaMed = db.nodes.create(name=med,desdeFecha=dateStart,hastaFecha=dateFinish,dosis=dosificacion)
        Drogas.add(nuevaMed)
        for r in results1:
            for i in results2:
                i[0].relationships.create("VISITS",r[0],fecha=date)
                r[0].relationships.create("PRESCRIBE",nuevaMed)
                i[0].relationships.create("TAKE",nuevaMed)
        print("Se ha ingresado con exito la relacion\n")
    else:
        print("Alguno de los nombres escogidos no estaba dentro de la base de Datos")

#_________Metodo para consultar Doctores por su especialidad en la base en Neo4j________#
def consultarEspecialidad(especialidades):
    q = 'MATCH (u: Doctores) WHERE u.especialidad="'+especialidades+'" RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    for r in results:
        print("\nSe encontro al Doctor(a) %s con numero de contacto %s\n" % (r[0]["name"],r[0]["telefono"]))
    if(len(results)==0):
        print("\nNo se encontro ningun doctor(a) con dicha especialidad")
    else:
        pass

#_________Metodo para relacionar personas ingresadas en la base en Neo4j________#
def relacionarPersonas():
    print("\nEstas son las personas disponibles en la base de datos\n")
    q = 'MATCH (u: Doctores) RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    for r in results:
        print("%s" % (r[0]["name"]))
    q = 'MATCH (u: Pacientes) RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    for r in results:
        print("%s" % (r[0]["name"]))
    persona1 = raw_input("Ingrese el nombre de la persona que conoce a otra persona: ")
    persona2 = raw_input("Ingrese el nombre de la persona que se conoce: ")
    
    q = 'MATCH (u: Doctores) WHERE u.name="'+persona1+'" RETURN u'
    results1 = db.query(q, returns=(client.Node))
    largo1 = len(results1)
    q = 'MATCH (u: Pacientes) WHERE u.name="'+persona1+'" RETURN u'
    results2 = db.query(q, returns=(client.Node))
    largo2 = len(results2)
    q = 'MATCH (u: Pacientes) WHERE u.name="'+persona2+'" RETURN u'
    results3 = db.query(q, returns=(client.Node))
    largo3 = len(results3)
    q = 'MATCH (u: Doctores) WHERE u.name="'+persona2+'" RETURN u'
    results4 = db.query(q, returns=(client.Node))
    largo4 = len(results4)

    if(largo1>0 and largo3>0):
        anio = raw_input("Ingrese el anio desde que dicha persona conoce a la otra")
        for r in results1:
            for i in results3:
                r[0].relationships.create("KNOWS",i[0],since=anio)
        print("La relacion fue ingresada correctamente")
    elif(largo1>0 and largo4>0):
        anio = raw_input("Ingrese el anio desde que dicha persona conoce a la otra")
        for r in results1:
            for i in results4:
                r[0].relationships.create("KNOWS",i[0],since=anio)
        print("La relacion fue ingresada correctamente")
    elif(largo2>0 and largo3>0):
        anio = raw_input("Ingrese el anio desde que dicha persona conoce a la otra")
        for r in results2:
            for i in results3:
                r[0].relationships.create("KNOWS",i[0],since=anio)
        print("La relacion fue ingresada correctamente")
    elif(largo2>0 and largo4>0):
        anio = raw_input("Ingrese el anio desde que dicha persona conoce a la otra")
        for r in results2:
            for i in results4:
                r[0].relationships.create("KNOWS",i[0],since=anio)
        print("La relacion fue ingresada correctamente")
    else:
        print("Alguno de los nombres colocados no se encuentra en la base de datos")
