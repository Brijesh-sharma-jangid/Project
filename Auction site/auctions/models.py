from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name', blank=True, null=True)
    amnt = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.amnt}"

class Category(models.Model):
    categoryName = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.categoryName}"

class Auction(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    isActive = models.BooleanField(default=1)
    start_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_auction', blank=True, null = True)
    urls = models.ImageField(blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="cat")
    watchlist = models.ManyToManyField(User,null=True, blank=True, related_name="watchlist")

    time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.id} -> {self.start_bid}  {self.title}->{self.desc}->{self.time}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', blank=True, null = True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='auction', blank=True, null = True)
    msg = models.CharField(max_length=1800)

    def __str__(self) -> str:
        return f"{self.msg}"


