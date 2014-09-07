from django import forms


class CommentForm(forms.Form):
    content = forms.CharField(
        label="", widget=forms.Textarea(attrs={'rows': 6})
    )


class TagForm(forms.Form):
    label = forms.CharField(max_length=64, label="new tag")
