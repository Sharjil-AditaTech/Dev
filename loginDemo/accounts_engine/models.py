from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import datetime
from rest_framework_simplejwt.tokens import RefreshToken




class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
        
    
    username = None
    user_kind = models.CharField(max_length=20, default='others',null=False,blank=False)
    email = models.EmailField(('email address'), unique=True)
    auth_provider = models.CharField(max_length=255, blank=False,null=False, default='email')
    is_verified = models.BooleanField(default=False)
      
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        try:
            user_detail = UserDetail.objects.get(user = self)
            return user_detail.__str__()
        except:
            return str(self.email)

    
    def kind(self):
        return str(self.kind)
    
   
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }    

    
    def get_user_detail(self):
        user_detail = UserDetail.objects.get(user = self)
        return user_detail


class Company(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name) + '-' + str(self.location)


class Role(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

    def get_permissions_of_role(self):
        role_wise_permission = RoleWisePermission.objects.get(role = self)
        return role_wise_permission.permission.all()


class Group(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

    def get_permissions_of_group(self):
        group_wise_permission = GroupWisePermission.objects.get(group = self)
        return group_wise_permission.permission.all()


class Permission(models.Model):
    SECTION_LIST = [
    ('-1', 'others'),
    ('0', 'profile'),
    ('1', 'setting'),
    ('2', 'upload'),    
    ('3', 'reports'),
    ]
    section = models.CharField(max_length = 10,choices = SECTION_LIST,default = '0')
    parent = models.ForeignKey('Permission', null=True,blank=True, on_delete=models.SET_NULL)
    url_name = models.CharField(max_length = 200)

    def __str__(self):
        return str(self.get_section_display())+ '-' + str(self.url_name).replace('_', ' ')

    def get_section(self):
        return self.section


class RoleWisePermission(models.Model):
    # TODO should change role and group in below model to OneToOneField in future to avoid conflicts
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ManyToManyField('Permission', related_name='role_permissions')

    def __str__(self):
        return str('permissions of Role: ' + self.role.name)

    def get_permissions_of_role(self, role):
        permission_list = []
        roles_wise_permission = RoleWisePermission.objects.get(role = role)
        permissions = roles_wise_permission.permission.all()
        for each in permissions:
            permission_list.append(each)
        return permission_list

    def get_urls_of_role_as_list(self, role):
        url_list = []
        permission_list = get_permissions_of_role(self, role)
        for each in permission_list:
            url_list.append(each.url_name)
        return url_list


class GroupWisePermission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permission = models.ManyToManyField('Permission', related_name='group_permissions')

    def __str__(self):
        return str('permissions of Group: ' + self.group.name)

    def get_permissions_of_group(self, group):
        permission_list = []
        groups_wise_permission = GroupWisePermission.objects.get(group = group)
        permissions = groups_wise_permission.permission.all()
        for each in permissions:
            permission_list.append(each)
        return permission_list

    def get_urls_of_group_as_list(self, group):
        url_list = []
        permission_list = get_permissions_of_group(self, group)
        for each in permission_list:
            url_list.append(each.url_name)
        return url_list

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}

class UserDetail(models.Model):
    KIND_LIST = (
        ('1', 'Premium'),
        ('2', 'Tier-1'),
        ('3', 'Tier-2'),        
        ('4', 'Other')
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    user_kind = models.CharField(max_length=1, choices=KIND_LIST)
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    mobile_number = models.CharField(max_length = 10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company')
    role = models.ManyToManyField('Role', related_name='roles')
    group = models.ManyToManyField('Group', related_name='groups')
    custom_permission = models.ManyToManyField('Permission', related_name='custom_permissions')
    

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    
    def can_access_setting_section(self):
        roles_wise_permission = RoleWisePermission.objects.filter(role__in = self.role.all())
        status = False
        for each in roles_wise_permission:
            permissions = each.permission.all()
            for each2 in permissions:
                # 1 is for setting section
                if each2.section == '1':
                    status = True
        return status

    def can_access_upload_section(self):
        roles_wise_permission = RoleWisePermission.objects.filter(role__in = self.role.all())
        status = False
        for each in roles_wise_permission:
            permissions = each.permission.all()
            for each2 in permissions:
                # 2 is for upload section
                if each2.section == '2':
                    status = True
        return status

    def can_access_report_section(self):
        roles_wise_permission = RoleWisePermission.objects.filter(role__in = self.role.all())
        status = False
        for each in roles_wise_permission:
            permissions = each.permission.all()
            for each2 in permissions:
                # 3 is for report section
                if each2.section == '3':
                    status = True
        return status

    

    def get_all_roles(self):
        return self.role.all()

    def get_all_groups(self):
        return self.group.all()

    def get_all_custom_permissions(self):
        return self.custom_permission.all()


class Task(models.Model):
    task = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    task_for_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='task_for_users')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    STATUS_LIST = [
    ('0', 'Pending'),
    ('1', 'In Progress'),
    ('2', 'Completed'),
    ('3', 'Not Applicable'),
    ]
    status = models.CharField(max_length = 10, choices = STATUS_LIST, default = '0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.task)

    def get_status_colour(self):
        if self.status == '0':
            return 'warning'
        if self.status == '1':
            return 'info'
        if self.status == '2':
            return 'success'
        if self.status == '3':
            return 'secondary'

    def is_due(self):
        today = datetime.datetime.today()
        if today > self.end_date:
            return True
        else:
            return False

               