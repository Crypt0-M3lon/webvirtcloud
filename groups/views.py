import time
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from groups.models import Group
from instances.models import Instance
from accounts.models import UserInstance
from libvirt import libvirtError
from groups.forms import groupAddForm, groupInstanceAddForm
from vrtManager.instance import wvmInstance, wvmInstances

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

    groups = Group.objects.all().order_by('name')
    groups_inst = []
    for group in groups:
        groups_inst.append((group, Instance.objects.filter(group=group).order_by('name')))
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
    available_instances = Instance.objects.filter(group=None).order_by('name')
    group_instances = []
    try:
        group_instances = Instance.objects.filter(group=group).order_by('name')
    except:
        pass
    group_instances_status = []
    # get status for each instances of the group
    for instance in group_instances:
        conn = wvmInstance(instance.compute.hostname,
                           instance.compute.login,
                           instance.compute.password,
                           instance.compute.type,
                           instance.name)

        status = conn.get_status()
        group_instances_status.append((instance,status))

    return render(request, 'group.html', locals())

def deleteFromGroup(request, group_id, instance_id):
    """
    :param request:
    :return:
    """
    if not request.user.is_authenticated():
       return HttpResponseRedirect(reverse('index'))
    if not request.user.is_superuser:
       return HttpResponseRedirect(reverse('index'))
    error_messages = []
    instance = get_object_or_404(Instance, pk=instance_id)
    instance.group = None
    instance.save()
    return redirect('group', group_id=group_id)


def powerGroupInstance(request, group_id):

    if not request.user.is_authenticated():
       return HttpResponseRedirect(reverse('index'))
    if not request.user.is_superuser:
       return HttpResponseRedirect(reverse('index'))

    group = get_object_or_404(Group, pk=group_id)

    msg = ("Power On Group")
    try:
        group_instances = Instance.objects.filter(group=group).order_by('name')
    except:
        pass
    group_instances_status = []
    # get status for each instances of the group
    for instance in group_instances:
        conn = wvmInstance(instance.compute.hostname,
                           instance.compute.login,
                           instance.compute.password,
                           instance.compute.type,
                           instance.name)
        if conn.get_status() != 1:
            conn.start()
    return redirect('group', group_id=group_id)