#Hoja de Trabajo 10, Algoritmos y estructuras de datos
#Consultas en Neo4j
#------------------Integrates------------------
# - Diego Sevilla 17348
# - David Soto 17551
# - Alejandro Tejada 17854

from neo4jrestclient.client import GraphDatabase    
from neo4jrestclient import client

db = GraphDatabase("http://localhost:7474", username="neo4j", password="123456")

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
    print("\nEstos son los pacientes disponibles en la base de datos: ")
    q = 'MATCH (u: Pacientes) RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    for r in results:
        print(" - " + "%s" % (r[0]["name"]))
    nomPaciente = raw_input("Ingrese el nombre del Paciente que desea relacionar: ")
    print("\nEstos son los doctores disponibles en la base de datos: ")
    q = 'MATCH (u: Doctores) RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    for r in results:
        print(" - " + "%s" % (r[0]["name"]))
    nomDoctor = raw_input("Ingrese el nombre del Doctor que desea relacionar: ")
    q = 'MATCH (u: Doctores) WHERE u.name="'+nomDoctor+'" RETURN u'
    results1 = db.query(q, returns=(client.Node))
    largo1 = len(results1)
    q = 'MATCH (u: Pacientes) WHERE u.name="'+nomPaciente+'" RETURN u'
    results2 = db.query(q, returns=(client.Node))
    largo2 = len(results2)
    if(largo1>0 and largo2>0):
        date = raw_input("Ingrese la fecha en la que el paciente visito al doctor(YYYYMMDD): ")
        med = raw_input("Ingrese el nombre de la medicina que el doctor prescribio: ")
        dateStart = raw_input("Ingrese la fecha en la cual debe iniciar el tratamoiento (YYYYMMDD): ")
        dateFinish = raw_input("Ingrese la fecha en la cual debe terminar el tratamoiento (YYYYMMDD): ")
        dosificacion = raw_input("Ingrese la dosis (cantidad y cada cuanto) que debe tomar el paciente: ")
        nuevaMed = db.nodes.create(name=med,desdeFecha=dateStart,hastaFecha=dateFinish,dosis=dosificacion)
        Drogas.add(nuevaMed)
        for r in results1:
            for i in results2:
                i[0].relationships.create("VISITS",r[0],fecha=date) #el paciente visita al doctor en tal fecha
                i[0].relationships.create("TAKE",nuevaMed) #el paciente toma la medicina
                r[0].relationships.create("PRESCRIBE",nuevaMed) #el doctor prescribe la medicina
                #r[0].relationships.create("PACIENT",i[0]) #el paciente es paciente del doctor en cuestion
                
        print("Se ha ingresado con exito la relacion\n")
    else:
        print("Alguno de los nombres escogidos no estaba dentro de la base de Datos")

#_________Metodo para consultar Doctores por su especialidad en la base de datos en Neo4j________#
def consultarEspecialidad():
    print("\nEstas son las especialidades disponibles en la base de datos: ") 
    q = 'MATCH (u: Doctores) RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    listaEsp = []
    for r in results:        
        if(len(results)>0):
            esp = r[0]["especialidad"]
            listaEsp.append(esp)
    imprimirSinRepetir(listaEsp) #Se imprime una lista de las especialidades que hay en la base de datos
    
    especialidadDada = raw_input("Ingrese el nombre de la especialidad para desplegar a los doctores en gestion: ")
    q = 'MATCH (u: Doctores) WHERE u.especialidad="'+especialidadDada+'" RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    for r in results:
        print("Se encontro al Doctor(a) %s con numero de contacto %s" % (r[0]["name"],r[0]["telefono"]))
    if(len(results)==0):
        print("\nNo se encontro ningun doctor(a) con dicha especialidad")
    else:
        pass

#_________Metodo para relacionar personas ingresadas en la base de datos en Neo4j________#
def relacionarPersonas():
    print("\nEstas son las personas disponibles en la base de datos: ")
    
    print("DOCTORES: ")
    q = 'MATCH (u: Doctores) RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    for r in results:
        print(" - " + "%s" % (r[0]["name"]))
        
    print("PACIENTES: ")
    q = 'MATCH (u: Pacientes) RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    for r in results:
        print(" - " + "%s" % (r[0]["name"]))
        
    persona1 = raw_input("Ingrese el nombre de la persona que conoce a otra persona: ")
    persona2 = raw_input("Ingrese el nombre de esa otra persona: ")
    
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
        anio = raw_input("Ingrese el anio desde que dicha persona conoce a la otra: ")
        for r in results1:
            for i in results3:
                r[0].relationships.create("KNOWS",i[0],since=anio)
        print("La relacion fue ingresada correctamente")
    elif(largo1>0 and largo4>0):
        anio = raw_input("Ingrese el anio desde que dicha persona conoce a la otra: ")
        for r in results1:
            for i in results4:
                r[0].relationships.create("KNOWS",i[0],since=anio)
        print("La relacion fue ingresada correctamente")
    elif(largo2>0 and largo3>0):
        anio = raw_input("Ingrese el anio desde que dicha persona conoce a la otra: ")
        for r in results2:
            for i in results3:
                r[0].relationships.create("KNOWS",i[0],since=anio)
        print("La relacion fue ingresada correctamente")
    elif(largo2>0 and largo4>0):
        anio = raw_input("Ingrese el anio desde que dicha persona conoce a la otra: ")
        for r in results2:
            for i in results4:
                r[0].relationships.create("KNOWS",i[0],since=anio)
        print("La relacion fue ingresada correctamente")
    else:
        print("Alguno de los nombres colocados no se encuentra en la base de datos")

def recomendacionDadoUnPaciente():
    print("\nEstos son los pacientes disponibles en la base de datos: ")
    q = 'MATCH (u: Pacientes) RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    for r in results:
        print(" - " + "%s" % (r[0]["name"]))
        
    paciente1 = raw_input("Ingrese el nombre del paciente a quien se le desea recomendar un doctor: ") #Se pide el nombre del paciente dado
    q = 'MATCH (u: Pacientes)-[r:KNOWS]->(m:Pacientes) WHERE u.name="'+paciente1+'" RETURN u, type(r), m' 
    resultsP = db.query(q, returns=(client.Node, str, client.Node))
    ConocidosPaciente = []
    for r in resultsP:        
        if(len(resultsP)>0):
            personaConocida = r[2]["name"]
            ConocidosPaciente.append(personaConocida)  #Se construye una lista con los nombres de las personas(Pacientes) que este paciente conoce
    
    print("\nEstas son las especialidades disponibles en la base de datos: ") 
    q = 'MATCH (u: Doctores) RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    listaEsp = []
    for r in results:        
        if(len(results)>0):
            esp = r[0]["especialidad"]
            listaEsp.append(esp)
    imprimirSinRepetir(listaEsp) #Se imprime una lista de las especialidades que hay en la base de datos                                            
        
    especialidadDada = raw_input("Ahora ingrese el nombre de la especialidad para recomendar algun doctor en gestion: ") #Se pide la especialidad del Dr que se recomendara
    q = 'MATCH (u: Doctores) WHERE u.especialidad="'+especialidadDada+'" RETURN u'
    resultsD = db.query(q, returns=(client.Node, str, client.Node))
    Especialistas = []
    for r in resultsD:         
        if(len(resultsD)>0):
            DrEsp = r[0]["name"]
            Especialistas.append(DrEsp) #Se construye una lista con los nombres de doctores que tienen la especialidad dada

    DrsRecomendados = []
    for i in ConocidosPaciente: #se recorre la lista de persnas(Pacientes) que el paciente dado conoce
        q = 'MATCH (u: Pacientes)-[r:VISITS]->(m:Doctores) WHERE u.name="'+i+'" RETURN u, type(r), m'
        DrsVisitados = []
        results1 = db.query(q, returns=(client.Node, str, client.Node))
        for r in results1:            
            if(len(results1)>0):
                DrVisitado = r[2]["name"]
                DrsVisitados.append(DrVisitado) #se construye una lista con los doctores visitados por el paciente conocido
        listaRepetidos = RepetidosEntreDosListas(DrsVisitados,Especialistas)
        if(len(listaRepetidos) > 0):
            for e in listaRepetidos:
                DrsRecomendados.append(e)
    if(len(DrsRecomendados) > 0):       
        print("\nEstos son los doctores que se le recomiendan al paciente, ya que han sido visitados por personas que el conoce.")
        imprimirSinRepetir(DrsRecomendados)
    else:
        print("\nProbablemente el paciente que ingreso no conoce a personas que hayan visitado a un medico con dicha especialidad. Intente de nuevo.")
    

def recomendacionDadoUnDoctor():
    print("\nEstos son los doctores disponibles en la base de datos: ")
    q = 'MATCH (u: Doctores) RETURN u'
    results1 = db.query(q, returns=(client.Node, str, client.Node))
    for r in results1:
        print(" - " + "%s" % (r[0]["name"]))
        
    doctor1 = raw_input("Ingrese el nombre del doctor que quiere recomendar otro doctor a un paciente: ")    

    q = 'MATCH (u: Doctores)-[r:KNOWS]->(m:Doctores) WHERE u.name="'+doctor1+'" RETURN u, type(r), m' 
    results3 = db.query(q, returns=(client.Node, str, client.Node))
    ConocidosDr = []
    for r in results3:
        print (" - " + "%s" % (r[2]["name"]))
        if(len(results3) > 0 ):
            conocidoDelDr = r[2]["name"]
            ConocidosDr.append(conocidoDelDr) #se construye una lista con los doctores que este doctor conoce    
    
    print("\nEstas son las especialidades disponibles en la base de datos: ") 
    q = 'MATCH (u: Doctores) RETURN u'
    results = db.query(q, returns=(client.Node, str, client.Node))
    listaEsp = []
    for r in results:        
        if(len(results)>0):
            esp = r[0]["especialidad"]
            listaEsp.append(esp)
    imprimirSinRepetir(listaEsp) #Se imprime una lista de las especialidades que hay en la base de datos

    especialidadDada = raw_input("Ahora ingrese el nombre de la especialidad para recomendar algun doctor en gestion: ") #Se pide la especialidad del Dr que se recomendara
    q = 'MATCH (u: Doctores) WHERE u.especialidad="'+especialidadDada+'" RETURN u'
    resultsD = db.query(q, returns=(client.Node, str, client.Node))
    Especialistas = []
    for r in resultsD:         
        if(len(resultsD)>0):
            DrEsp = r[0]["name"]
            Especialistas.append(DrEsp) #Se construye una lista con los nombres de doctores que tienen la especialidad dada

    DrsRecomendados = RepetidosEntreDosListas(ConocidosDr,Especialistas) #Se construye una lista con los doctores que el doctor conoce y ademas tienen la
                                                                        #especialidad dada
    if(len(DrsRecomendados)>0):
        print ("Los doctores recomendados son los siguientes: ")
        for i in DrsRecomendados:
            print(" - " + i)
    else:
        print ("El doctor que ingreso probablemente no conoce a otros doctores con esta especialidad. Intente de nuevo.")
    
    

#---------------------------Metodos extras para impresion y despliegue de informacion---------------------------#
#_________Metodo que elimina datos repetidos en una lista y los imprime________#
def imprimirSinRepetir(lista_original):
    if(len(lista_original)>0):
        lista_nueva = []
        for i in lista_original:
            if i not in lista_nueva:
                lista_nueva.append(i)
        for e in lista_nueva:
            print (" - " + e)            
        print ("")
    else:
        print ("No hay resultados")
        
#_________Metodo que retorna una lista con los valores repetidos entre dos listas____________#
def RepetidosEntreDosListas(lista1,lista2):    
    if(len(lista1)>0 and len(lista2)>0):
        lista_nueva = []
        for i in lista1:
            if (i in lista2 and i not in lista_nueva):
                lista_nueva.append(i)
    return lista_nueva
    
