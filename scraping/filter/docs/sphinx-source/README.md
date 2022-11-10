# General
Filter checks whether all PDF files in the map with medicijnen are correct.
Incorrect PDF files will be deleted and logged as a line in filter.txt.

Error types:
- corrupt (if PDF file cannot be opened)
- html (if the content of the PDF files is actually an HTML file)
- unknown (if the file can't be opened in utf8 format for the HTML check)
- wrong_doctype (if the PDF file is a different type than the filename suggests)

# Input & Output
## Input
Location of the data folder with medicines
## Output
- filter.txt containing the following line for each incorrect PDF file:
  - "{name of PDF}@{error type}@{URL}" for EPAR, OMAR and Annex files
  - "{name of PDF}@{error type}@{EU number}@{Brand name}@{url}" for a decision PDF
- data folder without the incorrect PDF files

# Other points of interest
After one run, all incorrect PDF files will be removed.
Therefore, filter.txt will be empty after two runs.
Make sure to make a backup if the filtered files relevant and you want to run filter again.