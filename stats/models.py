from django.db import models


class Statistics(models.Model):
    model_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_type} - {self.created_at}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Statistics"
        verbose_name_plural = "Statistics"
