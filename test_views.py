import json
import urllib

from SPARQLWrapper import SPARQLWrapper
from django.test import TestCase, Client
from django.urls import reverse
import unittest
fuseki = "http://localhost:3030/data"  #Adresse von Fuseki-Endpoint
unittest.TestLoader.sortTestMethodsUsing = None

class TestViews(TestCase):


    def setUp(self):
        self.client = Client()
        self.newUser_url = reverse('kb_service:newUser')
        self.newKurs_url = reverse('kb_service:newKurs')
        self.newLecturer_url = reverse('kb_service:newLecturer')
        self.newLearningItem_url = reverse('kb_service:newLearningItem')

# -----------Tests zu newUser-----------------
    def test_newUser_POST_guteDaten_IdName(self):  # gute Daten, nur id, name
        """Es erschafft einen neuen User mit bestimmten ID und URI.
            Status Code -	200
            Returnwert	- Neuer User
            """
        user = {
            "id": "1",
            "name": "T1"
        }
        erwartete = json.dumps({"head": {
            "vars": ["user", "id", "interesse", "knowledge"]
        },
            "results": {
                "bindings": [
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T1"},
                        "id": {"type": "literal", "value": "1"}
                    },
                    {
                    }
                ]
            }
        })
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals((result), json.loads(erwartete))

    def test_newUser_POST_guteDaten_IdNameInteresse(self):
        """Es erschafft einen neuen User mit bestimmten ID,  URI und einen Interesse
            Status Code	- 200
	        Returnwert	- Neuer User
        """
        user = {
            "id": "2",
            "name": "T2",
            "interesse": "Logic"
        }
        erwartete = json.dumps({"head": {
            "vars": ["user", "id", "interesse", "knowledge"]
        },
            "results": {
                "bindings": [
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T2"},
                        "id": {"type": "literal", "value": "2"},
                        "interesse": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Logic"}
                    },
                    {
                    }
                ]
            }
        })
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals((result), json.loads(erwartete))

    def test_newUser_POST_guteDaten_IdNameInteresseListe(self):
        """Es erschafft einen neuen User mit bestimmten ID, URI und mehren Interessen
            Status Code	- 200
            Returnwert	Neuer User
        """
        user = {
            "id": "3",
            "name": "T3",
            "interesse": ["Logic", "Robotics", "Deep_Learning"]
        }
        erwartete = json.dumps({"head": {
            "vars": ["user", "id", "interesse", "knowledge"]
        },
            "results": {
                "bindings": [
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T3"},
                        "id": {"type": "literal", "value": "3"},
                        "interesse": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Robotics"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T3"},
                        "id": {"type": "literal", "value": "3"},
                        "interesse": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Deep_Learning"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T3"},
                        "id": {"type": "literal", "value": "3"},
                        "interesse": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Logic"}
                    },
                    {
                    }
                ]
            }
        })
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals((result), json.loads(erwartete))

    def test_newUser_POST_guteDaten_IdNameInteresseListeKnowledge(self):
        """Es erschafft einen neuen User mit bestimmten ID, URI, mehreren Interessen und einen Knowledges
            Status Code	- 200
            Returnwert	- Neuer User
        """
        user = {
            "id": "4",
            "name": "T4",
            "interesse": ["Logic", "Robotics", "Deep_Learning"],
            "knowledge": "Clustering"
        }
        erwartete = json.dumps({"head": {
            "vars": ["user", "id", "interesse", "knowledge"]
        },
            "results": {
                "bindings": [
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T4"},
                        "id": {"type": "literal", "value": "4"},
                        "interesse": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Robotics"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T4"},
                        "id": {"type": "literal", "value": "4"},
                        "interesse": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Deep_Learning"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T4"},
                        "id": {"type": "literal", "value": "4"},
                        "interesse": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Logic"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T4"},
                        "id": {"type": "literal", "value": "4"},
                        "knowledge": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Clustering"}
                    }
                ]
            }
        })
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals((result), json.loads(erwartete))

    def test_newUser_POST_guteDaten_IdNameInteresseListeKnowledgeListe(self):
        """Es erschafft einen neuen User mit bestimmten ID, URI, mehreren Interessen und mehreren Knowledges
        	Status Code	- 200
            Returnwert	- Neuer User
        """
        user = {
            "id": "5",
            "name": "T5",
            "interesse": ["Logic", "Robotics", "Deep_Learning"],
            "knowledge": ["Clustering", "Effector"]
        }
        erwartete = json.dumps({"head": {
            "vars": ["user", "id", "interesse", "knowledge"]
        },
            "results": {
                "bindings": [
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T5"},
                        "id": {"type": "literal", "value": "5"},
                        "interesse": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Robotics"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T5"},
                        "id": {"type": "literal", "value": "5"},
                        "interesse": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Deep_Learning"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T5"},
                        "id": {"type": "literal", "value": "5"},
                        "interesse": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Logic"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T5"},
                        "id": {"type": "literal", "value": "5"},
                        "knowledge": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Clustering"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T5"},
                        "id": {"type": "literal", "value": "5"},
                        "knowledge": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Effector"}
                    }
                ]
            }
        })
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals((result), json.loads(erwartete))

    def test_newUser_POST_guteDaten_IdNameKnowledge(self):
        """Es erschafft einen neuen User mit bestimmten ID, URI und einen Knowledge
            Status Code	- 200
            Returnwert	- Neuer User
        """
        user = {
            "id": "6",
            "name": "T6",
            "knowledge": "Effector"
        }
        erwartete = json.dumps({"head": {
            "vars": ["user", "id", "interesse", "knowledge"]
        },
            "results": {
                "bindings": [
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T6"},
                        "id": {"type": "literal", "value": "6"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T6"},
                        "id": {"type": "literal", "value": "6"},
                        "knowledge": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Effector"}
                    }
                ]
            }
        })
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals((result), json.loads(erwartete))

    def test_newUser_POST_guteDaten_IdNameKnowledgeListe(self):
        """Es erschafft einen neuen User mit bestimmten ID, URI und mehreren Knowledges
            Status Code	- 200
            Returnwert - Neuer User
        """
        user = {
            "id": "7",
            "name": "T7",
            "knowledge": ["Clustering", "Effector"]
        }
        erwartete = json.dumps({"head": {
            "vars": ["user", "id", "interesse", "knowledge"]
        },
            "results": {
                "bindings": [
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T7"},
                        "id": {"type": "literal", "value": "7"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T7"},
                        "id": {"type": "literal", "value": "7"},
                        "knowledge": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Clustering"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T7"},
                        "id": {"type": "literal", "value": "7"},
                        "knowledge": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Effector"}
                    }
                ]
            }
        })
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals(result, json.loads(erwartete))

    def test_newUser_POST_FalscheID(self):
        """Es probiert einen User mit einer für User bereits zugeteilte ID zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        INSERT DATA 
                        { kic:T8 rdf:type kic:User;
                                 kic:hasID "8"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        user = {
            "id": "8",
            "name": "T8",
            "knowledge": ["Clustering", "Effector"]
        }
        erwartete = b'Die ID 8 hat schon ein User.'
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newUser_POST_FalscheURIbyUser(self):
        """Es probiert einen User mit einer für User bereits zugeteilte URI zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        INSERT DATA 
                        { kic:T9 rdf:type kic:User;
                                 kic:hasID "9"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        user = {
            "id": "10",
            "name": "T9",
            "knowledge": ["Clustering", "Effector"]
        }
        erwartete = b'Das URI T9 existiert schon. Es muss ein unique sein.'
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newUser_POST_FalscheURIbyLearningItem(self):
        """Es probiert einen User mit einer für LearningItem bereits zugeteilte URI zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        INSERT DATA 
                        { kic:TLI12 rdf:type kic:LearningItem;
                                 kic:hasID "12"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        user = {
            "id": "11",
            "name": "TLI12",
            "knowledge": ["Clustering", "Effector"]
        }
        erwartete = b'Das URI TLI12 existiert schon. Es muss ein unique sein.'
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newUser_POST_FalscheInteresse(self):
        """Es probiert einen User mit einem nicht existierenden Interesse zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        user = {
            "id": "12",
            "name": "T12",
            "interesse": "falsche_daten"
        }
        erwartete = b'Das Gebiet falsche_daten bei Interesse existiert nicht.'
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newUser_POST_FalscheKnowledge(self):
        """Es probiert einen User mit einem nicht existierenden Knowledge zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        user = {
            "id": "13",
            "name": "T13",
            "knowledge": "falsche_daten"
        }
        erwartete = b'Das Gebiet falsche_daten bei Knowledge existiert nicht.'
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newUser_POST_FalscheInteresseInListe(self):
        """Es probiert einen User mit einen Liste Interesse zu erschaffen. Die Interessenliste hat ein Mitglied, das nicht existiert
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        user = {
            "id": "14",
            "name": "T14",
            "interesse": ["Robotics", "falsche_daten"]
        }
        erwartete = b'Das Gebiet falsche_daten bei Interesse existiert nicht.'
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newUser_POST_FalscheKnowledgeInListe(self):
        """Es probiert einen User mit einen Liste Knowledge zu erschaffen. Die Knowledgeliste hat ein Mitglied, das nicht existiert
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        user = {
            "id": "15",
            "name": "T15",
            "knowledge": ["Robotics", "falsche_daten"]
        }
        erwartete = b'Das Gebiet falsche_daten bei Knowledge existiert nicht.'
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newUser_POST_OhneID(self):
        """Es probiert einen User ohne ID zu erschaffen
            Status Code	- 200
            Returnwert	Fehlermeldung
        """

        user = {
            "name": "T16",
            "knowledge": "Robotics"
        }
        erwartete = b"ID fehlt!"
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newUser_POST_OhneURI(self):
        """Es probiert einen User ohne URI zu erschaffen
            Status Code	- 200
            Returnwert - Fehlermeldung
        """

        user = {
            "id": "17",
            "knowledge": ["Robotics", "Haptic"]
        }
        erwartete = b"URI fehlt!"
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newUser_POST_GuteDaten_IDbyLearningItem(self):
        """Es probiert einen User mit einer für LearningItem bereits zugeteilte ID zu erschaffen
            Status Code	- 200
            Returnwert	- Neuer User
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        INSERT DATA 
                        { kic:TLI21 rdf:type kic:LearningItem;
                                 kic:hasID "21"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        user = {
            "id": "21",
            "name": "T21",
            "knowledge": ["Clustering", "Effector"]
        }
        erwartete = json.dumps({"head": {
            "vars": ["user", "id", "interesse", "knowledge"]
        },
            "results": {
                "bindings": [
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T21"},
                        "id": {"type": "literal", "value": "21"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T21"},
                        "id": {"type": "literal", "value": "21"},
                        "knowledge": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Clustering"}
                    },
                    {
                        "user": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T21"},
                        "id": {"type": "literal", "value": "21"},
                        "knowledge": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Effector"}
                    }
                ]
            }
        })
        userJSON = json.dumps(user)
        response = self.client.post(self.newUser_url, userJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals(result, json.loads(erwartete))


    def test_newUser_POST_falscheAnfrage_Put(self):
        """Es probiert ein falsche Anfrage zu view ordnen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """
        erwartete=b"An diese URL darf nur POST-Anfrage gesendet werden"
        response = self.client.put(self.newUser_url, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

# --------------Tests zu newKurs-----------------

    def test_newKurs_POST_guteDaten_IdUriCt(self):
        """Es erschafft einen neuen Kurs mit bestimmten ID, URI und einen ContentTag
            Status Code	- 200
            Returnwert	- Neuer Kurs
        """
        kurs = {
            "id": "1",
            "name": "TK1",
            "contentTags": "Affect"
        }
        erwartete = json.dumps({"head": {
            "vars": ["learningOffer", "id", "contentTag", "prerequitsute"]
        },
            "results": {
                "bindings": [
                    {
                        "learningOffer": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TK1"},
                        "id": {"type": "literal", "value": "1"},
                        "contentTag": {"type": "uri",
                                       "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Affect"}
                    },
                    {
                    }
                ]
            }
        })
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals(result, json.loads(erwartete))

    def test_newKurs_POST_guteDaten_IdUriCtListe(self):
        """Es erschafft einen neuen Kurs mit bestimmten ID, URI und mehreren ContentTags
            Status Code	- 200
            Returnwert	- Neuer Kurs
        """
        kurs = {
            "id": "2",
            "name": "TK2",
            "contentTags": ["Affect", "Logic"]
        }
        erwartete = json.dumps({"head": {
            "vars": ["learningOffer", "id", "contentTag", "prerequitsute"]
        },
            "results": {
                "bindings": [
                    {
                        "learningOffer": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TK2"},
                        "id": {"type": "literal", "value": "2"},
                        "contentTag": {"type": "uri",
                                       "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Affect"}
                    },
                    {
                        "learningOffer": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TK2"},
                        "id": {"type": "literal", "value": "2"},
                        "contentTag": {"type": "uri",
                                       "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Logic"}
                    },
                    {
                    }
                ]
            }
        })
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals(result, json.loads(erwartete))

    def test_newKurs_POST_guteDaten_IdUriCtPrerequisites(self):
        """Es erschafft einen neuen Kurs mit bestimmten ID, URI, mehreren ContentTags, und einen Vorwissen
            Status Code	- 200
            Returnwert	- Neuer Kurs
        """
        kurs = {
            "id": "3",
            "name": "TK3",
            "contentTags": ["Affect", "Logic"],
            "prerequisites": "Haptic"
        }
        erwartete = json.dumps({"head": {
            "vars": ["learningOffer", "id", "contentTag", "prerequitsute"]
        },
            "results": {
                "bindings": [
                    {
                        "learningOffer": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TK3"},
                        "id": {"type": "literal", "value": "3"},
                        "contentTag": {"type": "uri",
                                       "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Affect"}
                    },
                    {
                        "learningOffer": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TK3"},
                        "id": {"type": "literal", "value": "3"},
                        "contentTag": {"type": "uri",
                                       "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Logic"}
                    },
                    {
                        "learningOffer": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TK3"},
                        "id": {"type": "literal", "value": "3"},
                        "prerequitsute": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Haptic"}
                    }
                ]
            }
        })
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals(result, json.loads(erwartete))

    def test_newKurs_POST_guteDaten_IdUriCtPrerequisitesListe(self):
        """Es erschafft einen neuen Kurs mit bestimmten ID, URI, mehreren ContentTags, und mehreren Vorwissen
            Status Code	- 200
            Returnwert	- Neuer Kurs
        """
        kurs = {
            "id": "4",
            "name": "TK4",
            "contentTags": ["Affect", "Logic"],
            "prerequisites": ["Haptic", "Clustering"]
        }
        erwartete = json.dumps({"head": {
            "vars": ["learningOffer", "id", "contentTag", "prerequitsute"]
        },
            "results": {
                "bindings": [
                    {
                        "learningOffer": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TK4"},
                        "id": {"type": "literal", "value": "4"},
                        "contentTag": {"type": "uri",
                                       "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Affect"}
                    },
                    {
                        "learningOffer": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TK4"},
                        "id": {"type": "literal", "value": "4"},
                        "contentTag": {"type": "uri",
                                       "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Logic"}
                    },
                    {
                        "learningOffer": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TK4"},
                        "id": {"type": "literal", "value": "4"},
                        "prerequitsute": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Clustering"}
                    },
                    {
                        "learningOffer": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TK4"},
                        "id": {"type": "literal", "value": "4"},
                        "prerequitsute": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Haptic"}
                    }
                ]
            }
        })
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals(result, json.loads(erwartete))

    def test_newKurs_POST_FalscheID(self):
        """Es probiert einen Kurs mit einer für Kurs bereits zugeteilte ID zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        INSERT DATA 
                        { kic:TK5 rdf:type kic:LearningOffer;
                                 kic:hasID "5"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        kurs = {
            "id": "5",
            "name": "TK6",
            "contentTags": ["Clustering", "Effector"]
        }
        erwartete = b'Die ID 5 hat schon ein Kurs.'
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newKurs_POST_FalscheURIbyKurs(self):
        """Es probiert einen Kurs mit einer für einen Kurs bereits zugeteilte URI zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        INSERT DATA 
                        { kic:TK7 rdf:type kic:Kurs;
                                 kic:hasID "8"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        kurs = {
            "id": "9",
            "name": "TK7",
            "knowledge": ["Clustering", "Effector"]
        }
        erwartete = b'Das URI TK7 existiert schon. Es muss ein unique sein.'
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newKurs_POST_FalscheURIbyUser(self):
        """Es probiert einen Kurs mit einer für einen User bereits zugeteilte ID zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        INSERT DATA 
                        { kic:TK8 rdf:type kic:User;
                                 kic:hasID "20"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        kurs = {
            "id": "10",
            "name": "TK8",
            "knowledge": ["Clustering", "Effector"]
        }
        erwartete = b'Das URI TK8 existiert schon. Es muss ein unique sein.'
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newKurs_POST_FalscheContentTags(self):
        """Es probiert einen Kurs mit einem nicht existierenden ContentTag zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        kurs = {
            "id": "12",
            "name": "TK12",
            "contentTags": "falsche_daten"
        }
        erwartete = b'Das Content Tag falsche_daten existiert nicht.'
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newKurs_POST_FalschePrereqisites(self):
        """Es probiert einen Kurs mit einem ContentTag und einem nicht existierenden Vorwissen zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        kurs = {
            "id": "13",
            "name": "TK13",
            "contentTags": "Haptic",
            "prerequisites": "falsche_daten"
        }
        erwartete = b"Das Gebiet falsche_daten bei Prereqisites existiert nicht."
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newKurs_POST_FalscheContentTagsInListe(self):
        """Es probiert einen Kurs mit einer Liste ContentTags zu erschaffen. Die ContentTagliste hat ein Mitglied, das nicht existiert
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        kurs = {
            "id": "14",
            "name": "TK14",
            "contentTags": ["Robotics", "falsche_daten"]
        }
        erwartete = b'Das Content Tag falsche_daten existiert nicht.'
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newKurs_POST_FalschePrerequisitesInListe(self):
        """Es probiert einen Kurs mit einem ContentTags und einer Liste von Vorwissen zu erschaffen. Die ContentTagliste hat ein Mitglied, das nicht existiert
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        kurs = {
            "id": "15",
            "name": "TK15",
            "contentTags": ["Affect", "Logic"],
            "prerequisites": ["Robotics", "falsche_daten"]
        }
        erwartete = b"Das Gebiet falsche_daten bei Prereqisites existiert nicht."
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newKurs_POST_OhneID(self):
        """Es probiert einen Kurs ohne ID zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        kurs = {
            "name": "TK16",
            "contentTags": "Robotics"
        }
        erwartete = b"ID fehlt!"
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newKurs_POST_OhneURI(self):
        """Es probiert einen Kurs ohne URI zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        kurs = {
            "id": "17",
            "contentTags": ["Robotics", "Haptic"]
        }
        erwartete = b"URI fehlt!"
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newKurs_POST_OhneContentTags(self):
        """Es probiert einen Kurs ohne ContentTag zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        kurs = {
            "id": "18",
            "name": "TK18"
        }
        erwartete = b"Geben Sie mindestens ein Content Tag ein!"
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newKurs_POST_GuteDaten_IDbyLecturer(self):
        """Es probiert einen Kurs mit einer für Dozent bereits zugeteilte ID zu erschaffen
            Status Code	- 200
            Returnwert	- Neuer Kurs
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        INSERT DATA 
                        { kic:TL24 rdf:type kic:Lecturer;
                                 kic:hasID "24"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        kurs = {
            "id": "24",
            "name": "TK24",
            "contentTags": ["Affect", "Logic"]
        }
        erwartete = json.dumps({"head": {
            "vars": ["learningOffer", "id", "contentTag", "prerequitsute"]
        },
            "results": {
                "bindings": [
                    {
                        "learningOffer": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TK24"},
                        "id": {"type": "literal", "value": "24"},
                        "contentTag": {"type": "uri",
                                       "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Affect"}
                    },
                    {
                        "learningOffer": {"type": "uri",
                                          "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TK24"},
                        "id": {"type": "literal", "value": "24"},
                        "contentTag": {"type": "uri",
                                       "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Logic"}
                    },
                    {
                    }
                ]
            }
        })
        kursJSON = json.dumps(kurs)
        response = self.client.post(self.newKurs_url, kursJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals(result, json.loads(erwartete))


    def test_newKurz_POST_falscheAnfrage_Put(self):
        """Es probiert ein falsche Anfrage zu view ordnen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """
        erwartete=b"An diese URL darf nur POST-Anfrage gesendet werden"
        response = self.client.put(self.newKurs_url, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    # --------------Tests zu newLecture-----------------

    def test_newLecturer_POST_guteDaten_IdName(self):
        """Es erschafft einen neuen Dozent mit bestimmten ID und URI
            Status Code	- 200
            Returnwert	- Neuer Dozent
        """
        lecturer = {
            "id": "1",
            "name": "TL1"
        }
        erwartete = json.dumps({"head": {
            "vars": ["lecturer", "id", "expertise"]
        },
            "results": {
                "bindings": [
                    {
                        "lecturer": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL1"},
                        "id": {"type": "literal", "value": "1"}
                    }
                ]
            }
        })
        lecturerJSON = json.dumps(lecturer)
        response = self.client.post(self.newLecturer_url, lecturerJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals((result), json.loads(erwartete))

    def test_newLecturer_POST_guteDaten_IdNameExpertise(self):
        """Es erschafft einen neuen Dozent mit bestimmten ID, URI und einen Expertise
            Status Code	 - 200
            Returnwert	- Neuer Dozent
        """
        lecturer = {
            "id": "2",
            "name": "TL2",
            "expertise": "Clustering"
        }
        erwartete = json.dumps({"head": {
            "vars": ["lecturer", "id", "expertise"]
        },
            "results": {
                "bindings": [
                    {
                        "lecturer": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL2"},
                        "id": {"type": "literal", "value": "2"},
                        "expertise": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Clustering"}
                    }
                ]
            }
        })
        lecturerJSON = json.dumps(lecturer)
        response = self.client.post(self.newLecturer_url, lecturerJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals((result), json.loads(erwartete))

    def test_newLecturer_POST_guteDaten_IdNameExpertiseListe(self):
        """Es erschafft einen neuen Dozent mit bestimmten ID, URI und mehreren Expertise
            Status Code	- 200
            Returnwert	- Neuer Dozent
        """
        lecturer = {
            "id": "3",
            "name": "TL3",
            "expertise": ["Clustering", "Actor"]
        }
        erwartete = json.dumps({"head": {
            "vars": ["lecturer", "id", "expertise"]
        },
            "results": {
                "bindings": [
                    {
                        "lecturer": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL3"},
                        "id": {"type": "literal", "value": "3"},
                        "expertise": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Actor"}
                    },
                    {
                        "lecturer": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL3"},
                        "id": {"type": "literal", "value": "3"},
                        "expertise": {"type": "uri",
                                      "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Clustering"}
                    }
                ]
            }
        })
        lecturerJSON = json.dumps(lecturer)
        response = self.client.post(self.newLecturer_url, lecturerJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals((result), json.loads(erwartete))

    def test_newLecturer_POST_FalscheID(self):
        """Es probiert einen Dozent mit einer für einen Dozent bereits zugeteilte ID zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                         PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                         PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                         PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                         PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                         INSERT DATA 
                         { kic:TL5 rdf:type kic:Lecturer;
                                  kic:hasID "4"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        lecturer = {
            "id": "4",
            "name": "TL4",
            "expertise": ["Clustering", "Effector"]
        }
        erwartete = b'Die ID 4 hat schon ein Dozent.'
        lecturerJSON = json.dumps(lecturer)
        response = self.client.post(self.newLecturer_url, lecturerJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLecturer_POST_FalscheURIbyLecturer(self):
        """Es probiert einen Dozent mit einer für einen Dozent bereits zugeteilte URI zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                         PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                         PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                         PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                         PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                         INSERT DATA 
                         { kic:TL6 rdf:type kic:Lecturer;
                                  kic:hasID "7"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        lecturer = {
            "id": "6",
            "name": "TL6",
            "expertise": ["Clustering", "Effector"]
        }
        erwartete = b'Das URI TL6 existiert schon. Es muss ein unique sein.'
        lecturerJSON = json.dumps(lecturer)
        response = self.client.post(self.newLecturer_url, lecturerJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLecturer_POST_FalscheURIbyKurs(self):
        """Es probiert einen Dozent mit einer für einen Kurs bereits zugeteilte URI zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                         PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                         PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                         PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                         PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                         INSERT DATA 
                         { kic:TL8 rdf:type kic:LearningOffer;
                                  kic:hasID "19"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        lecturer = {
            "id": "8",
            "name": "TL8",
            "expertise": ["Clustering", "Effector"]
        }
        erwartete = b'Das URI TL8 existiert schon. Es muss ein unique sein.'
        lecturerJSON = json.dumps(lecturer)
        response = self.client.post(self.newLecturer_url, lecturerJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLecturer_POST_FalscheExpertise(self):
        """Es probiert einen Dozent mit einem nicht existierenden Expertise zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        lecturer = {
            "id": "9",
            "name": "TL9",
            "expertise": "falsche_daten"
        }
        erwartete = b'Das Expertise falsche_daten existiert nicht.'
        lecturerJSON = json.dumps(lecturer)
        response = self.client.post(self.newLecturer_url, lecturerJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLecturer_POST_FalscheExpertiseInListe(self):
        """Es probiert einen Dozent mit einer Liste Expertise zu erschaffen. Die Expertiseliste hat ein Mitglied, das nicht existiert
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        lecturer = {
            "id": "10",
            "name": "TL10",
            "expertise": ["Robotics", "falsche_daten"]
        }
        erwartete = b'Das Expertise falsche_daten existiert nicht.'
        lecturerJSON = json.dumps(lecturer)
        response = self.client.post(self.newLecturer_url, lecturerJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLecturerPOST_OhneID(self):
        """Es probiert einen Dozent ohne ID zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        lecturer = {
            "name": "TL11",
            "expertise": "Robotics"
        }
        erwartete = b"ID fehlt!"
        lecturerJSON = json.dumps(lecturer)
        response = self.client.post(self.newLecturer_url, lecturerJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLecturer_POST_OhneURI(self):
        """Es probiert einen Dozent ohne URI zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        lecturer = {
            "id": "12",
            "expertise": ["Robotics", "Haptic"]
        }
        erwartete = b"URI fehlt!"
        lecturerJSON = json.dumps(lecturer)
        response = self.client.post(self.newLecturer_url, lecturerJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLecturer_POST_GuteDaten_IDbyKurs(self):
        """Es probiert einen Dozent mit einer für einen Kurs bereits zugeteilte ID zu erschaffen
            Status Code	- 200
            Returnwert	- Neuer Dozent
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                         PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                         PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                         PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                         PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                         INSERT DATA 
                         { kic:TK22 rdf:type kic:LearningOffer;
                                  kic:hasID "22"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        lecturer = {
            "id": "22",
            "name": "TL22"
        }
        erwartete = json.dumps({"head": {
            "vars": ["lecturer", "id", "expertise"]
        },
            "results": {
                "bindings": [
                    {
                        "lecturer": {"type": "uri", "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL22"},
                        "id": {"type": "literal", "value": "22"}
                    }
                ]
            }
        })
        lecturerJSON = json.dumps(lecturer)
        response = self.client.post(self.newLecturer_url, lecturerJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals(result, json.loads(erwartete))


    def test_newLecturer_POST_falscheAnfrage_Put(self):
        """Es probiert ein falsche Anfrage zu view ordnen
            Status Code -	200
            Returnwert	- Fehlermeldung
        """
        erwartete=b"An diese URL darf nur POST-Anfrage gesendet werden"
        response = self.client.put(self.newLecturer_url, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    # --------------Tests zu newLearningItem-----------------

    def test_newLearningItem_POST_guteDaten_IdUriCt(self):
        """Es erschafft einen neuen LearningItem mit bestimmten ID, URI und einen ContentTag
            Status Code	- 200
            Returnwert	- Neuer Learning Item
        """
        learningItem = {
            "id": "1",
            "name": "TLI1",
            "contentTags": "Affect"
        }
        erwartete = json.dumps({"head": {
            "vars": ["learningItem", "id", "contentTags"]
        },
            "results": {
                "bindings": [
                    {
                        "learningItem": {"type": "uri",
                                         "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TLI1"},
                        "id": {"type": "literal", "value": "1"},
                        "contentTags": {"type": "uri",
                                        "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Affect"}
                    }
                ]
            }
        })
        learningItemJSON = json.dumps(learningItem)
        response = self.client.post(self.newLearningItem_url, learningItemJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals(result, json.loads(erwartete))

    def test_newLearningItem_POST_guteDaten_IdUriCtListe(self):
        """Es erschafft einen neuen LearningItem mit bestimmten ID, URI und mehreren ContentTags
            Status Code	- 200
            Returnwert	- Neuer Learning Item
        """
        learningItem = {
            "id": "2",
            "name": "TLI2",
            "contentTags": ["Affect", "Logic"]
        }
        erwartete = json.dumps({"head": {
            "vars": ["learningItem", "id", "contentTags"]
        },
            "results": {
                "bindings": [
                    {
                        "learningItem": {"type": "uri",
                                         "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TLI2"},
                        "id": {"type": "literal", "value": "2"},
                        "contentTags": {"type": "uri",
                                        "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Affect"}
                    },
                    {
                        "learningItem": {"type": "uri",
                                         "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TLI2"},
                        "id": {"type": "literal", "value": "2"},
                        "contentTags": {"type": "uri",
                                        "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Logic"}
                    }
                ]
            }
        })
        learningItemJSON = json.dumps(learningItem)
        response = self.client.post(self.newLearningItem_url, learningItemJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals(result, json.loads(erwartete))

    def test_newLearningItem_POST_FalscheID(self):
        """Es probiert einen LearningItem mit einer für einen LearningItem bereits zugeteilte ID zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        INSERT DATA 
                        { kic:TLI3 rdf:type kic:LearningItem;
                                 kic:hasID "3"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        learningItem = {
            "id": "3",
            "name": "TLI4",
            "contentTags": ["Clustering", "Effector"]
        }
        erwartete = b'Die ID 3 hat schon ein Learning Item.'
        learningItemJSON = json.dumps(learningItem)
        response = self.client.post(self.newLearningItem_url, learningItemJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLearningItem_POST_FalscheURIbyLearningItem(self):
        """Es probiert einenLearningItem mit einer für einen LearningItem bereits zugeteilte URI zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        INSERT DATA 
                        { kic:TLI5 rdf:type kic:LearningItem;
                                 kic:hasID "6"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        learningItem = {
            "id": "5",
            "name": "TLI5",
            "contentTags": ["Clustering", "Effector"]
        }
        erwartete = b'Das URI TLI5 existiert schon. Es muss ein unique sein.'
        learningItemJSON = json.dumps(learningItem)
        response = self.client.post(self.newLearningItem_url, learningItemJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLearningItem_POST_FalscheURIbyKurs(self):
        """Es probiert einen LearningItem mit einer für einen Kurs bereits zugeteilte URI zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                        PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        INSERT DATA 
                        { kic:TLI6 rdf:type kic:Kurs;
                                 kic:hasID "14"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        learningItem = {
            "id": "6",
            "name": "TLI6",
            "contentTags": ["Clustering", "Effector"]
        }
        erwartete = b'Das URI TLI6 existiert schon. Es muss ein unique sein.'
        learningItemJSON = json.dumps(learningItem)
        response = self.client.post(self.newLearningItem_url, learningItemJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLearningItem_POST_FalscheContentTags(self):
        """Es probiert einen LearningItem mit einem nicht existierenden ContentTag zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        learningItem = {
            "id": "7",
            "name": "TLI7",
            "contentTags": "falsche_daten"
        }
        erwartete = b'Das Content Tag falsche_daten existiert nicht.'
        learningItemJSON = json.dumps(learningItem)
        response = self.client.post(self.newLearningItem_url, learningItemJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLearningItem_POST_FalscheContentTagsInListe(self):
        """Es probiert einen LearningItem mit einer Liste ContentTags zu erschaffen. Die ContentTagliste hat ein Mitglied, das nicht existiert
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        learningItem = {
            "id": "8",
            "name": "TLI8",
            "contentTags": ["Robotics", "falsche_daten"]
        }
        erwartete = b'Das Content Tag falsche_daten existiert nicht.'
        learningItemJSON = json.dumps(learningItem)
        response = self.client.post(self.newLearningItem_url, learningItemJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLearningItem_POST_OhneID(self):
        """Es probiert einen LearningItem ohne ID zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        learningItem = {
            "name": "TLI9",
            "contentTags": "Robotics"
        }
        erwartete = b"ID fehlt!"
        learningItemJSON = json.dumps(learningItem)
        response = self.client.post(self.newLearningItem_url, learningItemJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLearningItem_POST_OhneURI(self):
        """Es probiert einen LearningItem ohne URI zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        learningItem = {
            "id": "10",
            "contentTags": ["Robotics", "Haptic"]
        }
        erwartete = b"URI fehlt!"
        learningItemJSON = json.dumps(learningItem)
        response = self.client.post(self.newLearningItem_url, learningItemJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLearningItem_POST_OhneContentTags(self):
        """Es probiert einen LearningItem ohne ContentTags zu erschaffen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """

        learningItem = {
            "id": "11",
            "name": "TLI11"
        }
        erwartete = b"Geben Sie mindestens ein Content Tag ein!"
        learningItemJSON = json.dumps(learningItem)
        response = self.client.post(self.newLearningItem_url, learningItemJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_newLearningItem_POST_GuteDaten_IDbyUser(self):
        """Es probiert einen LearningItem mit einer für einen User bereits zugeteilte ID zu erschaffen
            Status Code	- 200
            Returnwert	- Neuer Learning Item
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                         PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                         PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                         PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                         PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                         INSERT DATA 
                         { kic:T23 rdf:type kic:User;
                                  kic:hasID "23"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        learningItem = {
            "id": "23",
            "name": "TLI23",
            "contentTags": ["Affect", "Logic"]
        }
        erwartete = json.dumps({"head": {
            "vars": ["learningItem", "id", "contentTags"]
        },
            "results": {
                "bindings": [
                    {
                        "learningItem": {"type": "uri",
                                         "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TLI23"},
                        "id": {"type": "literal", "value": "23"},
                        "contentTags": {"type": "uri",
                                        "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Affect"}
                    },
                    {
                        "learningItem": {"type": "uri",
                                         "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TLI23"},
                        "id": {"type": "literal", "value": "23"},
                        "contentTags": {"type": "uri",
                                        "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Logic"}
                    }
                ]
            }
        })
        learningItemJSON = json.dumps(learningItem)
        response = self.client.post(self.newLearningItem_url, learningItemJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        try:
            self.assertEquals(json.loads(result), json.loads(erwartete))
        except json.decoder.JSONDecodeError:
            self.assertEquals(result, json.loads(erwartete))


    def test_newLearningItem_POST_falscheAnfrage_Put(self):
        """Es probiert ein falsche Anfrage zu view ordnen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """
        erwartete=b"An diese URL darf nur POST-Anfrage gesendet werden"
        response = self.client.put(self.newLearningItem_url, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

#---------------Tests zu learningItemDelete-----------------------

    def test_learningItemDelete_DELETE_guteDaten(self):
        """Es löscht ein LearningItem mit dem eingegebenden ID
            Status Code	- 200
            Returnwert	- Erfolgmeldung
            Existenz von gelöschte Instenz	- False
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                                 PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                                 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                 PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                                 PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                                 PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                                 PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                                 INSERT DATA 
                                 { kic:TLI24 rdf:type kic:LearningItem;
                                          kic:hasID "24"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        learningItemDelete_url = reverse('kb_service:learningItemDelete', args=['24'])
        erwartete=b"Das Learning Item mit ID 24 erfolgreich entfernt worden."
        response = self.client.delete(learningItemDelete_url)
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)
        sparql = SPARQLWrapper(fuseki, returnFormat="json")
        query = """
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    ASK
                    WHERE {
  						?x rdf:type kic:LearningItem .
                  		?x kic:hasID "24"^^xsd:string 
					}"""
        sparql.setQuery(query)
        existiert = sparql.query().convert()
        erwateteExistenz = json.dumps({'head': {}, 'boolean': False})
        self.assertEquals(existiert, json.loads(erwateteExistenz))

    def test_learningItemDelete_DELETE_falscheID(self):
        """Es probiert ein LearningItem mit dem eingegebenden ID löschen, dessen nicht existiert
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """
        learningItemDelete_url = reverse('kb_service:learningItemDelete', args=['25'])
        erwartete=b"Es gibt keinen Learning Item mit dem ID 25"
        response = self.client.delete(learningItemDelete_url)
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_learningItemDelete_DELETE_falscheAnfrage_Post(self):
        """Es probiert ein falsche Anfrage zu view ordnen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """
        learningItemDelete_url = reverse('kb_service:learningItemDelete', args=['25'])
        erwartete=b"An diese URL darf nur DELETE-Anfrage gesendet werden"
        response = self.client.post(learningItemDelete_url, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)



# --------------Tests zu userUpdateDelete - DELETE-----------------

    def test_userUpdateDelete_DELETE_guteDaten(self):
        """Es löscht ein User mit dem eingegebenden ID
            Status Code	- 200
            Returnwert	- Erfolgmeldung
            Existenz von gelöschte Instenz	- False
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                     PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                     PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                     INSERT DATA 
                     { kic:T24 rdf:type kic:User;
                              kic:hasID "24"^^xsd:string }"""
        sparql.setQuery(query)
        sparql.query()
        erwartete=b"Der User mit ID 24 erfolgreich entfernt worden."
        self.userUpdateDelete_url = reverse('kb_service:userUpdateDelete', args=['24'])
        response=self.client.delete(self.userUpdateDelete_url)
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)
        sparql = SPARQLWrapper(fuseki, returnFormat="json")
        query = """
                            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                            ASK
                            WHERE {
          						?x rdf:type kic:User .
                          		?x kic:hasID "24"^^xsd:string 
        					}"""
        sparql.setQuery(query)
        existiert = sparql.query().convert()
        erwateteExistenz = json.dumps({'head': {}, 'boolean': False})
        self.assertEquals(existiert, json.loads(erwateteExistenz))


    def test_userUpdateDelete_DELETE_falscheID(self):
        """Es probiert ein User mit dem eingegebenden ID löschen, dessen nicht existiert
            Status Code -	200
            Returnwert	- Fehlermeldung
        """
        userUpdateDelete_url = reverse('kb_service:userUpdateDelete', args=['25'])
        erwartete=b"Es gibt keinen User mit dem ID 25"
        response = self.client.delete(userUpdateDelete_url)
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_userUpdateDelete_falscheAnfrage_Post(self):
        """Es probiert ein falsche Anfrage zu view ordnen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """
        userUpdateDelete_url = reverse('kb_service:userUpdateDelete', args=['26'])
        erwartete=b"An diese URL darf nur PUT- und DELETE-Anfrage gesendet werden"
        response = self.client.post(userUpdateDelete_url, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

#----------------Tests zu userUpdateDelete - PUT-----------------

    def test_userUpdateDelete_PUT_guteDaten_InteresseKnowledgeLoeschen(self):
        """Es löscht die Interessen und Knowledges von einem User mit eingegebener ID
            Status Code	- 200
            Returnwert	- Erfolgmeldung
            Veränderte Instanz	- Veränderte Instanz
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                     PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                     PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                     INSERT DATA 
                     { kic:T27 rdf:type kic:User;
                              kic:hasID "27"^^xsd:string ;
                              kic:hasKnowledge dom:Robotics ; 
                              kic:hasInterests dom:Haptic . }"""
        sparql.setQuery(query)
        sparql.query()
        userdaten={

        }
        userdatenJSON=json.dumps(userdaten)
        erwartete=b"Update des Users mit ID 27 ist erfolgreich."
        self.userUpdateDelete_url = reverse('kb_service:userUpdateDelete', args=['27'])
        response=self.client.put(self.userUpdateDelete_url, userdatenJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)
        sparql = SPARQLWrapper(fuseki, returnFormat="json")
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
                      ?user kic:hasID  "27"^^xsd:string .  
                      ?user kic:hasID ?id .
                        OPTIONAL {
                            ?user kic:hasInterests ?interesse .
                            }
                      }
                    UNION
                      {
                        OPTIONAL{
                            ?user rdf:type kic:User .
                            ?user kic:hasID  "27"^^xsd:string .  
                            ?user kic:hasID ?id .
                            ?user kic:hasKnowledge ?knowledge
                      }    
                    }
                    }"""
        sparql.setQuery(query)
        newUser = sparql.query().convert()
        erwateteUser = json.dumps({ "head": {
            "vars": [ "user" , "id" , "interesse" , "knowledge" ]
            } ,
            "results": {
            "bindings": [
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T27" } ,
            "id": { "type": "literal" , "value": "27" }
            } ,
            {
            }
            ]
            }
            })
        self.assertEquals(newUser, json.loads(erwateteUser))


    def test_userUpdateDelete_PUT_guteDaten_InteresseKnowledgeListe(self):
        """Es löscht  die alte Interessen und Knowledges von einem User mit eingegebener ID, und fügt neuen hinzu
            Status Code	- 200
            Returnwert	- Erfolgmeldung
            Veränderte Instanz	- Veränderte Instanz
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                     PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                     PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                     INSERT DATA 
                     { kic:T28 rdf:type kic:User;
                              kic:hasID "28"^^xsd:string ;
                              kic:hasKnowledge dom:Robotics ; 
                              kic:hasInterests dom:Haptic . }"""
        sparql.setQuery(query)
        sparql.query()
        userdaten={
            "interesse":["Act","Robotics"] ,
            "knowledge":["Haptic", "Affect", "Emotion"]
        }
        userdatenJSON=json.dumps(userdaten)
        erwartete=b"Update des Users mit ID 28 ist erfolgreich."
        self.userUpdateDelete_url = reverse('kb_service:userUpdateDelete', args=['28'])
        response=self.client.put(self.userUpdateDelete_url, userdatenJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)
        sparql = SPARQLWrapper(fuseki, returnFormat="json")
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
                      ?user kic:hasID  "28"^^xsd:string .  
                      ?user kic:hasID ?id .
                        OPTIONAL {
                            ?user kic:hasInterests ?interesse .
                            }
                      }
                    UNION
                      {
                        OPTIONAL{
                            ?user rdf:type kic:User .
                            ?user kic:hasID  "28"^^xsd:string .  
                            ?user kic:hasID ?id .
                            ?user kic:hasKnowledge ?knowledge
                      }    
                    }
                    }"""
        sparql.setQuery(query)
        newUser = sparql.query().convert()
        erwateteUser = json.dumps( { "head": {
            "vars": [ "user" , "id" , "interesse" , "knowledge" ]
            } ,
            "results": {
            "bindings": [
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T28" } ,
            "id": { "type": "literal" , "value": "28" } ,
            "interesse": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Act" }
            } ,
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T28" } ,
            "id": { "type": "literal" , "value": "28" } ,
            "interesse": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Robotics" }
            } ,
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T28" } ,
            "id": { "type": "literal" , "value": "28" } ,
            "knowledge": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Affect" }
            } ,
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T28" } ,
            "id": { "type": "literal" , "value": "28" } ,
            "knowledge": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Emotion" }
            } ,
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T28" } ,
            "id": { "type": "literal" , "value": "28" } ,
            "knowledge": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Haptic" }
            }
            ]
            }
            })
        self.assertEquals(newUser, json.loads(erwateteUser))

    def test_userUpdateDelete_PUT_guteDaten_InteresseUmschreiben(self):
        """Es löscht  die alte Interessen von einem User mit eingegebener ID, und fügt neuen hinzu
            Status Code -	200
            Returnwert	- Erfolgmeldung
            Veränderte Instanz	- Veränderte Instanz
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                     PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                     PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                     INSERT DATA 
                     { kic:T29 rdf:type kic:User;
                              kic:hasID "29"^^xsd:string ;
                              kic:hasKnowledge dom:Robotics ; 
                              kic:hasInterests dom:Haptic . }"""
        sparql.setQuery(query)
        sparql.query()
        userdaten={
            "interesse":"Act",
            "knowledge":"Haptic"
        }
        userdatenJSON=json.dumps(userdaten)
        erwartete=b"Update des Users mit ID 29 ist erfolgreich."
        self.userUpdateDelete_url = reverse('kb_service:userUpdateDelete', args=['29'])
        response=self.client.put(self.userUpdateDelete_url, userdatenJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)
        sparql = SPARQLWrapper(fuseki, returnFormat="json")
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
                      ?user kic:hasID  "29"^^xsd:string .  
                      ?user kic:hasID ?id .
                        OPTIONAL {
                            ?user kic:hasInterests ?interesse .
                            }
                      }
                    UNION
                      {
                        OPTIONAL{
                            ?user rdf:type kic:User .
                            ?user kic:hasID  "29"^^xsd:string .  
                            ?user kic:hasID ?id .
                            ?user kic:hasKnowledge ?knowledge
                      }    
                    }
                    }"""
        sparql.setQuery(query)
        newUser = sparql.query().convert()
        erwateteUser = json.dumps( { "head": {
            "vars": [ "user" , "id" , "interesse" , "knowledge" ]
            } ,
            "results": {
            "bindings": [
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T29" } ,
            "id": { "type": "literal" , "value": "29" } ,
            "interesse": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Act" }
            } ,
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T29" } ,
            "id": { "type": "literal" , "value": "29" } ,
            "knowledge": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Haptic" }
            }
            ]
            }
            })
        self.assertEquals(newUser, json.loads(erwateteUser))

    def test_userUpdateDelete_PUT_guteDaten_InteresseUmschreibenKnowledgeLoeschen(self):
        """Es löscht  die alte Interessen und Knowledges von einem User mit eingegebener ID, und fügt neuen Interessen hinzu
            Status Code	- 200
            Returnwert	- Erfolgmeldung
            Veränderte Instanz	- Veränderte Instanz
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                     PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                     PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                     INSERT DATA 
                     { kic:T30 rdf:type kic:User;
                              kic:hasID "30"^^xsd:string ;
                              kic:hasKnowledge dom:Robotics ; 
                              kic:hasInterests dom:Haptic . }"""
        sparql.setQuery(query)
        sparql.query()
        userdaten={
            "interesse":["Haptic", "Act"]
        }
        userdatenJSON=json.dumps(userdaten)
        erwartete=b"Update des Users mit ID 30 ist erfolgreich."
        self.userUpdateDelete_url = reverse('kb_service:userUpdateDelete', args=['30'])
        response=self.client.put(self.userUpdateDelete_url, userdatenJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)
        sparql = SPARQLWrapper(fuseki, returnFormat="json")
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
                      ?user kic:hasID  "30"^^xsd:string .  
                      ?user kic:hasID ?id .
                        OPTIONAL {
                            ?user kic:hasInterests ?interesse .
                            }
                      }
                    UNION
                      {
                        OPTIONAL{
                            ?user rdf:type kic:User .
                            ?user kic:hasID  "30"^^xsd:string .  
                            ?user kic:hasID ?id .
                            ?user kic:hasKnowledge ?knowledge
                      }    
                    }
                    }"""
        sparql.setQuery(query)
        newUser = sparql.query().convert()
        erwarteteUser = json.dumps( { "head": {
            "vars": [ "user" , "id" , "interesse" , "knowledge" ]
            } ,
            "results": {
            "bindings": [
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T30" } ,
            "id": { "type": "literal" , "value": "30" } ,
            "interesse": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Act" }
            } ,
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T30" } ,
            "id": { "type": "literal" , "value": "30" } ,
            "interesse": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Haptic" }
            } ,
            {
            }
            ]
            }
            })
        self.assertEquals(newUser, json.loads(erwarteteUser))




    def test_userUpdateDelete_PUT_guteDaten_InteresseLoeschenKnowledgeUmschreiben(self):
        """Es löscht  die alte Interessen und Knowledges von einem User mit eingegebener ID, und fügt neuen Knowledges hinzu
            Status Code	- 200
            Returnwert	- Erfolgmeldung
            Veränderte Instanz	- Veränderte Instanz
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                     PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                     PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                     INSERT DATA 
                     { kic:T31 rdf:type kic:User;
                              kic:hasID "31"^^xsd:string ;
                              kic:hasKnowledge dom:Robotics ; 
                              kic:hasInterests dom:Haptic . }"""
        sparql.setQuery(query)
        sparql.query()
        userdaten={
            "knowledge":["Affect", "Act", "Emotion"]
        }
        userdatenJSON=json.dumps(userdaten)
        erwartete=b"Update des Users mit ID 31 ist erfolgreich."
        self.userUpdateDelete_url = reverse('kb_service:userUpdateDelete', args=['31'])
        response=self.client.put(self.userUpdateDelete_url, userdatenJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)
        sparql = SPARQLWrapper(fuseki, returnFormat="json")
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
                      ?user kic:hasID  "31"^^xsd:string .  
                      ?user kic:hasID ?id .
                        OPTIONAL {
                            ?user kic:hasInterests ?interesse .
                            }
                      }
                    UNION
                      {
                        OPTIONAL{
                            ?user rdf:type kic:User .
                            ?user kic:hasID  "31"^^xsd:string .  
                            ?user kic:hasID ?id .
                            ?user kic:hasKnowledge ?knowledge
                      }    
                    }
                    }"""
        sparql.setQuery(query)
        newUser = sparql.query().convert()
        erwarteteUser = json.dumps( { "head": {
            "vars": [ "user" , "id" , "interesse" , "knowledge" ]
            } ,
            "results": {
            "bindings": [
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T31" } ,
            "id": { "type": "literal" , "value": "31" }
            } ,
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T31" } ,
            "id": { "type": "literal" , "value": "31" } ,
            "knowledge": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Act" }
            } ,
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T31" } ,
            "id": { "type": "literal" , "value": "31" } ,
            "knowledge": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Affect" }
            } ,
            {
            "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T31" } ,
            "id": { "type": "literal" , "value": "31" } ,
            "knowledge": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Emotion" }
            }
            ]
            }
            })
        self.assertEquals(newUser, json.loads(erwarteteUser))


    def test_userUpdateDelete_PUT_guteDaten_InteresseKnowledgeHinzufuegen(self):
        """Es fügt zu einem User mehrere Interessen und knowledges hinzu, dem noch keine hat
            Status Code	- 200
            Returnwert	- Erfolgmeldung
            Veränderte Instanz -	Veränderte Instanz
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                     PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                     PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                     INSERT DATA 
                     { kic:T32 rdf:type kic:User;
                              kic:hasID "32"^^xsd:string . }"""
        sparql.setQuery(query)
        sparql.query()
        userdaten={
            "interesse": ["Haptic", "Effector"],
            "knowledge":["Affect", "Act", "Emotion"]
        }
        userdatenJSON=json.dumps(userdaten)
        erwartete=b"Update des Users mit ID 32 ist erfolgreich."
        self.userUpdateDelete_url = reverse('kb_service:userUpdateDelete', args=['32'])
        response=self.client.put(self.userUpdateDelete_url, userdatenJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)
        sparql = SPARQLWrapper(fuseki, returnFormat="json")
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
                      ?user kic:hasID  "32"^^xsd:string .  
                      ?user kic:hasID ?id .
                        OPTIONAL {
                            ?user kic:hasInterests ?interesse .
                            }
                      }
                    UNION
                      {
                        OPTIONAL{
                            ?user rdf:type kic:User .
                            ?user kic:hasID  "32"^^xsd:string .  
                            ?user kic:hasID ?id .
                            ?user kic:hasKnowledge ?knowledge
                      }    
                    }
                    }"""
        sparql.setQuery(query)
        newUser = sparql.query().convert()
        erwarteteUser = json.dumps( { "head": {
                "vars": [ "user" , "id" , "interesse" , "knowledge" ]
                } ,
                "results": {
                "bindings": [
                {
                "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T32" } ,
                "id": { "type": "literal" , "value": "32" } ,
                "interesse": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Effector" }
                } ,
                {
                "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T32" } ,
                "id": { "type": "literal" , "value": "32" } ,
                "interesse": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Haptic" }
                } ,
                {
                "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T32" } ,
                "id": { "type": "literal" , "value": "32" } ,
                "knowledge": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Act" }
                } ,
                {
                "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T32" } ,
                "id": { "type": "literal" , "value": "32" } ,
                "knowledge": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Affect" }
                } ,
                {
                "user": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#T32" } ,
                "id": { "type": "literal" , "value": "32" } ,
                "knowledge": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Emotion" }
                }
                ]
                }
                })
        self.assertEquals(newUser, json.loads(erwarteteUser))

    def test_userUpdateDelete_PUT_falscheID(self):
        """Es probiert die Daten von einem nicht existierenden User verändern
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """
        userUpdateDelete_url = reverse('kb_service:userUpdateDelete', args=['33'])
        erwartete=b"Es gibt keinen User mit dem ID 33"
        response = self.client.delete(userUpdateDelete_url)
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)




# --------------Tests zu lectureUpdate-----------------


    def test_lecturerUpdate_PUT_guteDaten_ExpertiseLoeschen(self):
        """Es löscht die Expertise von einem Dozent mit eingegebener ID
            Status Code -	200
            Returnwert	- Erfolgmeldung
            Veränderte Instanz	- Veränderte Instanz
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                     PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                     PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                     INSERT DATA 
                     { kic:TL25 rdf:type kic:Lecturer;
                              kic:hasID "25"^^xsd:string ;
                              kic:hasExpertise dom:Robotics ; 
                              kic:hasExpertise dom:Haptic . }"""
        sparql.setQuery(query)
        sparql.query()
        lecturerdaten={

        }
        lecturerdatenJSON=json.dumps(lecturerdaten)
        erwartete=b"Update des Lecturers mit ID 25 ist erfolgreich."
        self.lecturerUpdate_url = reverse('kb_service:lecturerUpdate', args=['25'])
        response=self.client.put(self.lecturerUpdate_url, lecturerdatenJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)
        sparql = SPARQLWrapper(fuseki, returnFormat="json")
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
                      ?lecturer kic:hasID  "25"^^xsd:string .  
                      ?lecturer kic:hasID ?id .
                        OPTIONAL {
                            ?lecturer kic:haExpertise ?expertise .
                            }
                    }"""
        sparql.setQuery(query)
        newLecturer = sparql.query().convert()
        erwateteLecturer = json.dumps({ "head": {
                "vars": [ "lecturer" , "id" , "expertise" ]
                } ,
                "results": {
                "bindings": [
                {
                "lecturer": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL25" } ,
                "id": { "type": "literal" , "value": "25" }
                }
                ]
                }
                })
        self.assertEquals(newLecturer, json.loads(erwateteLecturer))

    def test_lecturerUpdate_PUT_falscheAnfrage_Post(self):
        """Es probiert ein falsche Anfrage zu view ordnen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """
        lecturerUpdate_url = reverse('kb_service:lecturerUpdate', args=['26'])
        erwartete=b"An diese URL darf nur PUT-Anfrage gesendet werden"
        response = self.client.post(lecturerUpdate_url, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_lecturerUpdate_PUT_guteDaten_ExpertiseHinzufuegen(self):
        """Es fügt einen Expertise zu einem Dozent mit eingegebener ID hin, der  früher keine hatte
            Status Code -	200
            Returnwert	- Erfolgmeldung
            Veränderte Instanz	- Veränderte Instanz
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                     PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                     PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                     INSERT DATA 
                     { kic:TL26 rdf:type kic:Lecturer;
                              kic:hasID "26"^^xsd:string .}"""
        sparql.setQuery(query)
        sparql.query()
        lecturerdaten={
            "expertise":"Haptic"
        }
        lecturerdatenJSON=json.dumps(lecturerdaten)
        erwartete=b"Update des Lecturers mit ID 26 ist erfolgreich."
        self.lecturerUpdate_url = reverse('kb_service:lecturerUpdate', args=['26'])
        response=self.client.put(self.lecturerUpdate_url, lecturerdatenJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)
        sparql = SPARQLWrapper(fuseki, returnFormat="json")
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
                      ?lecturer kic:hasID  "26"^^xsd:string .  
                      ?lecturer kic:hasID ?id .
                        OPTIONAL {
                            ?lecturer kic:hasExpertise ?expertise .
                            }
                    }"""
        sparql.setQuery(query)
        newLecturer = sparql.query().convert()
        erwateteLecturer = json.dumps({ "head": {
            "vars": [ "lecturer" , "id" , "expertise" ]
            } ,
            "results": {
            "bindings": [
            {
            "lecturer": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL26" } ,
            "id": { "type": "literal" , "value": "26" } ,
            "expertise": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Haptic" }
            }
            ]
            }
            })
        self.assertEquals(newLecturer, json.loads(erwateteLecturer))


    def test_lecturerUpdate_PUT_guteDaten_ExpertiseListeHinzufuegen(self):
        """Es fügt mehreren Expertise zu einem Dozent mit eingegebener ID hin, der  früher keine hatte
            Status Code	- 200
            Returnwert	- Erfolgmeldung
            Veränderte Instanz	- Veränderte Instanz
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                     PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                     PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                     INSERT DATA 
                     { kic:TL27 rdf:type kic:Lecturer;
                              kic:hasID "27"^^xsd:string .}"""
        sparql.setQuery(query)
        sparql.query()
        lecturerdaten={
            "expertise":["Haptic", "Emotion", "Hillclimbing"]
        }
        lecturerdatenJSON=json.dumps(lecturerdaten)
        erwartete=b"Update des Lecturers mit ID 27 ist erfolgreich."
        self.lecturerUpdate_url = reverse('kb_service:lecturerUpdate', args=['27'])
        response=self.client.put(self.lecturerUpdate_url, lecturerdatenJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)
        sparql = SPARQLWrapper(fuseki, returnFormat="json")
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
                      ?lecturer kic:hasID  "27"^^xsd:string .  
                      ?lecturer kic:hasID ?id .
                        OPTIONAL {
                            ?lecturer kic:hasExpertise ?expertise .
                            }
                    }"""
        sparql.setQuery(query)
        newLecturer = sparql.query().convert()
        erwateteLecturer = json.dumps({ "head": {
            "vars": [ "lecturer" , "id" , "expertise" ]
            } ,
            "results": {
            "bindings": [
            {
            "lecturer": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL27" } ,
            "id": { "type": "literal" , "value": "27" } ,
            "expertise": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Emotion" }
            } ,
            {
            "lecturer": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL27" } ,
            "id": { "type": "literal" , "value": "27" } ,
            "expertise": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Haptic" }
            } ,
            {
            "lecturer": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL27" } ,
            "id": { "type": "literal" , "value": "27" } ,
            "expertise": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Hillclimbing" }
            }
            ]
            }
            })
        self.assertEquals(newLecturer, json.loads(erwateteLecturer))


    def test_lecturerUpdate_PUT_guteDaten_ExpertiseUmschreiben(self):
        """Es löscht  die alte Expertise von einem Dozent mit eingegebener ID, und fügt mehreren neuen hinzu
            Status Code	- 200
            Returnwert	- Erfolgmeldung
            Veränderte Instanz	- Veränderte Instanz
        """
        sparql = SPARQLWrapper(fuseki + "/update", returnFormat="json")
        sparql.method = 'POST'
        query = """
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                     PREFIX kic: <https://lnv-90209.sb.dfki.de/static/KIC.owl#>
                     PREFIX dom: <https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#>
                     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                     INSERT DATA 
                     { kic:TL28 rdf:type kic:Lecturer;
                              kic:hasID "28"^^xsd:string ;
                              kic:hasExpertise dom:Act.}"""
        sparql.setQuery(query)
        sparql.query()
        lecturerdaten={
            "expertise":["Haptic", "Emotion", "Hillclimbing"]
        }
        lecturerdatenJSON=json.dumps(lecturerdaten)
        erwartete=b"Update des Lecturers mit ID 28 ist erfolgreich."
        self.lecturerUpdate_url = reverse('kb_service:lecturerUpdate', args=['28'])
        response=self.client.put(self.lecturerUpdate_url, lecturerdatenJSON, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)
        sparql = SPARQLWrapper(fuseki, returnFormat="json")
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
                      ?lecturer kic:hasID  "28"^^xsd:string .  
                      ?lecturer kic:hasID ?id .
                        OPTIONAL {
                            ?lecturer kic:hasExpertise ?expertise .
                            }
                    }"""
        sparql.setQuery(query)
        newLecturer = sparql.query().convert()
        erwateteLecturer = json.dumps({ "head": {
            "vars": [ "lecturer" , "id" , "expertise" ]
            } ,
            "results": {
            "bindings": [
            {
            "lecturer": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL28" } ,
            "id": { "type": "literal" , "value": "28" } ,
            "expertise": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Emotion" }
            } ,
            {
            "lecturer": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL28" } ,
            "id": { "type": "literal" , "value": "28" } ,
            "expertise": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Haptic" }
            } ,
            {
            "lecturer": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/KIC.owl#TL28" } ,
            "id": { "type": "literal" , "value": "28" } ,
            "expertise": { "type": "uri" , "value": "https://lnv-90209.sb.dfki.de/static/domain_ontology.owl#Hillclimbing" }
            }
            ]
            }
            })
        self.assertEquals(newLecturer, json.loads(erwateteLecturer))

    def test_lecturerUpdate_PUT_falscheID(self):
        """Es probiert die Daten von einem nicht existierenden Dozent verändern
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """
        lecturerUpdate_url = reverse('kb_service:lecturerUpdate', args=['29'])
        erwartete=b"Es gibt keinen Lehrer mit dem ID 29"
        response = self.client.put(lecturerUpdate_url)
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)

    def test_lecturerUpdate_PUT_falscheAnfrage_Post(self):
        """Es probiert ein falsche Anfrage zu view ordnen
            Status Code	- 200
            Returnwert	- Fehlermeldung
        """
        lecturerUpdate_url = reverse('kb_service:lecturerUpdate', args=['30'])
        erwartete=b"An diese URL darf nur PUT-Anfrage gesendet werden"
        response = self.client.post(lecturerUpdate_url, content_type='application/json')
        result = response.content
        self.assertEquals(response.status_code, 200)
        self.assertEquals(result, erwartete)






