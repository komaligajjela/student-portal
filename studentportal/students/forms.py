from django import forms
from .models import Student

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

        widgets = {

    'name': forms.TextInput(attrs={
        'class': 'form-control'
    }),

    'email': forms.EmailInput(attrs={
        'class': 'form-control'
    }),

    'course': forms.TextInput(attrs={
        'class': 'form-control'
    }),

    'age': forms.NumberInput(attrs={
        'class': 'form-control'
    }),

    'joined_date': forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }),

    'profile_image': forms.FileInput(attrs={
        'class': 'form-control'
    }),

}

    def clean_age(self):
        age = self.cleaned_data.get('age')

        if age <= 0:
            raise forms.ValidationError("Age must be positive")

        return age