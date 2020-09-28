from django import forms

class WordForm(forms.Form):
    keywords = forms.CharField(label = 'Keywords:')

class UploadFileForm(forms.Form):
    tag = forms.CharField(label = 'Tag')
    mode = forms.CharField(label = 'Mode')
    file = forms.FileField(label = 'File')