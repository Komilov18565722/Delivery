from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Orders(models.Model):
    # 0- Buyurtma bo`sh hali hechkim band etmagan rang: green
    # 1- Buyurtmani kimdir kelishuv uchun band etgan rang: orange
    # 2- Buyurtmani kimdir olib bo`lgan rang: grey`

    status = models.IntegerField()
    order_type = models.CharField(max_length=255)
    order_weight = models.TextField()
    start_location = models.TextField()
    finished_location = models.TextField()
    delivery_fee = models.TextField()
    period = models.TextField()
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.status}'

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    feedback = models.TextField(null=True, blank=True)

class Work(models.Model):
    order = models.ForeignKey(Orders, on_delete=  models.CASCADE)
    driver = models.ForeignKey(User, on_delete= models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    diff_times = models.CharField(max_length=255, null=True, blank=True)
    fine = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.order}'




