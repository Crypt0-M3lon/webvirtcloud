import time
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from groups.models import Group
from instances.models import Instance
from accounts.models import UserInstance
from libvirt import libvirtError
from groups.forms import groupAddForm


def groups(request):
    """
    :param request:
    :return:
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))

    error_messages = []
    groups = Group.objects.all()
    if request.method == 'POST':
         form = groupAddForm(request.POST)
         if form.is_valid():
             group = form.cleaned_data
             new_group = Group(name=group['name'])
             new_group.save()
             return HttpResponseRedirect(request.get_full_path())
         else:
             for msg_err in form.errors.values():
                    error_messages.append(msg_err.as_text())
    return render(request, 'groups.html', locals())