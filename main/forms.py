from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Question, Answer, Profile


class AddQuestionForm(ModelForm):
    QuestionId = forms.IntegerField(required=False)
    OwnerUserId = forms.IntegerField(required=False)
    Title = forms.CharField(max_length=50)
    Body = forms.CharField(widget=forms.Textarea)
    Score = forms.IntegerField(required=False)
    class Meta:
        model = Question
        fields = [
            'Title',
            'Body',
            'tags',
        ]
        exclude = ('OwnerUserId', )
        help_texts = {
            'Title': None,
            'Body': None,
        }

class AddAnswerForm(ModelForm):
    AnswerId = forms.IntegerField(required=False)
    OwnerUserId = forms.IntegerField(required=False)
    ParentId = forms.IntegerField(required=False)
    Score = forms.IntegerField(required=False)
    IsAcceptedAnswer = forms.BooleanField(required=False)
    Body = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Answer
        fields = ['Body']
        exclude = ('OwnerUserId', 'ParentId', )

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UpdateUserForm(ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # exclude = ('username', 'password1', 'password2', )

class CreateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('Bio', 'Country')

class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('Bio', 'Country')