from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import modelformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Button
from crispy_forms.bootstrap import InlineRadios
from django.forms import ModelForm, Textarea, TextInput
from accounts_engine.models import *
from django.urls import reverse

class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    class Meta:
        model = get_user_model()
        fields = ['email']


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ('name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['name'].label = "Role"
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('role')
        self.helper.add_input(Submit('add_new_role', 'Add'))
        self.helper.layout = Layout(
            Row(
                Column('name'),
            )
        )


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['name'].label = "Group"

        self.helper.form_method = 'post'
        self.helper.form_action = reverse('group')
        self.helper.add_input(Submit('add_new_group', 'Add'))
        # self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn btn-danger'))
        self.helper.layout = Layout(
            Row(
                Column('name'),
            )
        )


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ('section', 'url_name',)

        widgets = {
            'section' : forms.Select(attrs={'class': 'selectpicker', 'data-style': 'btn btn-primary', 'title': 'select Section'}),
            'url_name' : forms.TextInput(attrs={'class': 'mt-3'}),
            # 'mobile_number' : forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['section'].label = "Section"
        self.fields['url_name'].label = "Url Name"

        self.helper.form_method = 'post'
        self.helper.form_action = reverse('permission')
        self.helper.add_input(Submit('add_new_permission', 'Add'))
        # self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn btn-danger'))
        self.helper.layout = Layout(
            Row(
                Column('section'),
            ),
            Row(),
            Row(
                Column('url_name'),
            )
        )


class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ('first_name', 'last_name', 'mobile_number', 'company', 'role', 'group', 'custom_permission', 'user','user_kind')

        widgets = {
            'user' : forms.TextInput(attrs={'type': 'hidden'}),
            'company' : forms.TextInput(attrs={'type': 'hidden'}),
            'user_kind' : forms.Select(attrs={'class': 'selectpicker', 'data-style': 'select-with-transition', 'data-style': 'btn btn-primary', 'title': 'select User Kind'}),
            'role' : forms.SelectMultiple(attrs={'class': 'selectpicker multiple', 'data-style': 'select-with-transition', 'multiple': '',  'data-style': 'btn btn-primary', 'title': 'select role'}),
            'group' : forms.SelectMultiple(attrs={'class': 'selectpicker multiple', 'data-style': 'select-with-transition', 'multiple': '',  'data-style': 'btn btn-primary', 'title': 'select group'}),
            'custom_permission' : forms.SelectMultiple(attrs={'class': 'selectpicker multiple', 'data-style': 'select-with-transition', 'multiple': '',  'data-style': 'btn btn-primary', 'title': 'select custome pemission'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'
        self.helper.add_input(Submit('add_user_details', 'Add'))
        # self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn btn-danger'))
        self.helper.layout = Layout(
            Row(
                Column('first_name'),
                Column('last_name'),
                Column('mobile_number'),
            ),
            Row(
                Column('user_kind'),                
                Column('role'),
            ),
            Row(
                Column('group'),
                Column('custom_permission'),
            ),            
            Row(
                Column('user'),
                Column('company'),                
            )
        )


class RoleWisePermissionForm(forms.ModelForm):
    class Meta:
        model = RoleWisePermission
        fields = ('role', 'permission')

        widgets = {
            'role' : forms.TextInput(attrs={'type': 'hidden'}),
            'permission' : forms.SelectMultiple(attrs={'class': 'selectpicker multiple', 'data-style': 'select-with-transition', 'multiple': '',  'data-style': 'btn btn-primary', 'title': 'select permissions'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'
        self.helper.add_input(Submit('add_permission', 'Add'))
        # self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn btn-danger'))
        self.helper.layout = Layout(
            Row(
                Column('permission'),
            ),
            Row(
                Column('role'),
            )
        )


class GroupWisePermissionForm(forms.ModelForm):
    class Meta:
        model = GroupWisePermission
        fields = ('group', 'permission')

        widgets = {
            'group' : forms.TextInput(attrs={'type': 'hidden'}),
            'permission' : forms.SelectMultiple(attrs={'class': 'selectpicker multiple', 'data-style': 'select-with-transition', 'multiple': '',  'data-style': 'btn btn-primary', 'title': 'select permissions'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'
        self.helper.add_input(Submit('add_permission', 'Add'))
        # self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn btn-danger'))
        self.helper.layout = Layout(
            Row(
                Column('permission'),
            ),
            Row(
                Column('group'),
            )
        )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('task', 'description', 'task_for_user', 'end_date', 'created_by')

        widgets = {
            'created_by' : forms.TextInput(attrs={'type': 'hidden'}),
            'task_for_user' : forms.Select(attrs={'class': 'selectpicker', 'data-style': 'select-with-transition', 'data-style': 'btn btn-primary', 'title': 'select User'}),
            'end_date' : forms.DateInput(attrs={'type': 'date', 'class': 'mt-5'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'
        self.helper.add_input(Submit('add_Task', 'Add'))
        # self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn btn-danger'))
        self.helper.layout = Layout(
            Row(
                Column('task'),
            ),
            Row(
                Column('description'),
            ),
            Row(
                Column('task_for_user'),
                Column('end_date'),
            )
            ,
            Row(
                Column('created_by'),
            )
        )


class TaskStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('status',)

        widgets = {
            'status' : forms.Select(attrs={'class': 'selectpicker', 'data-style': 'select-with-transition', 'data-style': 'btn btn-primary', 'title': 'select User'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['status'].label = "Update Status of task Below"

        self.helper.form_method = 'post'
        self.helper.add_input(Submit('update_status', 'Update Status'))
        # self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn btn-danger'))
        self.helper.layout = Layout(
            Row(
                Column('status'),
            ),
        )
