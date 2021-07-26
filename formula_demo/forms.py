from django import forms

class AreaForm(forms.Form):
    length = forms.IntegerField(label='Length', widget=forms.TextInput(attrs={'class': 'px-2 py-1 border rounded-sm'}))
    width = forms.IntegerField(label='Width', widget=forms.TextInput(attrs={'class': 'px-2 py-1 border rounded-sm'}))