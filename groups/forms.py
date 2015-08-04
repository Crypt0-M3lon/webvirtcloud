import re
from django import forms
from django.utils.translation import ugettext_lazy as _
from groups.models import Group


class groupAddForm(forms.Form):
    name = forms.CharField(error_messages={'required': _('No group name has been entered')}, max_length=20)

    def clean_name(self):
        name = self.cleaned_data['name']
        have_symbol = re.match('[^a-zA-Z0-9._-]+', name)
        if have_symbol:
            raise forms.ValidationError(_('The group name must not contain any special characters'))
        elif len(name) > 20:
            raise forms.ValidationError(_('The group name must not exceed 20 characters'))
        try:
            Group.objects.get(name=name)
        except Group.DoesNotExist:
            return name
        raise forms.ValidationError(_('This group already exist'))

class groupInstanceAddForm(forms.Form):
    instance_id = forms.Integer
