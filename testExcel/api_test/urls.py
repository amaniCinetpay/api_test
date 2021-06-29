from django.contrib import admin
from django.urls import include, path
from api_test.views import Catered, OperateurRUD,CateredDdva, OperateurView, TacheRUD, TacheView, Test_view,Reconcile,Cinetpay 
from api_test import views
from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework.routers import DefaultRouter


app_name='api_test'
urlpatterns = [
    path('reconciliation/', Reconcile.as_view(), name='reconciliation'),
    path('reconciliation/verification/', Reconcile.as_view(), name='reconcile'),
    path('catered/', Catered.as_view(), name='catered'),
    path('cinetpay/', Cinetpay.as_view(), name='cinetpay'),
    # path('auth/', include('rest_framework_social_oauth2.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('authentication/', include('users.urls')),
    path('operateurs/', OperateurView.as_view(), name='olc'),
    path('operateurs/<int:pk>/', OperateurRUD.as_view(), name='orud'),
    path('taches/', TacheView.as_view(), name='tlc'),
    path('taches/<int:pk>/', TacheRUD.as_view(), name='trud'),
    path('catered_ddva/', CateredDdva.as_view(), name='catered_ddva'),
    
]



