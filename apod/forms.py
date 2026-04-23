from django import forms
from .models import Apod

class Note(forms.ModelForm):
        class Meta:
            
            model = Apod
            fields = ['note']
    
        def clean_note(self):
            note = self.cleaned_data.get('note')
            
            if note and len(note) > 500:
                raise forms.ValidationError("Note cannot exceed 500 characters.")
            
            return note