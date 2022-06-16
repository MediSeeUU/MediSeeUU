# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import pandas as pd
import numpy as np

#data preparation before sending to the scraper endpoints
df = pd.read_excel('output.xlsx')

#rename columns to correct names
df.columns = ['emanumberlong', 'emanumber', 'emanumber_confidence', 'emanumber_doublecheck', 'eunumberlong',
              'eunumber', 'brandname', 'mah', 'status', 'ecurl', 'emaurl', 'activesubstance', 'authorisationprocedure', 'authorisationdate',
              'decisionurl', 'annexurl', 'recentprocedure', 'atccode', 'atcname', 'decisiontype', 'otherbrandname', 'legalscope', 'decision_date',
              'orphan', 'atmp', 'newactivesubstance', 'decision_type', 'prime', 'legalbasis' ]

#Usefull columns for current scraper
df = df[['emanumber', 'eunumber', 'brandname', 'mah', 'status', 'ecurl', 'emaurl', 'activesubstance', 'decisionurl', 'annexurl', 
         'atccode', 'legalscope', 'orphan', 'atmp', 'newactivesubstance', 'decision_type', 'prime', 'legalbasis']]
#Use (nullable) integer types for emanumber and eunumber
df['emanumber'] = df['emanumber'].astype('Int64')
df['eunumber'] = df['eunumber'].astype('Int64')

#replace yes/no with 0 (false) and 1 (true)
df['atmp'] = df['atmp'].replace({'no':0, 'yes':1})
df['orphan'] = df['orphan'].replace({'no':0, 'adopted':1, 'appointed':1})
df['prime'] = df['prime'].replace({'no':0, 'yes':1})
df['newactivesubstance'] = df['newactivesubstance'].replace({'no':0, 'yes':1})
#change dataframe to json format (oriented on the rows)
data = df.to_json(orient='records')

#insert data into scraper endpoint format
scraper_data = ("{"
                "\"override\": false,"
                f"\"data\": {data}"    
                "}")

#example of post request to scraper endpoints
import requests

API_ENDPOINT = "[input url to scraper endpoint here]"

API_KEY = "Token [input token key for api here]"

API_HEADERS={
    'Content-type':'application/json', 
    'Accept':'application/json',
    'Authorization': API_KEY
}

# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, headers= API_HEADERS, data = scraper_data)

#write failed rows to output file, (so this can be checked later)
with open('failedMedicines.txt', 'w') as f:
    f.write(r.text)
    f.close()