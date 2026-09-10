
from django.db import models
from django.contrib.auth.models import User


class Prediction(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    bmi = models.FloatField()

    cycle = models.IntegerField()
    cycle_length = models.IntegerField()

    weight_gain = models.IntegerField()
    hair_growth = models.IntegerField()
    pimples = models.IntegerField()

    prediction = models.IntegerField()
    probability = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.prediction}"

