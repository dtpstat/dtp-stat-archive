from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.indexes import Index



class Region(models.Model):
    name = models.CharField(max_length=1000, help_text="Region name", null=True, blank=True, default=None, db_index=True)
    alias= models.CharField(max_length=1000, help_text="Region alias", null=True, blank=True, default=None, db_index=True)
    oktmo_code = models.CharField(max_length=20, help_text="Region oktmo code", null=True, blank=True, default=None, db_index=True)
    level = models.IntegerField(help_text="Region level", null=True, blank=True, default=None, db_index=True)
    parent_region = models.ForeignKey('self', help_text="Parent region", null=True, blank=True, default=None, on_delete=models.SET_NULL, db_index=True)
    status = models.NullBooleanField(help_text="Region visible", null=True, blank=True, default=None, db_index=True)
    longitude = models.FloatField(help_text="Region longitude", null=True, blank=True, default=None)
    latitude = models.FloatField(help_text="Region longitude", null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.parent_region:
            return '/' + self.parent_region.alias + '_' + self.alias + '/'
        else:
            return '/' + self.alias + '/'


class UpdateLog(models.Model):
    term = models.DateField(help_text="Update term", db_index=True)
    last_update = models.DateField(help_text="Update date", db_index=True)
    area = models.ForeignKey(Region, help_text="Region/area", db_index=True, on_delete=models.CASCADE)


class Street(models.Model):
    name = models.CharField(max_length=1000, help_text="Street name", null=True, blank=True, default=None, db_index=True)


class Car(models.Model):
    brand = models.CharField(max_length=1000, help_text="Car brand", null=True, blank=True, default=None, db_index=True)
    car_model = models.CharField(max_length=1000, help_text="Car model", null=True, blank=True, default=None, db_index=True)
    color = models.CharField(max_length=1000, help_text="Car color", null=True, blank=True, default=None, db_index=True)
    manufacture_year = models.IntegerField(help_text="Car manufacture year", null=True, blank=True, default=None, db_index=True)

    def __str__(self):
        return self.brand + " " + self.car_model


class Offence(models.Model):
    name = models.CharField(max_length=1000, help_text="Participant offences", null=True, blank=True, default=None, db_index=True)

    def __str__(self):
        return self.name


class MVCType(models.Model):
    name = models.CharField(max_length=1000, help_text="MVC Type name", null=True, blank=True, default=None, db_index=True)
    alias = models.CharField(max_length=1000, help_text="MVC Type alias", null=True, blank=True, default=None, db_index=True)

    def __str__(self):
        return self.name


class MVCParticipantType(models.Model):
    name = models.CharField(max_length=1000, help_text="MVC Type name", null=True, blank=True, default=None, db_index=True)
    label = models.CharField(max_length=1000, help_text="MVC Type label", null=True, blank=True, default=None, db_index=True)
    value = models.BooleanField(max_length=1000, help_text="Is MVC Type Value at first", null=False, blank=False, default=True, db_index=True)

    def __str__(self):
        return self.name



class Nearby(models.Model):
    name = models.CharField(max_length=1000, help_text="Nearby object name", null=True, blank=True, default=None, db_index=True)

    def __str__(self):
        return self.name


class MVC(models.Model):
    region = models.ForeignKey(Region, help_text="MVC region", null=True, blank=True, default=None, on_delete=models.SET_NULL, db_index=True)
    alias = models.CharField(max_length=1000, help_text="MVC alias", null=True, blank=True, default=None, db_index=True)
    datetime = models.DateTimeField(default=None, help_text="MVC date", null=True, blank=True, db_index=True)
    address = models.CharField(max_length=1000, help_text="MVC address", null=True, blank=True, default=None, db_index=True)
    street = models.ForeignKey(Street, help_text="MVC Street", null=True, blank=True, default=None, on_delete=models.SET_NULL, db_index=True)
    type = models.ForeignKey(MVCType, help_text="MVC Type", null=True, blank=True, default=None, on_delete=models.SET_NULL, db_index=True)
    participant_type = models.ForeignKey(MVCParticipantType, help_text="MVC Participant Type", null=True, blank=True, default=None, on_delete=models.SET_NULL, db_index=True)
    lng = models.FloatField(help_text="MVC longitude", null=True, blank=True, default=None)
    lat = models.FloatField(help_text="MVC longitude", null=True, blank=True, default=None)
    conditions = JSONField(help_text="MVC conditions", null=True, blank=True, default=None)
    dead = models.IntegerField(help_text="MVC dead count", null=True, blank=True, default=None, db_index=True)
    injured = models.IntegerField(help_text="MVC injured count", null=True, blank=True, default=None, db_index=True)
    participants = models.IntegerField(help_text="MVC participants count", null=True, blank=True, default=None, db_index=True)
    scheme = models.CharField(max_length=100, help_text="MVC scheme number", null=True, blank=True, default=None, db_index=True)
    nearby = models.ManyToManyField(Nearby, help_text="Nearby objects", db_index=True)
    source_data = JSONField(help_text="Source data", null=True, blank=True, default=None)
    geo_updated = models.BooleanField(help_text="Geo updated", default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            Index(fields=('id', 'lng', 'lat')),
            Index(fields=('lng',)),
            Index(fields=('lat',)),
        ]

    def __str__(self):
        return self.type.name + " " + self.region.name + " " + str(self.datetime)

    def get_absolute_url(self):
        return '/dtp/' + self.alias + '/'

class Participant(models.Model):
    role = models.CharField(max_length=1000, help_text="Participant role", null=True, blank=True, default=None, db_index=True)
    offences = models.ManyToManyField(Offence, help_text="Participant offences", db_index=True)
    driving_experience = models.IntegerField(help_text="Participant driving experience (years)", null=True, blank=True)
    status = models.CharField(max_length=1000, help_text="Participant status", null=True, blank=True, default=None)
    gender = models.CharField(max_length=1000, help_text="Participant gender", null=True, blank=True, default=None)
    abscond = models.CharField(max_length=1000, help_text="Participant abscond", null=True, blank=True, default=None)
    mvc = models.ForeignKey(MVC, help_text="MVC", null=True, blank=True, default=None, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, help_text="Car", null=True, blank=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.role + " " + self.gender + self.mvc.region.name