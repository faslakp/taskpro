from django import forms

from notes.models import Task



class TaskForm(forms.ModelForm):

    class Meta:

        model=Task
        
        # fields="__all__"
        # fields=['titile','description',...]
        exclude=("created_date","status","updated_date","user")

        # for styling ModelForm
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "due_date":forms.DateInput(attrs={"class":"form-control","type":"date"}),
            "category":forms.Select(attrs={"class":"form-control form-select"}),
            
            # "user":forms.TextInput(attrs={"class":"form-control"})
        }



from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):

    class Meta:

        model=User

        fields=["username","email","password"]


        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"})
        }


class SignInForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))




        