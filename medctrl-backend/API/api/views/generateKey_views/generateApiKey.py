from django.views.generic import FormView
from django import forms
from django.contrib.auth.models import User
from api.models.medicine_models import Medicine
from django.db.models import Q
from django.contrib import messages
from knox.models import AuthToken
import datetime


class GenerateKeyForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=0)
        .filter(is_staff=0)
        .filter(~Q(username="AnonymousUser"))
    )
    user.widget.attrs.update({"style": "width: 100px"})
    duration = forms.IntegerField(min_value=1, max_value=365)
    duration.widget.attrs.update({"style": "width: 86px"})


class GenerateKeyView(FormView):
    form_class = GenerateKeyForm
    template_name = "generateApiKeyTemplate.html"
    success_url = "/admin/"

    def form_valid(self, form):
        duration = form.cleaned_data["duration"]
        user = form.cleaned_data["user"]

        instance, token = AuthToken.objects.create(
            user, datetime.timedelta(days=duration)
        )
        messages.success(self.request, "The generated api key is: " + str(token))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
