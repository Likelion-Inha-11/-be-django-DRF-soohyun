from django import forms
from django.contrib.auth.forms import UserCreationForm
from MBTIAPP.models import Profile, Comment
from django.contrib.auth.models import User

class Signupform(UserCreationForm):
    nickname = forms.CharField(max_length=15 ,label="닉네임", required=True)

    class Meta:
        model = Profile
        fields = ("username", "password1" , "password2", "nickname")


class MbtiForm(forms.Form):
    EI = forms.ChoiceField(choices=[('E','네'),('I','아니오')], widget=forms.RadioSelect)
    NS = forms.ChoiceField(choices=[('N','네'),('S','아니오')], widget=forms.RadioSelect)
    TF = forms.ChoiceField(choices=[('F','네'),('T','아니오')], widget=forms.RadioSelect)
    PJ = forms.ChoiceField(choices=[('J','네'),('P','아니오')], widget=forms.RadioSelect)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('post','commenter')