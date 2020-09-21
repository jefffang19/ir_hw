from django import forms

class WordForm(forms.Form):
    keywords = forms.CharField(label = 'Keywords:')
