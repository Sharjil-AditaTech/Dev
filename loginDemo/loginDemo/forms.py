from pyexpat import model
from attr import fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Row,Column,Submit
from accounts_engine.models import UserDetail,CustomUser


class RegistrationForm(UserCreationForm):
    
    email = forms.EmailField(max_length=200)

    class Meta:
        model = get_user_model()        
        fields = ("email",)

    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.helper = FormHelper()

       self.helper.form_method = 'post'
       self.helper.add_input(Submit('add_user_details', 'Add'))
        
       