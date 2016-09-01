from django.contrib import admin

from .models import Category, Choice, CustomUser, Question


# admin.site.register(Answer)
admin.site.register(Category)
admin.site.register(Choice)
admin.site.register(CustomUser)
admin.site.register(Question)
