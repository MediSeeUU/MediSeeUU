from django.test import TestCase
from api.models.medicine_models.common import Category
from api.views.other import get_medicine_info


class MedicineInfoTestCase(TestCase):
    def test_get_medicine_info(self):
        field1 = Object()
        setattr(field1, "name", "field1")
        setattr(field1, "category", Category.General_Information)
        setattr(field1, "data_format", "format1")
        setattr(field1, "data_value", "title1")
        field2 = Object()
        setattr(field2, "name", "field2")
        setattr(field2, "category", Category.Additional_Resources)
        setattr(field2, "data_format", "format2")
        setattr(field2, "data_value", "title2")
        field3 = Object()
        setattr(field3, "name", "field3")
        setattr(field3, "category", Category.General_Information)
        setattr(field3, "data_format", "format3")
        setattr(field3, "data_value", "title3")

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
