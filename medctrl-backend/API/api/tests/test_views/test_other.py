from django.test import TestCase
from api.models.medicine_models.common import Category, create_dashboard_column
from api.views.other import get_medicine_info


class MedicineInfoTestCase(TestCase):
    def test_get_medicine_info(self):
        field1 = Object()
        setattr(field1, "db_column", "field1")
        setattr(field1, "name", "field1")
        field1 = create_dashboard_column(field1, Category.General_Information, "format1", "title1")
        field2 = Object()
        setattr(field2, "db_column", "field2")
        setattr(field2, "name", "field2")
        field2 = create_dashboard_column(field2, Category.Additional_Resources, "format2", "title2")
        field3 = Object()
        setattr(field3, "db_column", "field3")
        setattr(field3, "name", "field3")
        field3 = create_dashboard_column(field3, Category.General_Information, "format3", "title3")

        mock = [field1, field2, field3]
        perm = ["field1", "field2"]
        data = get_medicine_info(perm, mock)
        expected = {
            "General Information": [
                {
                    "data-key": "field1",
                    "data-format": "format1",
                    "data-value": "title1"
                }
            ],
            "Identifying Information": [],
            "(Co-)Rapporteur": [],
            "Medicine Designations": [],
            "Legal Information": [],
            "Authorisation Timing": [],
            "Additional Resources": [
                {
                    "data-key": "field2",
                    "data-format": "format2",
                    "data-value": "title2"
                }
            ]
        }
        self.assertEqual(data, expected)


class Object:
    pass
