from django import forms
from django.contrib.auth.models import User
from .models import Article, Comment, UserProfile
from django.contrib.auth.forms import UserCreationForm

class ArticleForm(forms.ModelForm):
    """Form for the image model"""
    article_content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Article
        fields = ("headline", "article_content","article_photos","yt_links","article_image_upload","tag")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment_content",)

class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True,label="Updated email address if different",
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ("email",)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("about_user","user_photo",)



from django.contrib.auth import get_user_model


# Sign Up Form
class RegisterForm(UserCreationForm):
    #first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    #last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    #email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        User = get_user_model()
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            ]
