from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ManageMyHome.models import *

# Register your models here.
admin.site.register(t_user, UserAdmin)
admin.site.register(t_heaterTechnologie)
admin.site.register(t_house)
admin.site.register(t_document)
admin.site.register(t_picture)
admin.site.register(t_project)
admin.site.register(t_provide)
admin.site.register(t_company)
admin.site.register(t_contact)
admin.site.register(t_work)