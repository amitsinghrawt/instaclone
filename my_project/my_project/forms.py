from django import forms

from models import UserModel, PostModel, LikeModel, CommentModel


class SignUpFrom(forms.ModelForm):
    class Meta:
        model =UserModel
        fields=['email', 'username', 'name', 'password']

class LoginFrom(forms.ModelForm):
    class Meta:
        model =UserModel
        fields=['username','password']

class PostFrom(forms.ModelForm):
    class Meta:
        model=PostModel
        fields=['image','caption']

class LikeFrom(forms.ModelForm):
    class Meta:
        model=LikeModel
        fields=['post']


class CommentFrom(forms.ModelForm):
    class Meta:
        model=CommentModel
        fields=['comment_text','post']