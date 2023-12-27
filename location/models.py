from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class Region(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]
        verbose_name = "Region"
        verbose_name_plural = "Regions"


class City(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]
        verbose_name = "City"
        verbose_name_plural = "Cities"


class Address(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.country} {self.city} {self.region} {self.street}"

    class Meta:
        ordering = ["-country"]
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
