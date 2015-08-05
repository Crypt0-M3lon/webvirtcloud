import time
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from groups.models import Group
from instances.models import Instance
from accounts.models import UserInstance
from libvirt import libvirtError
from groups.forms import groupAddForm, groupInstanceAddForm


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

    groups = Group.objects.all()
    groups_inst = []
    for group in groups:
        groups_inst.append((group, Instance.objects.filter(group=group)))
    return render(request, 'groups.html', locals())

def editGroup(request, group_id):
    """
    :param request:
    :return:
    """
    if not request.user.is_authenticated():
       return HttpResponseRedirect(reverse('index'))
    if not request.user.is_superuser:
       return HttpResponseRedirect(reverse('index'))
    error_messages = []

    if request.method == 'POST':
        form = groupInstanceAddForm(request.POST)
        if form.is_valid():
             groupInstance = form.cleaned_data
             group = get_object_or_404(Group, pk=group_id)
             instance = get_object_or_404(Instance, pk=groupInstance['instance_id'])
             instance.group = group
             instance.save()
             return HttpResponseRedirect(request.get_full_path())
        else:
             for msg_err in form.errors.values():
                    error_messages.append(msg_err.as_text())

    group = get_object_or_404(Group, pk=group_id)
    available_instances = Instance.objects.exclude(group=group)
    group_instances= []
    try:
        group_instances = Instance.objects.filter(group=group)
    except:
        pass


    return render(request, 'group.html', locals())