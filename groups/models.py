from django.db import models
from instances.models import Instance

class Group(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Group_instance(models.Model):
    group = models.ForeignKey(Group)
    instance = models.ForeignKey(Instance)
