from django.shortcuts import render, redirect
from accounts_engine.forms import UserAdminCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts_engine.forms import *
from accounts_engine.models import *
from accounts_engine.decorators import is_user_allowed


@is_user_allowed
@login_required(login_url='/account/login')
def users(request):
    company = request.user.get_user_detail().company
    user_list = UserDetail.objects.filter(company = company)
    return render(request, 'accounts_engine/users.html', {
        'user_list': user_list,
    })

@is_user_allowed
@login_required(login_url='/account/login/')
def add_new_user(request):
    form = UserAdminCreationForm()
    if request.method == 'POST':

        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, 'New User created.')
            return redirect('add_user_details', new_user.id)
    return render(request, 'registration/add_new_user.html', {'form': form})


@is_user_allowed
@login_required(login_url='/account/login/')
def add_user_details(request, registered_user_id):
    registered_user = CustomUser.objects.get(id = registered_user_id)
    add_user_detail_form = UserDetailForm(initial = {'user': registered_user, 'company': request.user.get_user_detail().company})

    if request.method == 'POST':
        add_user_detail_form = UserDetailForm(request.POST)
        if add_user_detail_form.is_valid():
            add_user_detail = add_user_detail_form.save(commit=False)
            add_user_detail.save()
            add_user_detail_form.save_m2m()
            messages.success(request, 'User details added.')
            return redirect('users')

    return render(request, 'accounts_engine/add_user_details.html', {
        'registered_user': registered_user,
        'add_user_detail_form': add_user_detail_form,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def edit_user_details(request, user_id):
    registered_user = CustomUser.objects.get(id = user_id)
    user_detail = UserDetail.objects.get(user = registered_user)
    add_user_detail_form = UserDetailForm(instance = user_detail)
    if request.method == 'POST':
        add_user_detail_form = UserDetailForm(request.POST, instance = user_detail)
        if add_user_detail_form.is_valid():
            add_user_detail = add_user_detail_form.save(commit=False)
            add_user_detail.save()
            add_user_detail_form.save_m2m()
            messages.warning(request, 'User details updated.')
            return redirect('users')

    return render(request, 'accounts_engine/add_user_details.html', {
        'registered_user': registered_user,
        'add_user_detail_form': add_user_detail_form,
    })


@login_required(login_url='/account/login/')
def dashboard(request):
    return render(request, 'accounts_engine/dashboard.html')


@is_user_allowed
@login_required(login_url='/account/login/')
def role(request):
    action_type = 'add'
    role_form = RoleForm()
    role_list = Role.objects.all().order_by('name')

    if request.method == 'POST':
        role_form = RoleForm(request.POST)
        if role_form.is_valid():
            role_form.save()
            messages.success(request, 'New role created.')
            return redirect('role')

    return render(request, 'accounts_engine/role.html', {
        'role_form': role_form,
        'role_list': role_list,
        'action_type': action_type
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def role_edit(request, role_id):
    role = Role.objects.get(id = role_id)
    edit_role_form = RoleForm(instance = role)

    if request.method == 'POST':
        edit_role_form = RoleForm(request.POST, instance=role)
        if edit_role_form.is_valid():
            edit_role_form.save()
            messages.warning(request, 'Role updated.')
            return redirect('role')

    return render(request, 'accounts_engine/role_edit.html', {
        'edit_role_form': edit_role_form,
        'role_id': role_id,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def role_delete(request, role_id):
    role = Role.objects.get(id = role_id)
    role_name = role.name
    role.delete()
    messages.error(request, 'Role: ' + role_name + ' was deleted.')
    return redirect('role')


@is_user_allowed
@login_required(login_url='/account/login/')
def group(request):
    group_form = GroupForm()
    group_list = Group.objects.all().order_by('name')

    if request.method == 'POST':
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            group_form.save()
            messages.success(request, 'New group created.')
            return redirect('group')

    return render(request, 'accounts_engine/group.html', {
        'group_form': group_form,
        'group_list': group_list,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def group_edit(request, group_id):
    group = Group.objects.get(id = group_id)
    edit_group_form = GroupForm(instance = group)

    if request.method == 'POST':
        edit_group_form = GroupForm(request.POST, instance=group)
        if edit_group_form.is_valid():
            edit_group_form.save()
            messages.warning(request, 'Group updated.')
            return redirect('group')
    return render(request, 'accounts_engine/group_edit.html', {
        'edit_group_form': edit_group_form,
        'group_id': group_id,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def group_delete(request, group_id):
    group = Group.objects.get(id = group_id)
    group_name = group.name
    group.delete()
    messages.error(request, 'Group: ' + group_name + ' was deleted.')
    return redirect('group')


@is_user_allowed
@login_required(login_url='/account/login/')
def permission(request):
    permission_form = PermissionForm()
    permission_list = Permission.objects.all()

    if request.method == 'POST':
        permission_form = PermissionForm(request.POST)
        if permission_form.is_valid():
            permission_form.save()
            messages.success(request, 'New permission created.')
            return redirect('permission')

    return render(request, 'accounts_engine/permission.html', {
        'permission_form': permission_form,
        'permission_list': permission_list,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def permission_edit(request, permission_id):
    permission = Permission.objects.get(id = permission_id)
    edit_permission_form = PermissionForm(instance = permission)

    if request.method == 'POST':
        edit_permission_form = PermissionForm(request.POST, instance=permission)
        if edit_permission_form.is_valid():
            edit_permission_form.save()
            messages.warning(request, 'Permission updated.')
            return redirect('permission')

    return render(request, 'accounts_engine/permission_edit.html', {
        'edit_permission_form': edit_permission_form,
        'permission_id': permission_id,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def permission_delete(request, permission_id):
    permission = Permission.objects.get(id = permission_id)
    permission_name = permission.url_name
    permission.delete()
    messages.error(request, 'Permission: ' + permission_name + ' was deleted.')
    return redirect('permission')


@is_user_allowed
@login_required(login_url='/account/login/')
def role_wise_permission(request, role_id):
    role = Role.objects.get(id = role_id)
    try:
        role_wise_permissions = RoleWisePermission.objects.get(role = role).permission.all()
    except:
        role_wise_permissions = None

    if not role_wise_permissions or role_wise_permissions.count() == 0:
        messages.error(request, 'There are no permissions currently linked to this role. Please contact Admin')

    return render(request, 'accounts_engine/role_wise_permission.html', {
        'role_wise_permissions': role_wise_permissions,
        'role': role,
    })



@is_user_allowed
@login_required(login_url='/account/login/')
def add_permission_to_role(request, role_id):
    role = Role.objects.get(id = role_id)
    try:
        role_wise_permissions = RoleWisePermission.objects.get(role = role).permission.all()
        add_permission_to_role_form = RoleWisePermissionForm(instance = RoleWisePermission.objects.get(role = role))
    except:
        role_wise_permissions = None
        add_permission_to_role_form = RoleWisePermissionForm(initial = {'role': role})

    if request.method == 'POST':
        if role_wise_permissions is None:
            add_permission_to_role_form = RoleWisePermissionForm(request.POST)
        else:
            add_permission_to_role_form = RoleWisePermissionForm(request.POST, instance = RoleWisePermission.objects.get(role = role))
        if add_permission_to_role_form.is_valid():
            permission_to_role = add_permission_to_role_form.save(commit=False)
            permission_to_role.save()
            add_permission_to_role_form.save_m2m()
            messages.success(request, 'Permissions updated')
            return redirect('role_wise_permission', role_id)

    return render(request, 'accounts_engine/role_wise_permission.html', {
        'role_wise_permissions': role_wise_permissions,
        'add_permission_to_role_form': add_permission_to_role_form,
        'role': role,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def group_wise_permission(request, group_id):
    group = Group.objects.get(id = group_id)
    try:
        group_wise_permissions = GroupWisePermission.objects.get(group = group).permission.all()
    except:
        group_wise_permissions = None

    if not group_wise_permissions or group_wise_permissions.count() == 0:
        messages.error(request, 'There are no permissions currently linked to this Group. Please contact Admin')

    return render(request, 'accounts_engine/group_wise_permission.html', {
        'group_wise_permissions': group_wise_permissions,
        'group': group,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def add_permission_to_group(request, group_id):
    group = Group.objects.get(id = group_id)
    try:
        group_wise_permissions = GroupWisePermission.objects.get(group = group).permission.all()
        add_permission_to_group_form = GroupWisePermissionForm(instance = GroupWisePermission.objects.get(group = group))
    except:
        group_wise_permissions = None
        add_permission_to_group_form = GroupWisePermissionForm(initial = {'group': group})

    if request.method == 'POST':
        if group_wise_permissions is None:
            add_permission_to_group_form = GroupWisePermissionForm(request.POST)
        else:
            add_permission_to_group_form = GroupWisePermissionForm(request.POST, instance = GroupWisePermission.objects.get(group = group))
        if add_permission_to_group_form.is_valid():
            permission_to_group = add_permission_to_group_form.save(commit=False)
            permission_to_group.save()
            add_permission_to_group_form.save_m2m()
            messages.success(request, 'Permissions updated')
            return redirect('group_wise_permission', group_id)

    return render(request, 'accounts_engine/group_wise_permission.html', {
        'group_wise_permissions': group_wise_permissions,
        'add_permission_to_group_form': add_permission_to_group_form,
        'group': group,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def remove_permission_from_role(request, role_id, permission_id):
    role = Role.objects.get(id = role_id)
    permission_to_be_removed = Permission.objects.get(id = permission_id)
    role_wise_permissions = RoleWisePermission.objects.get(role = role)
    role_wise_permissions.permission.remove(permission_to_be_removed)
    message_str = 'permission- ' + permission_to_be_removed.__str__() + ' removed from role- ' + role.__str__()
    messages.error(request, message_str)
    return redirect('role_wise_permission', role_id)


@is_user_allowed
@login_required(login_url='/account/login/')
def remove_permission_from_group(request, group_id, permission_id):
    group = Group.objects.get(id = group_id)
    permission_to_be_removed = Permission.objects.get(id = permission_id)
    group_wise_permissions = GroupWisePermission.objects.get(group = group)
    group_wise_permissions.permission.remove(permission_to_be_removed)
    message_str = 'permission- ' + permission_to_be_removed.__str__() + ' removed from group- ' + Group.__str__()
    messages.error(request, message_str)
    return redirect('group_wise_permissions', group_id)


@is_user_allowed
@login_required(login_url='/account/login/')
def my_profile(request):
    return render(request, 'accounts_engine/my_profile.html')


@is_user_allowed
@login_required(login_url='/account/login/')
def view_profile(request, user_id):
    user_profile = CustomUser.objects.get(id = user_id)
    return render(request, 'accounts_engine/my_profile.html', {
        'user_profile': user_profile,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def tasks(request):
    task_list = Task.objects.filter(created_by = request.user) | Task.objects.filter(task_for_user = request.user)
    task_list = task_list.order_by('end_date')
    return render(request, 'accounts_engine/tasks.html', {
        'task_list': task_list,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def view_task(request, task_id):
    task = Task.objects.get(id = task_id)
    return render(request, 'accounts_engine/view_task.html', {
        'task': task,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def add_task(request):
    task_form = TaskForm(initial = {'created_by': request.user})

    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task_form.save()
            messages.success(request, 'Task created successfully')
            return redirect('tasks')
    return render(request, 'accounts_engine/add_task.html', {
        'task_form': task_form,
    })


@is_user_allowed
@login_required(login_url='/account/login/')
def edit_task(request, task_id):
    task = Task.objects.get(id = task_id)
    # redirect if task is not created by or created for user
    if not task.created_by == request.user:
        return HttpResponse('the task you are trying to edit was not created for you/ by you. This action is not allowed')

    task_form = TaskForm(instance = task)
    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance = task)
        if task_form.is_valid():
            task_form.save()
            messages.warning(request, 'Task updated.')
            return redirect('tasks')
    return render(request, 'accounts_engine/add_task.html', {
        'task': task,
        'task_form': task_form,
    })



@is_user_allowed
@login_required(login_url='/account/login/')
def delete_task(request, task_id):
    task = Task.objects.get(id = task_id)
    task_task = task.task
    # redirect if task is not creted by or created for user
    if not task.created_by == request.user:
        return HttpResponse('the task you are trying to edit was not created for you/ by you. This action is not allowed')
    task.delete()
    messages.error(request, 'Task: ' + task_task + ' was deleted.')
    return redirect('tasks')



@is_user_allowed
@login_required(login_url='/account/login/')
def update_status_task(request, task_id):
    # redirect if task is not creted by or created for user
    task = Task.objects.get(id = task_id)
    # redirect if task is not created by or created for user
    if not task.task_for_user == request.user:
        return HttpResponse('the task you are trying to edit was not created for you. This action is not allowed')

    task_status_update_form = TaskStatusUpdateForm(instance = task)

    if request.method == 'POST':
        task_status_update_form = TaskStatusUpdateForm(request.POST, instance = task)
        if task_status_update_form.is_valid():
            task_status_update_form.save()
            messages.warning(request, 'Task Status updated.')
            return redirect('tasks')

    return render(request, 'accounts_engine/view_task.html', {
        'task': task,
        'task_status_update_form': task_status_update_form,
    })
