# This file contains all functions that create a custom template for
# the django backend. This custom templete extends the default django admin 
# panel templat with the means to crate a token that a scraper can use to 
# access the backend.
#-------------------------------------------------------------------

import datetime
from django.views.generic import FormView
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib import messages
from knox.models import AuthToken
from django.conf import settings

base_url = settings.BASE_URL if "BASE_URL" in dir(settings) else ""

#Creats form on django admin panel
class GenerateKeyForm(forms.Form):
    """
    Generate form to get key for api user
    """

    #creates a dropdown menu with specified users, filtered from the entire user base
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=0)
        .filter(is_staff=0)
        .filter(~Q(username="AnonymousUser"))
    )
    user.widget.attrs.update({"style": "width: 100px"})
    duration = forms.IntegerField(min_value=1, max_value=365)
    duration.widget.attrs.update({"style": "width: 86px"})

#Creates view for for the django admin page
class GenerateKeyView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """
    Generate view to get key for api user
    """

    form_class = GenerateKeyForm
    template_name = "generateApiKeyTemplate.html"
    success_url = f"/{base_url}admin"
    login_url = f"/{base_url}admin/login/"

    #Creates a token when form is submitted via the django admin panel
    def form_valid(self, form):
        duration = form.cleaned_data["duration"]
        user = form.cleaned_data["user"]

        instance, token = AuthToken.objects.create(
            user, datetime.timedelta(days=duration)
        )
        messages.success(self.request, "The generated api key is: " + str(token))
        return super().form_valid(form)

    #gets the context in which the data should be used in the serializer
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    #Returs bolean value true if superuser
    def test_func(self):
        return self.request.user.is_superuser
