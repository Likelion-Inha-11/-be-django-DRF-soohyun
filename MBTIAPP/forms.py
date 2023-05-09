from django import forms
from django.contrib.auth.forms import UserCreationForm
from MBTIAPP.models import Profile, Comment
from django.contrib.auth.models import User

class Signupform(UserCreationForm):
    nickname = forms.CharField(max_length=15 ,label="닉네임", required=True)

    class Meta:
        model = Profile
        fields = ("username", "password1" , "password2", "nickname")

    def save(self):
        user = super(Signupform, self).save(commit=False)
        user.save()

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password1 = cleaned_data.get("password1")
    #     password2 = cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         self.add_error('password2', '비밀번호가 일치하지 않습니다.')




class MbtiForm(forms.Form):
    EI = forms.ChoiceField(choices=[('E','네'),('I','아니오')], widget=forms.RadioSelect)
    NS = forms.ChoiceField(choices=[('N','네'),('S','아니오')], widget=forms.RadioSelect)
    TF = forms.ChoiceField(choices=[('F','네'),('T','아니오')], widget=forms.RadioSelect)
    PJ = forms.ChoiceField(choices=[('J','네'),('P','아니오')], widget=forms.RadioSelect)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('post','commenter')