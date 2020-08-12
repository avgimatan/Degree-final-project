from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Avatar(models.Model):
    user = models.ForeignKey(User, related_name="avatars")
    created_at = models.DateTimeField(auto_now=True)
    avatar_name = models.CharField(max_length=255, unique=True)
    avatar_password = models.CharField(max_length=255)
    avatar_email = models.CharField(max_length=255)
    is_choosen = models.BooleanField(default=False)

    def __str__(self):
        return self.avatar_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "search:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-user"]
        unique_together = ["user", "avatar_name", "avatar_password", "avatar_email", "created_at", "is_choosen"]
