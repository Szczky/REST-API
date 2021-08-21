import json
import sys
import urllib

from SPARQLWrapper import SPARQLWrapper
from django.http import HttpResponse
from SPARQLWrapper.SPARQLExceptions import Unauthorized, EndPointNotFound
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

fuseki = "http://localhost:3030/data"  #Adresse von Fuseki-Endpoint


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def newUser(request):
    """
        Legt einen neuen User in der Ontologie an. Die Methode wird aufgerufen, wenn ein POST Request an die
        URL "<base_URL>/user/" gesendet wird.
        Die Informationen für den anzulegenden User werden aus dem Body ausgelesen.
        Parameter:
        - request: Das Anfrageobjekt
        - Body: id, username, [interesse], [kenntnisse]
        Return-Wert:
        Userobjekt wenn es angelegt wurde oder Fehlermeldung
        Wirft Exceptions:
        - urllib.error.URLError - wenn den SPARQL-Endpoint nicht erreichbar
        - KeyError - Wenn ein Wert von Body Fehlt
        - allgemeinen Exception
    """
    if request.method != 'POST':
        return HttpResponse("An diese URL darf nur POST-Anfrage gesendet werden")
    sparql = SPARQLWrapper(fuseki, returnFormat="json")
    try:
        body_unicode = request.body.decode('utf-8') #JSONFile von Body wird zu lesbare Daten umwandelt
        body = json.loads(body_unicode)
    except:
        return HttpResponse("Bei Dateneingabe ist ein Fehler aufgetaucht!")
    try:                                        #Die Daten von Body werden zu Variablen gespeichert
        id=body["id"]                           #wenn die nicht erreichbar sind, wirt einen Exception
    except KeyError:
        return HttpResponse("ID fehlt!")        #kontrollieren, ob noch keine User mit dieser ID in Onotolgy angelegt geworden
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            ASK  { 
                ?uri rdf:type kic:User .
                ?uri kic:hasID "%s"^^xsd:string
            }
        """ % id
    sparql.setQuery(query)                      #Querytext einstellen
    try:
        existiert = sparql.query().convert()        #Query ausführen un den Ergebnis in ein Variablen speichern
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist aufgetaucht!")
    if existiert['boolean']:                    #Falls diese ID schon existiert, kann den USer nicht angelegt werden
        return HttpResponse("Die ID %s hat schon ein User." % id)
    try:                                        #gleiche wie oben mit dem URI
        name=body["name"]
    except KeyError:
        return HttpResponse("URI fehlt!")       #Hier Prüfen wir nicht nur den User Klasse, sondern die ganze Ontology
    query = """                                 
                PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                ASK  { 
                  kic:%s ?p ?o.
                } 
            """ % name
    sparql.setQuery(query)
    try:
        existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist aufgetaucht!")
    if existiert['boolean']:
        return HttpResponse("Das URI %s existiert schon. Es muss ein unique sein." % name)
    hatInteresse=True                       #Weil Interesse und Knowledge nicht Pflichtfelden sind, muss man kontrollieren,
    hatKnowledge=True                       #ob sie in JSON Daten existieren. falls nein, wird KeyError Exception werfen, und
    try:                                    #den bestimte Variable False stellen
        interesse=body["interesse"]
        if type(interesse) is list:         #kann 0..n Stück Interesse eingegeben werden. Je nach Liste oder String, muss
                                            #es anderes behandelt werden
            for i in interesse:             #Bei ein Liste: kontrollieren wir alle Elemente, ob sie in Onto existieren
                query="""
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                    PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                    ASK  { 
                      dom:%s rdf:type ?p .
                      FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                      dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                    }
                """ %i
                sparql.setQuery(query)
                existiert=sparql.query().convert()
                if not existiert['boolean']:    #Falls ein davon existiert nicht, bekommen wir eine Meldung
                    return HttpResponse("Das Gebiet %s bei Interesse existiert nicht." % i)
        else:
            query = """
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                    PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                    ASK  { 
                      dom:%s rdf:type ?p .
                      FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                      dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                    }
                                """ % interesse
            sparql.setQuery(query)
            existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
            if not existiert['boolean']:
                return HttpResponse("Das Gebiet %s bei Interesse existiert nicht." % interesse)
    except KeyError:
        hatInteresse = False
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist aufgetaucht!")
    try:
        knowledge=body["knowledge"]                 #Bei Knowledge passiert das gleiche wie bei Interesse
        if type(knowledge) is list:
            for k in knowledge:
                query="""
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                    PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                    ASK  { 
                      dom:%s rdf:type ?p .
                      FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                      dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                    }
                """ % k
                sparql.setQuery(query)
                existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
                if not existiert['boolean']:
                    return HttpResponse("Das Gebiet %s bei Knowledge existiert nicht." % k)
        else:
            query = """
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                    PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                    ASK  { 
                      dom:%s rdf:type ?p .
                      FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                      dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                    }
                                """ % knowledge
            sparql.setQuery(query)
            existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
            if not existiert['boolean']:
                return HttpResponse("Das Gebiet %s bei Knowledge existiert nicht." % knowledge)
    except KeyError:
        hatKnowledge = False
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist aufgetaucht!")
    sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")     #Wenn alle in Orndung mit Daten ist, umstellen wir
                                            # den SPARQL-Endpoint zu upadet stelle
                                            #Das erste Teil von Query ist fix: wir geben den neu URI und ID ein
    sparql.method = 'POST'  #Die SPARQL-Abfragen werden als GET-Anforderung gesendet, aber das UPDATE erfordert, dass
                            # die Abfrage als POST-Anforderung gesendet wird.
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            INSERT DATA 
            { kic:%s rdf:type kic:User;
                     kic:hasID "%s"^^xsd:string """ % (name, id)
    if hatInteresse:                        #Falls der User hat Interesse, fügen wir zu Query hinzu
        if type(interesse) is list:
            for i in interesse:
                query+="""    ;
                kic:hasInterests dom:%s """ % i
        else:
            query += """;
             kic:hasInterests dom:%s """ % interesse
    if hatKnowledge:                        #Falls der User hat Knowledge, fügen wir zu Query hinzu
        if type(knowledge) is list:
            for k in knowledge:
                query+= """    ;
                kic:hasKnowledge dom:%s """ % k
        else:
            query+= """;
             kic:hasKnowledge dom:%s """ % knowledge
                                            #Kommt das Ende von Query
    query+=""". 
        }"""
    sparql.setQuery(query)
    try:
        sparql.query()                      #Query ausführen
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist aufgetaucht!")
                                            #Fall wir keines Exception bekommen Abfragen wir den neulich geschpeicherten User
    sparql = SPARQLWrapper(fuseki, returnFormat="json")     #Dazu stellen wir den Endpoint zu normal Abfragestellung zurück
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?user ?id ?interesse ?knowledge
            WHERE {
              {
              ?user rdf:type kic:User .
              ?user kic:hasID  "%s"^^xsd:string .  
              ?user kic:hasID ?id .
                OPTIONAL {
                    ?user kic:hasInterests ?interesse .
                    }
              }
            UNION
              {
                OPTIONAL{
                    ?user rdf:type kic:User .
                    ?user kic:hasID  "%s"^^xsd:string .  
                    ?user kic:hasID ?id .
                    ?user kic:hasKnowledge ?knowledge
              }    
            }
            }

 """ % (id, id)
    sparql.setQuery(query)
    try:
        user = sparql.query()
        return HttpResponse(user)       #Es kommt mit den nuelich angelegte Userobjekt zurück
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei Datenausgabe ist ein Fehler aufgetaucht!")



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def newKurs(request):
    """
    Legt einen neuen Kurs in der Ontologie an. Die Methode wird aufgerufen, wenn ein POST Request an die
    URL "<base_URL>/kurs/" gesendet wird.
    Die Informationen für den anzulegenden Kurs werden aus dem Body ausgelesen.
    Parameter:
    - request: Das Anfrageobjekt
    - Body: id, kursname, contentTags
    Return-Wert:
    Kursobjekt wenn es angelegt wurde oder Fehlermeldung
    Wirft Exceptions:
    - urllib.error.URLError - wenn den SPARQL-Endpoint nicht erreichbar
    - KeyError - Wenn ein Wert von Body Fehlt
    - allgemeinen Exception
    """
    if request.method != 'POST':
        return HttpResponse("An diese URL darf nur POST-Anfrage gesendet werden")
    sparql = SPARQLWrapper(fuseki, returnFormat="json")
    try:
        body_unicode = request.body.decode('utf-8')     #JSONFile von Body wird zu lesbare Daten umwandelt
        body = json.loads(body_unicode)                 #Die Daten von Body werden zu Variablen gespeichert
    except:
        return HttpResponse("Bei der Dateneingabe ist ein Fehler aufgetaucht!")
    try:                                            #wenn die nicht erreichbar sind, wirt einen Exception
        id = body["id"]
    except KeyError:
        return HttpResponse("ID fehlt!")            #kontrollieren, ob noch keine User mit dieser ID in Onotolgy angelegt geworden
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            ASK  { 
                ?uri rdf:type kic:LearningOffer .
                ?uri kic:hasID "%s"^^xsd:string
            }
        """ % id
    sparql.setQuery(query)                          #Querytext einstellen
    try:
        existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Datenkontrolle ist ein Fehler aufgetaucht!")
    if existiert['boolean']:                        #Falls diese ID schon existiert, kann den USer nicht angelegt werden
        return HttpResponse("Die ID %s hat schon ein Kurs." % id)
    try:
        name = body["name"]                         #gleiche wie oben mit dem URI
    except KeyError:
        return HttpResponse("URI fehlt!")           #Hier Prüfen wir nicht nur den LearningOffer Klasse, sondern die ganze Ontology
    query = """
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            ASK  { 
              kic:%s ?p ?o.
            } 
        """ % name
    sparql.setQuery(query)
    try:
        existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Datenkontrolle ist ein Fehler aufgetaucht!")
    if existiert['boolean']:
        return HttpResponse("Das URI %s existiert schon. Es muss ein unique sein." % name)
    try:
        contentTags = body["contentTags"]       #kann 1..n Stück Content Tags eingegeben werden. Je nach Liste oder String, muss
        if type(contentTags) is list:           #es anderes behandelt werden
            for c in contentTags:               #Bei ein Liste: kontrollieren wir alle Elemente, ob sie in Onto existieren
                query = """
                       PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                       PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                       PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                       ASK  { 
                         dom:%s rdf:type ?p .
                         FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                         dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                       }
                               """ % c
                sparql.setQuery(query)
                existiert = sparql.query().convert()
                if not existiert['boolean']:    #Falls ein davon existiert nicht, bekommen wir eine Meldung
                    return HttpResponse("Das Content Tag %s existiert nicht." % c)
        else:
            query = """
                       PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                       PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                       PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                       ASK  { 
                         dom:%s rdf:type ?p .
                         FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                         dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                       }
                   """ % contentTags
            sparql.setQuery(query)
            existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
            if not existiert['boolean']:
                return HttpResponse("Das Content Tag %s existiert nicht." % contentTags)
    except KeyError:
        return HttpResponse("Geben Sie mindestens ein Content Tag ein!")
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Datenkontrolle ist ein Fehler aufgetaucht!")
    hatPrereqisites=True            #Weil Prereuistes nicht Pflichtfeld ist, muss man kontrollieren, ob sie in
                                    # JSON Daten existieren. falls nein, wird KeyError Exception werfen, und
    try:                            #den bestimte Variable False stellen
        prerequisites = body["prerequisites"]
        if type(prerequisites) is list:     #kann 0..n Stück Prerequisites eingegeben werden. Je nach Liste oder
                                            # String, muss es anderes behandelt werden
            for p in prerequisites:         #Bei ein Liste: kontrollieren wir alle Elemente, ob sie in Onto existieren
                query="""
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                    PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                    ASK  { 
                      dom:%s rdf:type ?p .
                      FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                      dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                    }
                """ % p
                sparql.setQuery(query)
                existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
                if not existiert['boolean']:    #Falls ein davon existiert nicht, bekommen wir eine Meldung
                    return HttpResponse("Das Gebiet %s bei Prereqisites existiert nicht." % p)
        else:
            query = """
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                    PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                    ASK  { 
                      dom:%s rdf:type ?p .
                      FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                      dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                    }
                                """ % prerequisites
            sparql.setQuery(query)
            existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
            if not existiert['boolean']:
                return HttpResponse("Das Gebiet %s bei Prereqisites existiert nicht." % prerequisites)
    except KeyError:
        hatPrereqisites = False
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Dateneingabe ist ein Fehler aufgetaucht!")
    sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")  #Wenn alle in Orndung mit Daten ist, umstellen wir
                                            # den SPARQL-Endpoint zu upadet stelle
                                            #Das erste Teil von Query ist fix: wir geben den neu URI und ID ein
    sparql.method = 'POST'  # Die SPARQL-Abfragen werden als GET-Anforderung gesendet, aber das UPDATE erfordert, dass
    # die Abfrage als POST-Anforderung gesendet wird.
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            INSERT DATA 
            { kic:%s rdf:type kic:LearningOffer;
                     kic:hasID "%s"^^xsd:string """ % (name, id)
    if type(contentTags) is list:           #Wir fügen den Content Tag(s) hinzu
        for c in contentTags:
            query += """    ;
            kic:hasContentTags dom:%s """ % c
    else:
        query += """;
         kic:hasContentTags dom:%s """ % contentTags
    if hatPrereqisites:                      #Falls der Kurs hat prereuisites, fügen wir zu Query hinzu
        if type(prerequisites) is list:
            for p in prerequisites:
                query += """    ;
                kic:hasPrerequisites dom:%s """ % p
        else:
            query += """;
             kic:hasPrerequisites dom:%s """ % prerequisites    #Kommt das Ende von Query
    query += """.                           
        }"""
    sparql.setQuery(query)
    try:
        sparql.query()                  #Query ausführen
                                        #Fall wir keines Exception bekommen Abfragen wir den neulich geschpeicherten Kurs
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist aufgetaucht!")
    sparql = SPARQLWrapper(fuseki, returnFormat="json")
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?learningOffer ?id ?contentTag ?prerequitsute
            WHERE {
              {
              ?learningOffer rdf:type kic:LearningOffer . 
              ?learningOffer kic:hasID "%s"^^xsd:string .
              ?learningOffer kic:hasID ?id .
              ?learningOffer kic:hasContentTags ?contentTag .
                    }
            UNION
              {
                OPTIONAL{
                    ?learningOffer rdf:type kic:LearningOffer .
                    ?learningOffer kic:hasID "%s"^^xsd:string .
                    ?learningOffer kic:hasID ?id .
                    ?learningOffer kic:hasPrerequisites ?prerequitsute
              }    
            }
            }

 """ % (id, id)
    sparql.setQuery(query)
    try:
        kurs = sparql.query()
        return HttpResponse(kurs)  # Es kommt mit den nuelich angelegte Kursobjekt zurück
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist bei der Ausgabe des neues Anwenderes aufgetaucht! ")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def newLecturer(request):
    """
    Legt einen neuen Dozent in der Ontologie an. Die Methode wird aufgerufen, wenn ein POST Request an die
    URL "<base_URL>/lecturer/" gesendet wird.
    Die Informationen für den anzulegenden Dozent werden aus dem Body ausgelesen.
    Parameter:
    - request: Das Anfrageobjekt
    - Body: id, name, [expertise]
    Return-Wert:
    Lecturerobjekt wenn es angelegt wurde oder Fehlermeldung
    Wirft Exceptions:
    - urllib.error.URLError - wenn den SPARQL-Endpoint nicht erreichbar
    - KeyError - Wenn ein Wert von Body Fehlt
    - allgemeinen Exception
    """
    if request.method != 'POST':
        return HttpResponse("An diese URL darf nur POST-Anfrage gesendet werden")
    sparql = SPARQLWrapper(fuseki, returnFormat="json")
    try:
        body_unicode = request.body.decode('utf-8') #JSONFile von Body wird zu lesbare Daten umwandelt
        body = json.loads(body_unicode)
    except:
        return HttpResponse("Bei der Dateneingabe ist ein Fehler aufgetaucht!")
    try:                                        #Die Daten von Body werden zu Variablen gespeichert
        id=body["id"]                           #wenn die nicht erreichbar sind, wirt einen Exception
    except KeyError:
        return HttpResponse("ID fehlt!")        #kontrollieren, ob noch keine User mit dieser ID in Onotolgy angelegt geworden
    query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        ASK  { 
                            ?uri rdf:type kic:Lecturer .
                            ?uri kic:hasID "%s"^^xsd:string
                        }
                    """ % id
    sparql.setQuery(query)                      #Querytext einstellen
    try:
        existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
        if existiert['boolean']:                    #Falls diese ID schon existiert, kann den USer nicht angelegt werden
            return HttpResponse("Die ID %s hat schon ein Dozent." % id)
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Datenkontrolle ist ein Fehler aufgetaucht!")
    try:                                        #gleiche wie oben mit dem URI
        name = body["name"]
    except KeyError:
        return HttpResponse("URI fehlt!")       #Hier Prüfen wir nicht nur den Lectuter Klasse, sondern die ganze Ontology
    query = """
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        ASK  { 
                          kic:%s ?p ?o.
                        } 
                    """ % name
    sparql.setQuery(query)
    try:
        existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
        if existiert['boolean']:
            return HttpResponse("Das URI %s existiert schon. Es muss ein unique sein." % name)
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Datenkontrolle ist ein Fehler aufgetaucht!")
    hatExpertise=True                       #Weil Expertises nicht Pflichtfelden sind, muss man kontrollieren,
    try:                                    #ob sie in JSON Daten existieren. falls nein, wird KeyError Exception werfen, und
        expertise = body["expertise"]       #den bestimte Variable False stellen
        if type(expertise) is list:         #kann 0..n Stück Expertise eingegeben werden. Je nach Liste oder String, muss
                                            #es anderes behandelt werden
            for e in expertise:             #Bei ein Liste: kontrollieren wir alle Elemente, ob sie in Onto existieren
                query = """
                       PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                       PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                       PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                       ASK  { 
                         dom:%s rdf:type ?p .
                         FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                         dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                       }
                               """ % e
                sparql.setQuery(query)
                existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
                if not existiert['boolean']:            #Falls ein davon existiert nicht, bekommen wir eine Meldung
                    return HttpResponse("Das Expertise %s existiert nicht." % e)
        else:
            query = """
                       PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                       PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                       PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                       ASK  { 
                         dom:%s rdf:type ?p .
                         FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                         dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                       }
                                   """ % expertise
            sparql.setQuery(query)
            existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
            if not existiert['boolean']:
                return HttpResponse("Das Expertise %s existiert nicht." % expertise)
    except KeyError:
        hatExpertise = False
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Datenkontrolle ist ein Fehler aufgetaucht!")
    sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")     #Wenn alle in Orndung mit Daten ist, umstellen wir
                                            # den SPARQL-Endpoint zu upadet stelle
                                            #Das erste Teil von Query ist fix: wir geben den neu URI und ID ein
    sparql.method = 'POST'  # Die SPARQL-Abfragen werden als GET-Anforderung gesendet, aber das UPDATE erfordert, dass
                            # die Abfrage als POST-Anforderung gesendet wird.
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            INSERT DATA 
            { kic:%s rdf:type kic:Lecturer;
                     kic:hasID "%s"^^xsd:string """ % (name, id)
    if hatExpertise:                    #Falls der Dozent hat Expertise, fügen wir zu Query hinzu
        if type(expertise) is list:
            for e in expertise:
                query += """    ;
                kic:hasExpertise dom:%s """ % e
        else:
            query += """;
             kic:hasExpertise dom:%s """ % expertise        #Kommt das Ende von Query
    query += """. 
        }"""
    sparql.setQuery(query)
    try:
        sparql.query()                      #Query ausführen
                                            #Fall wir keines Exception bekommen Abfragen wir den neulich geschpeicherten
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist aufgetaucht!")
    sparql = SPARQLWrapper(fuseki, returnFormat="json")     #Dazu stellen wir den Endpoint zu normal Abfragestellung
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?lecturer ?id ?expertise
            WHERE {
              ?lecturer rdf:type kic:Lecturer . 
              ?lecturer kic:hasID "%s"^^xsd:string .
              ?lecturer kic:hasID ?id .
                OPTIONAL{
                    ?lecturer kic:hasExpertise ?expertise
              }    
            }

    """ % (id)
    sparql.setQuery(query)
    try:
        lecturer = sparql.query()
        return HttpResponse(lecturer)       #Es kommt mit den nuelich angelegte Lecturerobjekt zurück
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist bei der Ausgabe des neues Kurses aufgetaucht!")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def newLearningItem(request):
    """
    Legt einen neuen Learning Item in der Ontologie an. Die Methode wird aufgerufen, wenn ein POST Request an die
    URL "<base_URL>/learning_item/" gesendet wird.
    Die Informationen für den anzulegenden Learning Item werden aus dem Body ausgelesen.
    Parameter:
    - request: Das Anfrageobjekt
    - Body: id, name, contentTags
    Return-Wert:
    LearningItemobjekt wenn es angelegt wurde oder Fehlermeldung
    Wirft Exceptions:
    - urllib.error.URLError - wenn den SPARQL-Endpoint nicht erreichbar
    - KeyError - Wenn ein Wert von Body Fehlt
    - allgemeinen Exception
    """
    if request.method != 'POST':
        return HttpResponse("An diese URL darf nur POST-Anfrage gesendet werden")
    sparql = SPARQLWrapper(fuseki, returnFormat="json")
    try:
        body_unicode = request.body.decode('utf-8')     #JSONFile von Body wird zu lesbare Daten umwandelt
        body = json.loads(body_unicode)
    except:
        return HttpResponse("Bei der Dateneingabe ist ein Fehler aufgetaucht!")
    try:                                            #Die Daten von Body werden zu Variablen gespeichert
        id = body["id"]                             #wenn die nicht erreichbar sind, wirt einen Exception
    except KeyError:
        return HttpResponse("ID fehlt!")            #kontrollieren, ob noch keine User mit dieser ID in Onotolgy angelegt
    query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        ASK  { 
                            ?uri rdf:type kic:LearningItem .
                            ?uri kic:hasID "%s"^^xsd:string
                        }
                    """ % id
    sparql.setQuery(query)                          #Querytext einstellen
    try:
        existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
        if existiert['boolean']:                        #Falls diese ID schon existiert, kann den USer nicht angelegt werden
            return HttpResponse("Die ID %s hat schon ein Learning Item." % id)
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Datenkontrolle ist ein Fehler aufgetaucht!")
    try:                                            #gleiche wie oben mit dem URI
        name = body["name"]
    except KeyError:
        return HttpResponse("URI fehlt!")           #Hier Prüfen wir nicht nur den LearningItem Klasse, sondern die ganze Ontolog
    query = """
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        ASK  { 
                          kic:%s ?p ?o.
                        } 
                    """ % name
    sparql.setQuery(query)
    try:
        existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
        if existiert['boolean']:
            return HttpResponse("Das URI %s existiert schon. Es muss ein unique sein." % name)
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Datenkontrolle ist ein Fehler aufgetaucht!")
    try:
        contentTags = body["contentTags"]   #Weil ContentTags ein Pflichtfelden ist, muss man kontrollieren,
                                            # ob sie in JSON Daten existieren. falls nein, wird KeyError Exception
                                            #werfen, und Fehlermeldung geben
        if type(contentTags) is list:       #kann 1..n Stück Interesse eingegeben werden. Je nach Liste oder String, muss
                                            #es anderes behandelt werden
            for c in contentTags:           #Bei ein Liste: kontrollieren wir alle Elemente, ob sie in Onto existieren
                query = """
                       PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                       PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                       PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                       ASK  { 
                         dom:%s rdf:type ?p .
                         FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                         dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                       }
                   """ % c
                sparql.setQuery(query)
                existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
                if not existiert['boolean']:        #Falls ein davon existiert nicht, bekommen wir eine Meldung
                    return HttpResponse("Das Content Tag %s existiert nicht." % c)
        else:
            query = """
                       PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                       PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                       PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                       ASK  { 
                         dom:%s rdf:type ?p .
                         FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                         dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                       }
                                   """ % contentTags
            sparql.setQuery(query)
            existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
            if not existiert['boolean']:
                return HttpResponse("Das Content Tag %s existiert nicht." % contentTags)
    except KeyError:
        return HttpResponse("Geben Sie mindestens ein Content Tag ein!")
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Datenkontrolle ist ein Fehler aufgetaucht!")
    sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")     #Wenn alle in Orndung mit Daten ist, umstellen wir
                                            # den SPARQL-Endpoint zu upadet stelle
                                            #Das erste Teil von Query ist fix: wir geben den neu URI und ID ein
    sparql.method = 'POST'  # Die SPARQL-Abfragen werden als GET-Anforderung gesendet, aber das UPDATE erfordert, dass
                            # die Abfrage als POST-Anforderung gesendet wird.
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            INSERT DATA 
            { kic:%s rdf:type kic:LearningItem;
                     kic:hasID "%s"^^xsd:string """ % (name, id)
    if type(contentTags) is list:                           #wir fügen die Content Tags zu Query hinzu
        for c in contentTags:
            query += """    ;
            kic:hasContentTags dom:%s """ % c
    else:
        query += """;
         kic:hasContentTags dom:%s """ % contentTags        #Kommt das Ende von Query
    query += """. 
        }"""
    sparql.setQuery(query)
    try:
        sparql.query()              #Query ausführen
                                    #Fall wir keines Exception bekommen Abfragen wir den neulich geschpeicherten LearningItem
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist aufgetaucht!")
    sparql = SPARQLWrapper(fuseki, returnFormat="json") #Dazu stellen wir den Endpoint zu normal Abfragestellung zurück
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?learningItem ?id ?contentTags
            WHERE {
              ?learningItem rdf:type kic:LearningItem . 
              ?learningItem kic:hasID "%s"^^xsd:string .
              ?learningItem kic:hasID ?id .
              ?learningItem kic:hasContentTags ?contentTags
            }

 """ % (id)
    sparql.setQuery(query)
    try:
        leaningItem = sparql.query()
        return HttpResponse(leaningItem)    #Es kommt mit den nuelich angelegte LearningItemobjekt zurück
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist bei der Ausgabe des neues LearningItems aufgetaucht! ")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def userUpdateDelete(request, id):
    """
    PUT:
    Verändert die Danten von einen User in der Ontologie an. Die Methode wird aufgerufen, wenn ein
    PUT Request an die URL "<base_URL>/user/<id>" gesendet wird.
    Die Informationen für den veränderenden User werden aus dem Body ausgelesen.
    Parameter:
    - request: Das Anfrageobjekt
    - Body: id, [interesse], [kenntnisse]
    - id: ID des Users, dessen Daten Verändern wollen
    Return-Wert:
    Erfolgmeldung oder Fehlermeldung
    Wirft Exceptions:
    - urllib.error.URLError - wenn den SPARQL-Endpoint nicht erreichbar
    - KeyError - Wenn ein Wert von Body Fehlt
    - allgemeinen Exception

    DELETE:
    Löscht einen User aus der Ontologie. Die Methode wird aufgerufen, wenn ein
    DELETE Request an die URL "<base_URL>/user/<id>" gesendet wird.
    Parameter:
    - request: Das Anfrageobjekt
    - id: ID des Users, der löschen werden muss
    Return-Wert:
    Erfolgmeldung oder Fehlermeldung
    Wirft Exceptions:
    - urllib.error.URLError - wenn den SPARQL-Endpoint nicht erreichbar
    - KeyError - Wenn ein Wert von Body Fehlt
    - allgemeinen Exception
    """

    sparql = SPARQLWrapper(fuseki, returnFormat="json")     #kontrollieren, dass mit in der Variable id geschpeicherten
                                                            #id einen user in Ontology existiert
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            ASK  { 
              ?x rdf:type kic:User .
              ?x kic:hasID "%s"^^xsd:string 
            }
            """ % id
    sparql.setQuery(query)
    try:
        hatUser= sparql.query().convert()       # Query ausführen un den Ergebnis in ein Variablen speichern
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Idskontrolle ist ein Fehler aufgetaucht!")

    if request.method == 'PUT':
        if not hatUser['boolean']:              # Falls nicht, kommt mit ein Fehlermeldung zurück
            return HttpResponse("Es gibt keinen User mit dem ID %s" % id)
        try:
            body_unicode = request.body.decode('utf-8')     #JSONFile von Body wird zu lesbare Daten umwandelt
            body = json.loads(body_unicode)                 #Bei User kann mann nur die Interesse und die Knowledge verändern
        except urllib.error.URLError:
            return HttpResponse("Endpoint ist nicht erreichbar!")
        except EndPointNotFound:
            return HttpResponse("Datensatz fehlt!")
        except:
            return HttpResponse("Bei der Dateneingabe ist ein Fehler aufgetaucht!")
        hatInteresse = True                     #Weil Interesse und Knowledge nicht Pflichtfelden sind, muss man kontrollieren,
        hatKnowledge = True                     #ob sie in JSON Daten existieren. falls nein, wird KeyError Exception werfen, und
        try:                                    #den bestimte Variable False stellen
            interesse = body["interesse"]
            if type(interesse) is list:         #kann 0..n Stück Interesse eingegeben werden. Je nach Liste oder String, muss
                                                #es anderes behandelt werden
                for i in interesse:             #Bei ein Liste: kontrollieren wir alle Elemente, ob sie in Onto existieren
                    query = """
                            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                            PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                            ASK  { 
                              dom:%s rdf:type ?p .
                              FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                              dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                            }
                        """ % i
                    sparql.setQuery(query)
                    existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
                    if not existiert['boolean']:        #Falls ein davon existiert nicht, bekommen wir eine Meldung
                        return HttpResponse("Das Gebiet %s bei Interesse existiert nicht." % i)
            else:
                query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        ASK  { 
                          dom:%s rdf:type ?p .
                          FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                          dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                        }
                                    """ % interesse
                sparql.setQuery(query)
                existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
                if not existiert['boolean']:
                    return HttpResponse("Das Gebiet %s bei Interesse existiert nicht." % interesse)
        except KeyError:
            hatInteresse = False
        except urllib.error.URLError:
            return HttpResponse("Endpoint ist nicht erreichbar!")
        except EndPointNotFound:
            return HttpResponse("Datensatz fehlt!")
        except:
            return HttpResponse("Bei der Datenkontrolle ist ein Fehler aufgetaucht!")
        try:
            knowledge = body["knowledge"]       #Bei Knowledge passiert das gleiche wie bei Interesse
            if type(knowledge) is list:
                for k in knowledge:
                    query = """
                            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                            PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                            ASK  { 
                              dom:%s rdf:type ?p .
                              FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                              dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                            }
                        """ % k
                    sparql.setQuery(query)
                    existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
                    if not existiert['boolean']:
                        return HttpResponse("Das Gebiet %s bei Knowledge existiert nicht." % k)
            else:
                query = """
                                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                                PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                                ASK  { 
                                  dom:%s rdf:type ?p .
                                  FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                                  dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                                }
                                            """ % knowledge
                sparql.setQuery(query)
                existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
                if not existiert['boolean']:
                    return HttpResponse("Das Gebiet %s bei Knowledge existiert nicht." % knowledge)
        except KeyError:
            hatKnowledge = False
        except urllib.error.URLError:
            return HttpResponse("Endpoint ist nicht erreichbar!")
        except EndPointNotFound:
            return HttpResponse("Datensatz fehlt!")
        except:
            return HttpResponse("Bei der Datenkontrolle ist ein Fehler aufgetaucht!")
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")     #Wenn alle in Orndung mit Daten ist, umstellen wir
                                                # den SPARQL-Endpoint zu update
                                                #Das erste Teil von Query ist fix: wir geben den neu URI und ID ein
        sparql.method = 'POST'  # Die SPARQL-Abfragen werden als GET-Anforderung gesendet, aber das UPDATE erfordert, dass
                                # die Abfrage als POST-Anforderung gesendet wird.
        query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        DELETE {
                          ?user kic:hasInterests ?interesse ;
                                kic:hasKnowledge ?knowledge
                        }"""
        if (hatInteresse or hatKnowledge):      #Falls der User hat neue Interesse oder Knowledge, kommt ein INSERT Teil in SPARQL
            query += """INSERT { """
            if hatInteresse:
                if type(interesse) is list:     #neu(e) Interssse(n) hinzufügen
                    for i in interesse:
                        query+="""?user kic:hasInterests dom:%s . """ % i
                else:
                    query += """?user kic:hasInterests  dom:%s . """ % interesse
            if hatKnowledge:                    #neu(e) Kowledge(s) hinzufügen
                if type(knowledge) is list:
                    for k in knowledge:
                        query += """?user kic:hasKnowledge dom:%s . """ % k
                else:
                    query += """?user kic:hasKnowledge  dom:%s . """ % knowledge
                                #Kommt das Ende von Query, der WHERE Klausur.
                                #Hier sagen wir zu fuseki, von welchen User muss die Interesse und Knowledes gelöscht werden
            query += """}"""
        query +=   """WHERE { 
                      ?user rdf:type kic:User .
                      ?user kic:hasID ?id .
                      FILTER( ?id ="%s"^^xsd:string) .
                      OPTIONAL {
                      ?user kic:hasInterests ?interesse .
                        }
                      OPTIONAL {
                      ?user kic:hasKnowledge ?knowledge .
                      }
                    } """ % id

        sparql.setQuery(query)
        try:
            sparql.query()          #Wenn der Query ohne Exception durchgeht, kommt mir Erfogsmeldung zurück
            return HttpResponse("Update des Users mit ID %s ist erfolgreich." % id)
        except Unauthorized:
            return HttpResponse("Sie haben keinen Zugriff auf die angeforderten Daten")
        except urllib.error.URLError:
            return HttpResponse("Endpoint ist nicht erreichbar!")
        except:
            return HttpResponse("Ein Fehler ist aufgetaucht!")

    elif request.method == 'DELETE':
        if not hatUser['boolean']:              # Falls nicht, kommt mit ein Fehlermeldung zurück
            return HttpResponse("Es gibt keinen User mit dem ID %s" % id)
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")  # stellen wir den SPARQL-Endpoint zu update um
                                                        # Der Query löscht alle Tripleten von User mit den eingegebene ID
        sparql.method = 'POST'  # Die SPARQL-Abfragen werden als GET-Anforderung gesendet, aber das UPDATE erfordert, dass
                                # die Abfrage als POST-Anforderung gesendet wird.
        query = """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                DELETE {?user ?p ?o} 
                WHERE {
                    ?user rdf:type kic:User .
                    ?user kic:hasID ?id .
                    FILTER ( ?id = "%s"^^xsd:string )
                    ?user ?p ?o
                }
                 """ % id
        sparql.setQuery(query)
        try:
            sparql.query()                                              # Kommt mit Erfolg- oder mit Fehlermeldung zurück
            return HttpResponse("Der User mit ID %s erfolgreich entfernt worden." % id)
        except urllib.error.URLError:
            return HttpResponse("Endpoint ist nicht erreichbar!")
        except EndPointNotFound:
            return HttpResponse("Datensatz fehlt!")
        except:
            return HttpResponse("Ein Fehler ist aufgetaucht!")
    else:
        return HttpResponse("An diese URL darf nur PUT- und DELETE-Anfrage gesendet werden")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def lecturerUpdate(request, id):
    """
    Verändert die Danten von einen Dozent in der Ontologie an. Die Methode wird aufgerufen, wenn ein
    PUT Request an die URL "<base_URL>/lecturer/<id>" gesendet wird.
    Die Informationen für den veränderenden Dozentwerden aus dem Body ausgelesen.
    Parameter:
    - request: Das Anfrageobjekt
    - Body: id, name, [expertisse]
    - id: ID des Dozents, dessen Daten Verändern wollen
    Return-Wert:
    Erfolgmeldung oder Fehlermeldung
    Wirft Exceptions:
    - urllib.error.URLError - wenn den SPARQL-Endpoint nicht erreichbar
    - KeyError - Wenn ein Wert von Body Fehlt
    - allgemeinen Exception
    """
    if request.method != 'PUT':
        return HttpResponse("An diese URL darf nur PUT-Anfrage gesendet werden")
    sparql =SPARQLWrapper(fuseki, returnFormat="json")  #kontrollieren, dass mit in der Variable id geschpeicherten
                                                        #id einen Dozent in Ontology existiert
    query="""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
            PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            ASK  { 
              ?x rdf:type kic:Lecturer .
              ?x kic:hasID "%s"^^xsd:string 
            }
    """ % id
    sparql.setQuery(query)
    try:
        hatLehrer = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
        if not hatLehrer['boolean']:         #Falls nicht, kommt mit ein Fehlermeldung zurück
            return HttpResponse("Es gibt keinen Lehrer mit dem ID %s" % id)
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Idskontrolle ist ein Fehler aufgetaucht!")
    sparql = SPARQLWrapper(fuseki, returnFormat="json")
    try:
        body_unicode = request.body.decode('utf-8')     #JSONFile von Body wird zu lesbare Daten umwandelt
        body = json.loads(body_unicode)             #Bei Dozenten kann mann nur die Expertisse verändern
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Dateneingabe ist ein Fehler aufgetaucht!")
    hatExpertise = True                         #Weil Expertise nicht Pflichtfelden ist, muss man kontrollieren,
                                                #ob sie in JSON Daten existieren. falls nein, wird KeyError Exception werfen, und
    try:                                        #den hatExpertise Variable False stellen
        expertise = body["expertise"]
        if type(expertise) is list:             #kann 0..n Stück Interesse eingegeben werden. Je nach Liste oder String, muss
                                                #es anderes behandelt werden
            for e in expertise:                 #Bei ein Liste: kontrollieren wir alle Elemente, ob sie in Onto existieren
                query = """
                       PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                       PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                       PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                       ASK  { 
                         dom:%s rdf:type ?p .
                         FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                         dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                       }
                                   """ % e
                sparql.setQuery(query)
                existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
                if not existiert['boolean']:    #Falls ein davon nicht existiert, bekommen wir eine Meldung
                    return HttpResponse("Das Content Tag %s existiert nicht." % e)
        else:
            query = """
                       PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                       PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                       PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                       ASK  { 
                         dom:%s rdf:type ?p .
                         FILTER(?p IN (dom:Field, dom:Topic, dom:Subtopic, dom:Theme, dom:Method, 
                         dom:ApplicationArea, dom:Application, dom:InterdisciplinaryTopic))
                       }
                                                       """ % expertise
            sparql.setQuery(query)
            existiert = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
            if not existiert['boolean']:
                return HttpResponse("Das Expertise %s existiert nicht." % expertise)
    except KeyError:
        hatExpertise = False
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Bei der Datenkontrolle ist ein Fehler aufgetaucht!")

    sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")     #Wenn alle in Orndung mit Daten ist, stellen wir
                                            # den SPARQL-Endpoint zu update um
                                            #Das erste Teil von Query ist fix: Löschen wir alle Expertise von Docent aus
    sparql.method = 'POST'  # Die SPARQL-Abfragen werden als GET-Anforderung gesendet, aber das UPDATE erfordert, dass
                            # die Abfrage als POST-Anforderung gesendet wird.
    query = """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                DELETE {
                  ?lecturer kic:hasExpertise ?expertise 
                }"""
    if (hatExpertise):
        query += """INSERT { """
        if type(expertise) is list:     #Falls der Dozent hat Expertise bekommen, kommt ein INSERT Teil in SPARQL
            for e in expertise:
                query += """?lecturer kic:hasExpertise dom:%s . """ % e
        else:
            query += """?lecturer kic:hasExpertise  dom:%s . """ % expertise
                            # Kommt das Ende von Query, der WHERE Klausur.
                            # Hier sagen wir zu fuseki, von welchen Dozent muss die Expertise gelöscht werden
        query += """}"""
    query += """WHERE { 
                      ?lecturer rdf:type kic:Lecturer .
                      ?lecturer kic:hasID ?id .
                      FILTER( ?id ="%s"^^xsd:string) .
                      OPTIONAL {
                      ?lecturer kic:hasExpertise ?expertise .
                        }
                    } """ % id
    sparql.setQuery(query)
    try:
        sparql.query()
        return HttpResponse("Update des Lecturers mit ID %s ist erfolgreich." % id)
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist aufgetaucht!")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def learningItemDelete(request, id):
    """
    Löscht einen Learning Item aus der Ontologie. Die Methode wird aufgerufen, wenn ein
    DELETE Request an die URL "<base_URL>/learning_item/<id>" gesendet wird.
    Parameter:
    - request: Das Anfrageobjekt
    - id: ID des Learning Items, der löschen werden muss
    Return-Wert:
    Erfolgmeldung oder Fehlermeldung
    Wirft Exceptions:
    - urllib.error.URLError - wenn den SPARQL-Endpoint nicht erreichbar
    - KeyError - Wenn ein Wert von Body Fehlt
    - allgemeinen Exception
    """
    if request.method!="DELETE":
        return HttpResponse("An diese URL darf nur DELETE-Anfrage gesendet werden")
    sparql = SPARQLWrapper(fuseki, returnFormat="json")     #kontrollieren, dass mit in der Variable id geschpeicherten
                                                            #id einen LearningItem in Ontology existiert
    query = """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                ASK  { 
                  ?x rdf:type kic:LearningItem .
                  ?x kic:hasID "%s"^^xsd:string 
                }
            """ % id
    sparql.setQuery(query)
    try:
        hatLearningItem = sparql.query().convert()  # Query ausführen un den Ergebnis in ein Variablen speichern
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist aufgetaucht!")
    if not hatLearningItem['boolean']:                      #Falls nicht, kommt mit ein Fehlermeldung zurück
        return HttpResponse("Es gibt keinen Learning Item mit dem ID %s" % id)
    sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")     #stellen wir den SPARQL-Endpoint zu update um
                                                    #Der Query löscht alle Tripleten von LearningItem mit den eingegebene ID
    sparql.method = 'POST'  # Die SPARQL-Abfragen werden als GET-Anforderung gesendet, aber das UPDATE erfordert, dass
                            # die Abfrage als POST-Anforderung gesendet wird.
    query = """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                DELETE {?learningItem ?p ?o} 
                WHERE {
                    ?learningItem rdf:type kic:LearningItem .
                    ?learningItem kic:hasID ?id .
                    FILTER ( ?id = "%s"^^xsd:string )
                    ?learningItem ?p ?o
                }
 
     """ % id
    sparql.setQuery(query)
    try:
        sparql.query()                                      #Kommt mit Erfolg- oder mit Fehlermeldung zurück
        return HttpResponse("Das Learning Item mit ID %s erfolgreich entfernt worden." % id)
    except urllib.error.URLError:
        return HttpResponse("Endpoint ist nicht erreichbar!")
    except EndPointNotFound:
        return HttpResponse("Datensatz fehlt!")
    except:
        return HttpResponse("Ein Fehler ist aufgetaucht!")

