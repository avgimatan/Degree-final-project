

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()


class Search(models.Model):
    user = models.ForeignKey(User, related_name="Search")
    onion_link = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.User.username

    def save(self, *args, **kwargs):
        # self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "search:choose",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        unique_together = ["onion_link"]

'''
class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = ['onion_link']'''