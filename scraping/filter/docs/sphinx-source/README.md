# Algemene functie
Filter checkt of alle PDF bestanden in een map met medicijnen correct zijn.
Incorrecte PDF bestanden worden verwijderd en gelogd als een regel in filter.txt.

Error types:
- corrupt (als PDF bestand niet geopend kan worden)
- html (als de inhoud van het PDF bestanden een html site blijkt te zijn)
- unknown (als do file niet geopend kan worden in utf8 formaat voor de HTML check)
- wrong_doctype (als het PDF bestand niet van het type is dat in de filename staat)

# Input & Output
## Input
Locatie van data map met medicijnen
## Output
- filter.txt met per incorrect PDF bestand de volgende regel:
  - "{naam van PDF}@{error type}@{URL}" voor EPAR, OMAR en Annex PDF bestanden
  - "{naam van PDF}@{error type}@{EU nummer}@{Brand name}@{url}" voor een decision PDF
- data folder zonder incorrecte PDF bestanden

# Overige belangrijke punten
Na een keer filter uitvoeren zijn alle incorrecte bestanden verwijderd, 
na twee keer uitvoeren zal filter.txt dus ook leeg zijn.