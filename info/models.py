from django.db import models

# Create your models here.
class Tip(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tip #{self.pk}"
