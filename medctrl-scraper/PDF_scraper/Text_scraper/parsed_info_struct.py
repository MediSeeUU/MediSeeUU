import datetime


class parsed_info_struct:
    parse_date: datetime.date
    medicine_name: str
    shelf_life: str

    def __init__(self):
        self.parse_date = datetime.datetime.date
