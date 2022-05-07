from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView,DetailView, UpdateView
from django.contrib.auth.views import LoginView

from . import forms
from . import models


# Create your views here.

class Homepage(TemplateView):
    template_name = "index.html" 


# class Profile():
def profile(request):
    if request.user.student_id is None:
        return HttpResponse("Please Insert")
    
    return redirect( reverse_lazy("index") )

class UserProfileEdit(UpdateView):
    model = models.User
    fields = ['first_name', 'last_name', 'email', 'profile', 'phone', 'about' ]
    template_name='account/edit_profile.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs['pk']:
            return HttpResponse('You are not authorized to see this page', status=403)
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        if request.user.id != kwargs['pk']:
            return HttpResponse('You are not authorized to see this page', status=403)
        return super().post(request, *args, **kwargs)
    def form_valid(self, form) :

        try:
            
            
            user_me = models.User.objects.get(id=self.request.user.id)
            
            print( user_me )
            
            socials = user_me.socials
            
            soc = forms.SocialAccountLinksForm( form.data )
            
            if  soc.is_valid() :
                soc = soc.cleaned_data
                socials.website =  soc.get("website") if soc.get("website") else socials.website
                socials.github = soc.get("github") if soc.get("github") else socials.github
                socials.twitter = soc.get("twitter") if  soc.get("twitter") else socials.twitter
                socials.linkedin = soc.get("linkedin") if soc.get("linkedin") else socials.linkedin
            # socials.save()
            
            user_me.socials = socials
            user_me.socials.save() 
            user_me.first_name = "Changed"
            user_me.save()
            
        except Exception as e :
            import traceback; traceback.print_exc();    
            print("Error in self.cleaned_data")
            pass
        
        # self.object = form.save()
        return super().form_valid(form)
    
class UserProfile(DetailView):
    model = models.User
    template_name='account/profile.html'

class Events(TemplateView):
    template_name = "events.html"
    
class Login(TemplateView):
    template_name = "login.html"
    
class Register(CreateView):
    form_class = forms.RegisterForm
    # fields =  ['first_name', 'last_name', 'email', 'username', 'student_id', 'password1','password2']
    success_url = reverse_lazy("index")
    http_method_names = ['get', 'post']
    success_message = "%(username)s was created successfully"
    template_name = "register.html"
    
