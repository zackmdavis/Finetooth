from django import forms

from core.models import FinetoothUser

class CommentForm(forms.Form):
    content = forms.CharField(
        label="", widget=forms.Textarea(attrs={'rows': 6})
    )

class SignupForm(forms.ModelForm):
    class Meta:
        model = FinetoothUser
        fields = ('username', 'email')

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Password confirmation didn't match."
            )
        return password
