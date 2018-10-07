"""coreui_boilerplate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.defaults import page_not_found

import logistica.views as logistica



urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', logistica.home, name='home'),

    url(r'^login/', logistica.login_user, name='login_user'),
    url(r'^logout/', logistica.logout_user, name='logout_user'),

    url(r'^actividades/', logistica.activities, name='activities'),
    url(r'^principal/', logistica.principal, name='principal'),
    url(r'^tour/', logistica.create_tour_request, name='tour'),
    url(r'^showTour/', logistica.save_tour_option, name='showTour'),

    url(r'^edit_activity_capacity/', logistica.edit_activity_capacity, name='edit_activity_capacity'),

    url(r'^monitor/(?P<pk_monitor>[0-9A-Za-z_\-]+)/$', logistica.monitor, name='monitor'),
    url(r'^monitor/', logistica.monitor, name='monitor'),

    url(r'^espacio/(?P<pk_espacio>[0-9A-Za-z_\-]+)/$', logistica.espacio, name='espacio'),
    url(r'^espacio/', logistica.espacio, name='espacio'),

    url(r'^espacio_master/', logistica.espacio_master, name='espacio_master'),

    url(r'^profile/', logistica.monitorProfile, name='profile'),
    url(r'^update/', logistica.updateActividad, name='update'),

    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


