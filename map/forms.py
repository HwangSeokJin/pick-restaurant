from django import forms


class KeywordForm(forms.Form):
    keyword = forms.CharField(label='현재 위치', max_length=100)

