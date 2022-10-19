from django.test import TestCase, Client
from django.contrib.auth.models import Group, User, Permission
from api.models.medicine_models.common import Category
from api.views.other import get_medicine_info
from api.management.commands.create_column_permissions import Command as createColumnPermissions
from api.management.commands.init_setup import Command as InitSetup


class PublicMedicineTestCase(TestCase):
    def setUp(self):
        createColumnPermissions().handle()
        InitSetup().handle()
        self.client = Client()
        self.user = User.objects.filter(is_superuser=True)

    def test_structure_equal_medicine(self):
        """
        tests if the output from structureData has the same keys as public medicine
        """
        response = self.client.get('/api/structureData/')
        self.assertEqual(response.status_code, 200)
