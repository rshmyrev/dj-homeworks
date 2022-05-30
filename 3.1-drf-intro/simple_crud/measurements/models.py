from django.db import models


class AutoDateTime(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class Project(AutoDateTime):
    """Объект на котором проводят измерения."""

    name = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()


class Measurement(AutoDateTime):
    """Измерение температуры на объекте."""

    value = models.FloatField()
    image = models.ImageField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
