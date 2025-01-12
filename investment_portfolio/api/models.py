from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    balance = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"User({self.name}, {self.balance})"


class Asset(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assets'
    )
    coin_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    value_rub = models.IntegerField()

    def __str__(self):
        return f"Asset({self.coin_name}, {self.quantity}, {self.value_rub})"
