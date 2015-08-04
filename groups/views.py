import time
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from groups.models import Group, Group_instance
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
        pass

    instances = Instance.objects.all()
    print instances
    #instances = instances - Instance.objects.all()

    group = get_object_or_404(Group, pk=group_id)
    group_instances= []
    try:
        group_instances = Group_instance.objects.get(group=group_id)
    except:
        pass


    return render(request, 'group.html', locals())