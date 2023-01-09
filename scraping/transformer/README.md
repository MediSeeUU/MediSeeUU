# General
The main functionality of the file scraper is to transform the format of the combined.json file 
for each medicine such that it is in the format accepted by the database.

This module will produce a transformed.json for each combined.json file. It will remove the human 
attributes from orphan medicines, and remove the orphan attributes from human medicines.
These attributes will have null values after all.

The module will also convert all types of "Not found" strings (like "COMBINER_NOT_FOUND" and "SCAPER_NOT_FOUND") when an attribute is not found,
to a generic "Not found".

# Input & Output
## Input
The filepath of the data folder containing the active_withdrawn folder,
which will contain all human and orphan medicines.

## Output
- A JSON file for every medicine, containing all attributes of that medicine that are relevant for the database.
  - JSON name format: `{EU_number}_transformed.json`

# Other points of interest
This module is basically an extension of the combiner, so it could become part of the combiner in the future.

© Copyright Utrecht University (Department of Information and Computing Sciences)
