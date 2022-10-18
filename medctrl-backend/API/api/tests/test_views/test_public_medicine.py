from django.test import TestCase, Client
from django.contrib.auth.models import Group, User, Permission
from api.models.medicine_models.common import Category
from api.views.other import get_medicine_info
from api.management.commands.create_column_permissions import Command as createColumnPermissions
from api.management.commands.init_setup import Command as InitSetup


class PublicMedicineTestCase(TestCase):
    def test_structure_equal_medicine(self):
        """
        tests if the output from structureData has the same keys as public medicine
        """
        createColumnPermissions().handle()
        InitSetup().handle()
        anonymous = Group.objects.get(name="anonymous")
        anonymous.permissions.set(Permission.objects.values())
        c = Client()
        response = c.get('/api/structureData/')
        self.assertEqual(response.status_code, 200)
