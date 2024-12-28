from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm = forms.CharField(widget=forms.CheckboxInput)

    def clean_username(self):
        return self.cleaned_data['username'].lower().strip()


class SignUpForm(forms.Form):
    name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_name(self):
        return self.cleaned_data['name'].lower().strip()

    def clean_username(self):
        return self.cleaned_data['username'].lower().strip()


# Profile Edit
class ProfileEditForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        data = super().clean()
        if data['password'] != data['password_confirmation']:
            raise ValidationError('Passwords do not match')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class AskForm(forms.ModelForm):
    tags = forms.CharField()

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

        widgets = {
            'title': forms.TextInput(),
            'text': forms.Textarea(attrs={'placeholder': "Detailed description"}),
            'tags': forms.TextInput(attrs={'placeholder': "Tags"})
        }

        labels = {
            'title': "Question header",
            'text': "Add a description to your question and write it in details.",
            'tags': "Add some tags!",
        }

    def clean_tags(self):
        data = self.data['tags']
        if len(data) > 30:
            raise ValidationError("Tags field length must be less than 30 characters")
        return data

    def clean_title(self):
        data = self.data['title']
        if len(data) > 100:
            raise ValidationError("Title length must be less than 100 characters")
        return data

    def clean_text(self):
        data = self.data['text']
        if len(data) > 5000:
            raise ValidationError("Question body must be less than 5000 characters")
        return data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Answer...', 'rows': '3'})
        }
        labels = {
            'text': 'Answer a question!'
        }

    def clean_text(self):
        data = self.data['text']
        if len(data) > 3000:
            raise ValidationError("Answer body must be less than 3000 characters")
        return data
