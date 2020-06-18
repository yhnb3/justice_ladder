from django import forms
from .models import Review, Comment, Article, Iwantthis


class ReviewForm(forms.ModelForm):
    INTEGER_CHOICES= [tuple([x,x]) for x in range(1,11)]
    rate = forms.IntegerField(widget=forms.Select(choices=INTEGER_CHOICES))
    class Meta:
        model = Review
        fields = ['content', 'rate']
        labels = { 'content': '내용', 'rate': '평점' }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = { 'content': '댓글' }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']


class IwantthisForm(forms.ModelForm):
    class Meta:
        model = Iwantthis
        fields = ['comment'] 