from ldapdb.models.fields import CharField
import ldapdb.models
from django.contrib import admin


class Meta:
    app_label = 'ldap_profile'

fields = {
    'object_classes': ['inetOrgPerson', 'organizationalPerson'],
    'email': CharField(db_column='mail', max_length=200, unique=True),
    'name': CharField(db_column='cn', max_length=200, primary_key=True),
    'username': CharField(db_column='sn', max_length=200, unique=False),
    'Meta': Meta,
    '__module__': 'ldap_profile.models',
    '__str__': lambda self: self.name,
    '__unicode__': lambda self: self.name, }

fields.update({
    'base_dn': 'dc=transfer-tic,dc=org'})
Profile = type('Profile', (ldapdb.models.Model, ),
                        fields.copy())

fields.update({
    'base_dn': 'ou=formateur,ou=Usersdev,dc=transfer-tic,dc=org'})
ProfileFormateur = type('ProfileFormateur', (ldapdb.models.Model, ),
                        fields.copy())

fields.update({
    'base_dn': 'ou=participant,ou=users,dc=transfer-tic,dc=org'})
ProfileParticipant = type('ProfileParticipant', (ldapdb.models.Model, ),
                          fields.copy())

fields.update({
    'base_dn': 'ou=encadrant,ou=users,dc=transfer-tic,dc=org'})
ProfileEncadrant = type('ProfileEncadrant', (ldapdb.models.Model, ),
                          fields.copy())


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email')
    search_fields = ('name', 'username', 'email')
