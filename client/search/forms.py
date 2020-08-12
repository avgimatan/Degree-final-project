from django import forms
from django.shortcuts import render
from .models import Search

class SearchForm(forms.Form):
    link = forms.CharField(max_length=255)


