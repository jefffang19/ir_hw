from django import forms

class WordForm(forms.Form):
    keywords = forms.CharField(label = 'Keywords:')

class UploadFileForm(forms.Form):
    tag = forms.CharField(label = 'Tag')
    file = forms.FileField(label = 'File')