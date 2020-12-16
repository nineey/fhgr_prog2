
# Votery  
Dieses Projekt ist im Rahmen des Moduls *Programmierung 2* an der Fachhochschule Graubünden entstanden.   
  
## Ausgangslage  
In einem Team mit mehreren Mitarbeitern gibt es Abstimmungen über Produkte, mit denen Sonderaktionen durchgeführt werden sollen. Bis anhin fanden diese Abstimmungen per umständlichem Mail-Verkehr statt.   
  
## Projekt – Votery  
Das Tool ***Votery*** unterstützt das Team bei beim Abstimmungsprozess, indem alle Produkte und zugehörige Abstimmungsergebnisse zentral gespeichert werden. Ein Login für ***Votery*** sorgt dafür, dass einfach für Produkte gevoted werden kann.   
  
## Installation  
Damit du ***Votery*** lokal starten kannst, benötigst du folgende Installationen (getestete Version):   
 - `Python (3.8)`  
 - `Flask (1.1.2)`  
 - `Jinja2 (2.11.2)`  
 - `Plotly (4.13.0)`  
 
 Zusätzlich ist eine aktive Internetverbindung vorausgesetzt.   
  
Im Anschluss kann das Tool mit dem Befehl `python app.py` gestartet und über den Localhost (i.d.R 127.0.0.1, Port 5000) aufgerufen werden.   
  
## Anforderungen  
Für die Umsetzung des Projekts wurden die folgenden Anforderungen definiert:   
  
1. Der Benutzer muss sich registrieren bzw. einloggen können.   
2. Der Benutzer muss ein neues Produkt erfassen und damit eine neue Abstimmung eröffnen können.   
3. Der Benutzer muss sein Voting zu bereits erfassten Produkten abgeben können.   
4. Der Benutzer muss Kategorien und Logins verwalten können.   
5. Der Benutzer muss die Abstimmungsergebnisse prüfen können.   
6. Der Benutzer muss erfasste Produkte bearbeiten können.   
  
## Workflow  
  
### Dateneingabe  
Der Benutzer kann über das UI neue Produkte erfassen oder über die Detailsansicht Produkte bearbeiten. Zudem können neue Kategorien und weitere Benutzer ergänzt werden. 

### Datenverarbeitung / Speicherung
Die eingetragenen Daten werden im Ordner `data` ins das jeweilige JSON-File abgespeichert:

**data.json**
 - Dict mit Produktdaten und Votings

**categories.json**
 - Liste mit allen Kategorien

**users.json**
 - Dict mit verschlüsselten Login-Daten

### Datenausgabe
Die Daten werden entsprechend der URL, die der Benutzer aufruft, vom JSON gelesen. Im Anschluss werden die notwendigen Daten mittels Jinja im Front-End ausgegeben. 

## Benutzeranleitung
folgt...