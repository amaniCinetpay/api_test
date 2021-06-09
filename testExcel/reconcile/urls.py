from django.urls import path

from . import views


app_name='reconcile'
urlpatterns = [
    path('', views.index, name='index'),
    path('excel-to-json/', views.excel_to_json, name='excel_to_json'),
    path('reconcile/', views.reconcile, name='reconcile'),
    path('update_transaction/', views.update_transaction, name='update_transaction'),
]