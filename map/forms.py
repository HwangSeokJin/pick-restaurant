from django import forms


class KeywordForm(forms.Form):
    keyword = forms.CharField(label='νμ¬ μμΉ', max_length=100)

