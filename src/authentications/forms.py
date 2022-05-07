from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, SocialAccountsLinks

# All Auth imports 

from allauth.account.forms import SignupForm


def check_student_id(student_id):
    if User.objects.filter(student_id__iexact=student_id).exists():
        return True
    return False


class CustomSingupForm(SignupForm):
    first_name = forms.CharField( max_length=150 )
    last_name = forms.CharField( max_length= 150 ) 
    student_id = forms.CharField( max_length=20 )
    
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        student_id = self.cleaned_data['student_id']
        
        # if check_student_id(student_id):
        #     try:
        #         raise forms.ValidationError()
        #     except forms.ValidationError as e:
        #         self.add_error("Student Id already exist", e)
        
        user.student_id = student_id 
        user.save()
        return user


class RegisterForm(forms.ModelForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('student_id',)

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if User.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("Student Id already exists")
        return student_id


class SocialAccountLinksForm(forms.ModelForm):
    class Meta:
        model = SocialAccountsLinks
        fields = "__all__"
    
    
