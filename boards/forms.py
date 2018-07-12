from django import forms
from .models import Topic, Post, Board


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'What is in your mind?', 'id': 'topic-message'}),
        max_length=4000,
        help_text='The max length of the text is 4000')
    subject = forms.CharField(widget=forms.Textarea(attrs={'id': 'topic-subject'}))

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={
                'id': 'post-text',
                'required': True,
                'placeholder': 'Say something...'
            }), }


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description', ]
