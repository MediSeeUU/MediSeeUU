# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
"""api_settings URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
import api.urls
from api.views.generate_key_views import GenerateKeyView

# Set base url if it exists in the settings file
base_url = settings.BASE_URL if "BASE_URL" in dir(settings) else ""

urlpatterns = [
    path(
        base_url,
        include(
            [
                path("admin/doc/", include("django.contrib.admindocs.urls")),
                path(
                    "admin/generateApiKey",
                    GenerateKeyView.as_view(),
                    name="generate_key",
                ),
                path("admin/", admin.site.urls),
                path("", include(api.urls)),
            ]
        ),
    )
]
