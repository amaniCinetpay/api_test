from django.contrib import admin
from .models import Operateur, Post, Tache, Role,Profile

admin.site.register(Post)
# Register your models here.

admin.site.register(Operateur)


admin.site.register(Profile)

admin.site.register(Role)
admin.site.register(Tache)