from django.db import models


class Contact(models.Model):
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=500)
    email = models.EmailField()
    reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
