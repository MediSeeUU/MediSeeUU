# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all functions that create a custom template for
# the django backend. This custom template extends the default django admin
# panel template with the means to crate a token that a scraper can use to
# access the backend.
# -------------------------------------------------------------------

import datetime
from django.views.generic import FormView
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib import messages
from knox.models import AuthToken
from django.conf import settings
import logging

base_url = settings.BASE_URL if "BASE_URL" in dir(settings) else ""

logger = logging.getLogger(__name__)


class GenerateKeyForm(forms.Form):
    """
    Generate a form to get key for api user
    """    
    # creates a dropdown menu with specified users, filtered from the entire user base
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=0)
        .filter(is_staff=0)
        .filter(~Q(username="AnonymousUser"))
    )
    user.widget.attrs.update({"style": "width: 100px"})
    duration = forms.IntegerField(min_value=1, max_value=365)
    duration.widget.attrs.update({"style": "width: 86px"})


# Creates view for for the django admin page
class GenerateKeyView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """
    Generate a view to get key for api user
    """
    form_class = GenerateKeyForm
    template_name = "generateApiKeyTemplate.html"
    success_url = f"/{base_url}admin"
    login_url = f"/{base_url}admin/login/"

    def form_valid(self, form):
        """
        Creates a token when a form is submitted via the django admin pannel.

        Args:
            form (djangoForm): A form submitted via the django admin panel.

        Returns:
            super.url: will return the url if the form is valid.
        """        
        duration = form.cleaned_data["duration"]
        user = form.cleaned_data["user"]
        logger.info("API duration: " + str(duration) + "API user" + str(user))

        instance, token = AuthToken.objects.create(
            user, datetime.timedelta(days=duration)
        )
        logger.info("API Key generated: " + str(token))

        messages.success(self.request, "The generated api key is: " + str(token))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Gets the context in which the data should be used in the serializer.

        Returns:
            any: The corresponding context.
        """        
        context = super().get_context_data(**kwargs)
        return context

    def test_func(self):
        """
        Returns a boolean depending on the usertype of the user.

        Returns:
            bool: returns true if the user is a superuser
        """        
        return self.request.user.is_superuser
