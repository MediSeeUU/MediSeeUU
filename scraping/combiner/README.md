# General
Combiner combines the PDF json and web scraper json file in each medicine folder.
It cross-checks several attributes of the PDF scraper with the attributes of the web scraper, 
to make sure the attributes are as correct as possible. **It is currently not functional.**

# Input & Output
## Input
Location of the data folder.

## Output
A {EU_num}_combined_attributes.json file for each medicine.
## Todo
### Voeg een beschrijving to van elke attribuutwaarde. Voorbeeld hieronder in comment.
[

"__SCRAPER_NOT_FOUND__": waarde is niet gevonden in PDF
"attribute not available on release": datum van PDF ligt vóór datum waarop het attribuut werd geïntroduceerd
"Value should be present in document": waarde is hoogstwaarschijnlijk aanwezig in PDF, bijvoorbeeld als de string "rapporteur:" voorkomt, maar de waarde zelf is lastig te scrapen (edge case).
“__COMBINER NOT FOUND___”: Combiner vond geen waarde voor een attribuut van een medicijn in de PDF en web data
“| -> INSUFFICIENT OVERLAP <-|”: Combiner merkt dat de waarden van twee verschillende bronnen totaal niet overeenkomen. Normaalgesproken moet de waarde uit de kortere string voor X% overeenkomen met de waarde van de langere string om een waarde te returnen. Is dat niet zo? Dan geeft de combiner nu deze waarde (volgens mij moest dit zo aangepast worden dat de combiner wel een daadwerkelijke waarde teruggeeft, maar tegelijkertijd logt dat de waarden niet overeenkomen).

]::

# Other points of interest
Not yet implemented.