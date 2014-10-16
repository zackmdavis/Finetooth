from django import forms


class CommentForm(forms.Form):
    content = forms.CharField(
        label="", widget=forms.Textarea(attrs={'rows': 6})
    )

class SignupForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField()    