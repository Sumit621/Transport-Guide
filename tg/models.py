from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class BusRoutes(models.Model):
    place=models.CharField(max_length=250)
    values=models.TextField()
    roads=models.TextField()
    geoLocLat=models.FloatField()
    geoLocLon=models.FloatField()
    def __str__(self):
        return self.place

class UserPrefHist(models.Model):
    UserName=models.CharField(max_length=250)
    preferredRoutes=models.TextField()
    history=models.TextField()
    def __str__(self):
        return self.UserName

class PoribohonRoutes(models.Model):
    poribohonName=models.CharField(max_length=250)
    fullRoute=models.TextField()
    imgLink=models.CharField(max_length=300)
    def __str__(self):
        return self.poribohonName

class PlaceLocs(models.Model):
    placeName=models.CharField(max_length=250)
    geoLocLat=models.FloatField()
    geoLocLon=models.FloatField()
    def __str__(self):
        return self.placeName

class HubLocs(models.Model):
    hubName=models.CharField(max_length=250)
    geoLocLat=models.FloatField()
    geoLocLon=models.FloatField()
    def __str__(self):
        return self.hubName

class Review(models.Model):
    uName=models.ForeignKey(User, models.CASCADE, related_name="uReviews")
    poribohon=models.ForeignKey(PoribohonRoutes, models.CASCADE, related_name="pReviews")
    comment=models.TextField()

class LogData(models.Model):
    uName=models.ForeignKey(User, models.CASCADE, related_name="uLog")
    logType=models.CharField(max_length=250)
    details=models.TextField()
    def __str__(self):
        return self.details

class SignInOutLog(models.Model):
    uName=models.ForeignKey(User, models.CASCADE, related_name="uSignInOut")
    details=models.TextField()
    def __str__(self):
        return self.details




