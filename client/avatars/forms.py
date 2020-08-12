from django import forms
from . import models


class AvatarForm(forms.ModelForm):
    class Meta:
        fields = ('avatar_name', 'avatar_password', 'avatar_email')
        model = models.Avatar

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

