from accounts_engine.models import *

def get_all_permitted_sections_and_urls(request):
    default_url_list = ['my_profile', 'tasks', 'view_task', 'update_status_task' ]
    url_list = []
    group_list = []
    custom_permission_list = []
    section_list = ['profile']
    try:
        roles = request.user.get_user_detail().role.all()
        roles_wise_permission = RoleWisePermission.objects.filter(role__in = roles)
        for each in roles_wise_permission:
            permissions = each.permission.all()
            for each2 in permissions:
                section_list.append(each2.get_section_display())
                url_list.append(each2.url_name)
    except:
        print('issue in collecting role level permisions in context processor')

    try:
        groups = request.user.get_user_detail().group.all()
        groups_wise_permission = GroupWisePermission.objects.filter(group__in = groups)
        for each in groups_wise_permission:
            permissions = each.permission.all()
            for each2 in permissions:
                section_list.append(each2.get_section_display())
                group_list.append(each2.url_name)
    except:
        print('issue in collecting group level permisions in context processor')


    try:
        custom_permissions = request.user.get_user_detail().custom_permission.all()
        for each in custom_permissions:
            section_list.append(each.get_section_display())
            custom_permission_list.append(each.url_name)
    except:
        print('issue in collecting custom permisions in context processor')

    permitted_url_list = list(set(default_url_list + url_list + group_list + custom_permission_list))
    permitted_section_list = list(set(section_list))

    return_dict = {}
    return_dict['permitted_url_list'] = permitted_url_list
    return_dict['permitted_section_list'] = permitted_section_list
    return return_dict


def get_active_section(request):
    try:
        permission = Permission.objects.get(url_name = request.resolver_match.url_name)
        return permission.get_section_display
    except:
        print('issue in getting active section')
        return False


def general_details(request):
    try:
        permitted_sections_and_urls = get_all_permitted_sections_and_urls(request)
        active_section = get_active_section(request)
        user_tasks = Task.objects.filter(task_for_user = request.user, status__in = [0,1])

        return {'active_section': active_section, 'permitted_section_list': permitted_sections_and_urls['permitted_section_list'], 'permitted_url_list': permitted_sections_and_urls['permitted_url_list'], 'user_tasks': user_tasks}
    except:
        print('issue in custom context processor')
        return {}
