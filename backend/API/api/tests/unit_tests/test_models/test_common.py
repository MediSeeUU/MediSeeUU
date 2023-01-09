# from django.test import TestCase
# from api.models.common import Category, create_dashboard_column
#
# class DashboardColumnTestCase(TestCase):
#     def test_create_dashboard_column1(self):
#         field1 = Object()
#         category1 = Category.Additional_Resources
#         format1 = "string"
#         value1 = "Title"
#         create_dashboard_column(field1, category1, format1, value1)
#         self.assertEqual(field1.dashboard_columns[0].category, category1)
#         self.assertEqual(field1.dashboard_columns[0].data_format, format1)
#         self.assertEqual(field1.dashboard_columns[0].data_value, value1)
#
#     def test_create_dashboard_column2(self):
#         field2 = Object()
#         category2 = Category.Identifying_Information
#         format2 = "int"
#         value2 = "Value"
#         create_dashboard_column(field2, category2, format2, value2)
#         self.assertEqual(field2.dashboard_columns[0].category, category2)
#         self.assertEqual(field2.dashboard_columns[0].data_format, format2)
#         self.assertEqual(field2.dashboard_columns[0].data_value, value2)
#
# class Object:
#     pass
