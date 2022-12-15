"""LiquidBundle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from . import views, api_views


admin.AdminSite.site_header = 'Jack Tembo\'s Administration'
admin.AdminSite.site_title = 'Jack Tembo Administration'


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('reduce-amount-api', api_views.ReduceAmount.as_view()),
    path('pay', api_views.PayInvoice.as_view()),
    path('reduce-amount', views.reduce_amount, name='reduce-amount'),
    path('buy-liquid-data', views.buy_liquid_bundle, name='buy-liquid-data'),

]
