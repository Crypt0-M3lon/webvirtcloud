from django.db import models
from computes.models import Compute
from groups.models import Group

class Instance(models.Model):
    compute = models.ForeignKey(Compute)
    name = models.CharField(max_length=20)
    uuid = models.CharField(max_length=36)
    group = models.ForeignKey(Group, null=True)

    def __unicode__(self):
        return self.name




