from django import forms
from .models import Apod
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Note(forms.ModelForm):
        class Meta:
            
            model = Apod
            fields = ['note']
    
        def clean_note(self):
            note = self.cleaned_data.get('note')
            
            if note and len(note) > 500:
                raise forms.ValidationError("Note cannot exceed 500 characters.")
            
            return note

class SignUpForm(UserCreationForm) :
     
     class Meta :
         
         model = User
         fields = ['username','password1','password2']

