"""testExcel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from api_test.views import OperateurRUD,ReconcileUpdate,TrxRightCorrespodentb,TrxRightCorrespodentRUDView,TrxDifferenceRUDView,TrxDifferenceView, OperateurView,ProfileView,ProfileRUD, TacheRUD, TacheView,TokenView, Test_view,Reconcile,Cinetpay
from api_test import views
from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('reconcile/', include('reconcile.urls')),
    path('api_test/', include('api_test.urls')),
    path('admin/', admin.site.urls),
    path('get_user/',TokenView.as_view(),name="token"),
    path('', Test_view.as_view(), name='test'),
    path('reconciliation/', Reconcile.as_view(), name='reconcile'),
    path('update_reconciliation/<int:pk>/', ReconcileUpdate.as_view(), name='reconcile'),
    path('reconciliation/verification/', Reconcile.as_view(), name='reconcile'),
    path('cinetpay/', Cinetpay.as_view(), name='cinetpay'),
    # path('auth/', include('rest_framework_social_oauth2.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('authentication/', include('users.urls')),
    path('operateurs/', OperateurView.as_view(), name='olc'),
    path('operateurs/<int:pk>/', OperateurRUD.as_view(), name='orud'),
    path('profiles/', ProfileView.as_view(), name='plc'),
    path('profiles/<int:pk>/', ProfileRUD.as_view(), name='prud'),
    path('taches/', TacheView.as_view(), name='tlc'),
    path('taches/<int:pk>/', TacheRUD.as_view(), name='trud'),
    path('<int:tache_id>/trxdifferences/', TrxDifferenceView.as_view(), name='trxdifferences'),
    path('<int:tache_id>/trxdifferences/<int:pk>/', TrxDifferenceRUDView.as_view(), name='trxdifference'),
    path('<int:tache_id>/trxrightcorrespodent/', TrxRightCorrespodentb.as_view(), name='trxrightcorrespodent'),
    path('<int:tache_id>/trxrightcorrespodent/<int:pk>/', TrxRightCorrespodentRUDView.as_view(), name='rudtrxrightcorrespodent'),
    # path('export/<int:pk>/', ExportFile.as_view(), name='trud'),
]
