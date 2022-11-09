# Web Scraper


## Algemene Functie
De webscraper zorgt ervoor dat alle relevante informatie over het beoordelingsproces van medicijnen van het internet wordt gehaald. De scraper haalt (op dit moment) informatie van twee verschillende bronnen: de website van de Europese Commissie (EC) en het European Medicine Agency (EMA). Op de website van de EC is er voor ieder medicijn een unieke pagina die informatie bevat over dat medicijn, aangevuld met bestanden (pdf’s) die extra informatie bevatten over beoordelingsprocedures. Daarnaast wordt er ook doorgelinkt naar de EMA website die ook een aparte pagina heeft voor dat medicijn, eveneens met extra informatie en bestanden.  
Er zijn 5 belangrijke python bestanden die ervoor zorgen dat de informatie van deze websites wordt gehaald; ec_scraper.py, ema_scraper.py, download.py, filter_retry.py en __main__.py.

### ec_scraper.py
Het script voor de EC website heeft twee verschillende functionaliteiten. Ten eerste haalt het een lijst op van medicijnen die moet worden gescraped. Voor ieder van deze medicijnen wordt een mapje aangemaakt waar de nodige informatie van het medicijn tijdelijk wordt opgeslagen. Daarnaast zorgt de EC scraper er daadwerkelijk ook voor dat alle nodige informatie van de EC website wordt gehaald. Deze informatie bestaat uit een aantal datapunten voor een medicijn (attributen), links naar extra procedure bestanden (decisions en annexes) en links naar de website van de EMA. De attributen van een medicijn worden in de eerder genoemde map, in een JSON opgeslagen. De links naar decision documenten en annex documenten  voor alle medicijnen worden in één enkele JSON opgeslagen. Dit bestand bevat ook links naar de EMA en wordt later aangevuld door de EMA scraper. 

### ema_scraper.py
ema_scraper.py heeft een soortgelijke functie als de scraper voor de Europese Commissie. Het haalt voor ieder medicijn een aantal attributen op van de website zelf, en het slaat alle linkjes naar bestanden, zodat deze lijst later kan worden gedownload. De attributen worden in de JSON bijgevoegd, evenals de linkjes naar EPAR en OMAR bestanden. Van de EMA website moet ook een lijst van Annex 10 bestanden worden gedownload. Hier is een begin aan gemaakt, maar is nog niet af.

### download.py
Het downloadscript zorgt ervoor dat de JSON met linkjes naar bestanden (die zijn gescraped door ec_scraper.py en ema_scraper.py) ook daadwerkelijk worden opgeslagen. Het download ieder decision, annex, EPAR of OMAR bestand naar de juiste medicijnmap. Ieder bestand dat niet kon worden gedownload wordt gelogd. 

### filter_retry.py
Gebaseerd op het .txt bestand dat de filtermodule aan de webscraper geeft, wordt voor de bestanden die in eerste instantie niet gedownload konden worden en nieuwe poging gedaan om ze te downloaden. 

### __main__.py
Dit script is wat de volledige webscraper aanstuurt. Het kan bepaalde delen van de webscraper aan en uit zetten, zodat het niet altijd in zijn volledigheid loopt. Als alles wel aan staat, zal eerst de lijst met te scrapen medicijnen van de EC website worden gehaald. Vervolgens wordt alle benodigde informatie voor ieder van deze medicijnen van de EC website gehaald. Dit bevat dus ook linkjes naar de EMA website. Met deze linkjes kan vervolgens de EMA website worden gescraped. Als laatste worden alle linkjes naar bestanden op de EC en EMA website gedownload.


## Input & Output
Deze module start, wanneer deze voor het eerst wordt aangeroepen, zonder input. Het haalt alle benodigde informatie van de EC website af, en kan daarmee zelfstandig aan de slag. Voor ieder medicijn wordt een apart mapje gemaakt waar alle informatie omtrent dat medicijn wordt opgeslagen. Alle attributen die rechtstreeks van de EC en EMA websites af worden gehaald worden in een JSON bestand gezet. Ook worden alle procedure bestanden voor een medicijn in diezelfde map opgeslagen wanneer ze worden gedownload. De bestanden die in de mapjes staan worden door de filter module onder handen genomen. Het kan namelijk zijn dat het bestand dat is gedownload corrupt, een html pagina, of een plaatje is. De filter maakt een lijst met alle bestanden die niet goed zijn en koppelt dit terug aan de websraper, zodat deze bestanden opnieuw gedownload kunnen worden.
De goede pdf-bestanden die in de mapjes staan worden onder handen genomen door de pdf scraper, die op zijn beurt ook weer attributen voor medicijnen ophaalt. De JSON met attributen die direct van de website zijn gehaald, de JSON met attributen uit de pdf scraper en JSON’s van externe bronnen worden aan de combiner gegeven, zodat inconsistente informatie correct kan worden opgeslagen in de database.

## Overige belangrijke punten



This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.

© Copyright Utrecht University (Department of Information and Computing Sciences)
