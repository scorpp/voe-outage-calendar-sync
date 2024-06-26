"""
URL configuration for voe_outage_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path

from voe_outage_sync.views import ICalView, IndexView, RunSyncView

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("sync/run", RunSyncView.as_view(), name="run-sync"),
    path("ical/<str:city>/<str:street>/<str:building>.ics", ICalView.as_view(), name="ical-view"),
]
