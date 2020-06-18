from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'nickname']
        labels = { 'username': '아이디', 'nickname': '별명' }


class CustomUserChangeForm(UserChangeForm):
    password = None
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'nickname', 'photo', 'intro']
        labels = { 'nickname': '별명', 'intro': '소개', 'photo': '프로필 사진' }