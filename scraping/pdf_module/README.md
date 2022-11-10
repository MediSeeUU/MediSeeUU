# Algemene functie
PDF Scraper haalt alle relevante attributen uit PDF files per PDF type.

PDF Types:
- EC Decision
- Annex files
- EPAR
- OMAR

Dit wordt deels gedaan met behulp van de XML converter.
Deze converteert alle PDF files naar XML formaat, waarna deze XML files
worden gescraped. De EC scraper maakt geen gebruik van de XML converter:
deze scraped de PDF bestanden direct.
# Input & Output
## Input
Locatie van data
## Output
- XML bestand voor elk PDF bestand in zelfde map als PDF bestand.
- JSON bestand voor elk medicijn, met alle relevante attributen van dat medicijn.
  - JSON naam format: {EU_number}_pdf_parser.json
# Overige belangrijke punten
Het parsen vanuit XML files is sneller dan vanuit PDF files door het snellere lezen.
Het kost wat tijd om de XML files te maken, maar dit hoeft maar één keer.

Visualisatie van gescrapede attributen: [Visualisaties PDF](MediSee_PDF_visualisation.html)