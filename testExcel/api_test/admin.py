from django.contrib import admin
from .models import Operateur, Post, Tache

admin.site.register(Post)
# Register your models here.

admin.site.register(Operateur)
admin.site.register(Tache)