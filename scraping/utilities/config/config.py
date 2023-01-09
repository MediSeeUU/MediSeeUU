import json
filename = "scraping_config.txt"

run_web = 'run_web'
run_xml = 'run_xml'
run_pdf = 'run_pdf'
run_annex_10 = 'run_annex_10'
run_combiner = 'run_combiner'
run_transformer = 'run_transformer'
run_db_com =  'run_db_communicator'
xml_convert_all = 'xml_convert_all'
pdf_parse_all = 'pdf_parse_all'
db_com_send_together = 'db_com_send_together'

default_config = {
    run_web: True,
    run_xml: True,
    run_pdf: True,
    run_annex_10: True,
    run_combiner: True,
    run_transformer: True,
    run_db_com: True,
    xml_convert_all: False,
    pdf_parse_all: False,
    db_com_send_together: True
}

def load_config():
  try:
    with open(filename, 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    with open(filename, 'w') as f:
      json.dump(default_config, f, indent=4)
      return default_config
