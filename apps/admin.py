from django.contrib import admin
from .models import NewPerson, User, ContactsUser

admin.site.register(NewPerson)
admin.site.register(User)
admin.site.register(ContactsUser)
