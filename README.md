# REST-API
REST-API im Rahmen des KI-Campus-Projekts von DFKI
Die Aufgabe ist ein Teil des KI-Campus-Projekts, bei dem es darum geht, eine Online-Lernplattform 
zum Thema künstliche Intelligenz aufzubauen. Auf der Lernplattform gibt es Nutzer*innen, die 
verschiedene Kurse belegen können. Es gibt mehrere KI-Anwendungen (z.B. ein 
Empfehlungssystem, einen Chatbot), welche die Nutzer*innen dabei unterstützen, die passenden 
Kurse zu finden.
Im Rahmen des Projektes wurde eine Ontologie (eine Wissensbasis) entwickelt, in der die 
Abhängigkeiten zwischen den auf dem KI-Campus vertretenen Themen abgebildet sind. Sowohl die 
Kurse als auch die Nutzer*innen sollen mit „Themenschlagwörtern“ markiert werden. In Bezug auf 
die Kurse bedeutet das, dass erkennbar ist, welche Themen sie behandeln und in welchem Bezug 
sie zu den anderen Kursen des KI-Campus stehen (z.B. grundlegender Kurs, Folgekurs, 
Anwendungskurs für Grundlagen xyz, etc.). In Bezug auf die Nutzer*innen bedeutet dies, dass ihre 
Interessen und ihr Vorwissen formalisiert werden und auf dieser Basis passende Kurse empfohlen 
werden können.
Der Hauptteil des Projektes besteht in der Entwicklung eines Webservices, der die beschriebene 
Ontologie aktualisiert. Über eine REST-API werden POST-, PUT- und DELETE-HTTP-Anfragen an den 
Webservice gesendet. Dieser wandelt die Anfrage in SPARQL-Queries um und verwaltet mithilfe 
eines Apache Jena Servers die Ontologie, die entsprechend der eingehenden Befehle neue 
Instanzen in der Ontologie anlegt, bestehende aktualisiert oder nicht mehr benötigte löscht. Der 
Webserivce wird mit Python umgesetzt, mithilfe das Django Pythonpacket. Die Entwicklung wird 
mit Postman unterstützt.
