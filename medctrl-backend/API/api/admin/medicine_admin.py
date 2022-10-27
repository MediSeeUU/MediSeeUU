# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import Medicine
from api.admin.cachemodeladmin import CacheModelAdmin


class MedicineResource(resources.ModelResource):
    """
    Necessary resource class for the Medicine admin view.
    ModelResource is Resource subclass for handling Django models.
    """    
    class Meta:
        """
        Meta class for MedicineResource
        """
        model = Medicine
        import_id_fields = ("eu_pnumber",)


class MedicineAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Medicine, contains a list of all the shown attributes.
    """
    resource_class = MedicineResource
    list = (
        "eu_pnumber",
        "active_substance",
        "eu_nas",
        "ema_procedure_start_initial",
        "chmp_opinion_date",
        "eu_aut_date",
        "eu_legal_basis",
        "ema_url",
        "ec_url",
        "ema_number",
        "eu_med_type",
        "eu_atmp",
        "ema_number_check",
        "ema_rapp",
        "ema_corapp",
        "eu_accel_assess_g",
        "eu_accel_assess_m",
        "assess_time_days_total",
        "assess_time_days_active",
        "assess_time_days_cstop",
        "ec_decision_time_days",
        "ema_reexamination",
        "eu_referral",
        "eu_suspension",
        "omar_url",
        "odwar_url",
        "eu_od_number",
        "ema_od_number",
        "eu_od_con",
        "eu_od_date",
        "eu_od_pnumber",
        "eu_od_sponsor",
        "eu_od_comp_date"
    )

    def save_model(self, request, obj, form, change: bool):
        """
        This is a Django Admin function that saves the model.

        Args:
            request (Any): This is a HttpRequest.
            obj (Any): This is the instance of the model.
            form (Any): This is the ModelForm instance.
            change (bool): This boolean decides whether the object is being changed or added to.
        Returns:
            None
        """        
        # Get reference to previous object
        med = Medicine.objects.filter(eu_pnumber=obj.eu_pnumber).first()

        # Check if the manually updated checkbox has been unchecked
        if not med.manually_updated:
            obj.manually_updated = True
        super().save_model(request, obj, form, change)


admin.site.register(Medicine, MedicineAdmin)
