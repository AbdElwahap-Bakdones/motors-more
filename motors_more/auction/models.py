from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
import json
# Create your models here.


class Country(models.Model):
    country_name = models.CharField(max_length=50)

    def __str__(self):
        return self.country_name


class Province(models.Model):
    province_name = models.CharField(max_length=50)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)


class Option(models.Model):
    option_name = models.CharField(max_length=150)


class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    phone = models.CharField(("phone"), max_length=50, null=True)
    location = models.ForeignKey(Province, on_delete=models.PROTECT, null=True)
    kind_art = [('User', 'User'), ('Company', 'Company'), ('Admin', 'Admin')]
    user_kind = models.CharField(choices=kind_art, default='User', max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_kind']

    def __str__(self):
        return self.email


class Client(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    gender_art = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(choices=gender_art, max_length=50)


class admin(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


class Company(models.Model):
    company_name = models.CharField(max_length=50)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


class CarBrand(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name


class CarModels(models.Model):
    name = models.CharField(max_length=150)
    brand_id = models.ForeignKey(CarBrand, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Car(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    mileage = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    type_art = [
        ('SEDAN', 'SEDAN'),
        ('COUPE', 'COUPE'),
        ('SPORTS CAR', 'SPORTS CAR'),
        ('HATCHBACK', 'HATCHBACK'),
        ('CONVERTIBLE', 'CONVERTIBLE'),
        ('SUV', 'SUV'),
        ('MINIVAN', 'MINIVAN'),
        ('PICKUP', 'PICKUP')]
    type = models.CharField(choices=type_art, max_length=50)
    manufacturing_year = models.PositiveIntegerField()
    clean_title = models.BooleanField()
    engine_art = [
        ('ESS', 'Internal petrol combustion engine'),
        ('DSL', 'DSL'),
        ('BEV', 'battery electric vehicle'),
        ('HEV', 'Hybrid electric vehicle')]
    engine_type = models.CharField(choices=engine_art, max_length=250)
    gear_art = [('Manual', 'Manual'), ('Automatic', 'Automatic')]
    gear_type = models.CharField(choices=gear_art, max_length=150)
    cylinders = models.CharField(max_length=50)
    notes = models.TextField(null=True)
    price = models.CharField(max_length=50, default='0')
    engine_capacity = models.CharField(max_length=50, default='2.0-liter engine')
    damage = models.CharField(max_length=250, null=True)
    drive_type_art = [('4WD', '4WD'), ('AWD', 'AWD'), ('FWD', 'FWD'), ('RWD', 'RWD')]
    drive_type = models.CharField(choices=drive_type_art, default='4WD', max_length=50)
    location = models.ForeignKey(Province, on_delete=models.PROTECT)
    car_models = models.ForeignKey(CarModels, on_delete=models.CASCADE, null=True)

    # def set_damage(self, data):
    #     self.damage = json.dumps(data)

    # def get_damage(self):
    #     return json.loads(self.damage)

    def __str__(self):
        return str(self.pk)


class CarOption(models.Model):
    option_id = models.ForeignKey(Option, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    is_special = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class Videos(models.Model):
    video_url = models.URLField()


class Images(models.Model):
    image = models.ImageField(upload_to='cars_images')


class Media(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Images, on_delete=models.CASCADE, null=True)
    video_id = models.ForeignKey(Videos, on_delete=models.CASCADE, null=True)
    kind_art = [('video', 'video'), ('image', 'image')]
    kind = models.CharField(choices=kind_art, max_length=50)


class Auction(models.Model):
    date = models.DateField()
    time = models.TimeField()
    status_art = [
        ('later auction', 'later auction'),
        ('live auction', 'live auction'),
        ('finished auction', 'finished auction'),
        ('canceled auction', 'canceled auction')
    ]
    status = models.CharField(choices=status_art, max_length=50, default='later auction')
    kind_art = [('User', 'User'), ('Company', 'Company')]
    kind = models.CharField(choices=kind_art, max_length=25)
    notebook_conditions = models.FloatField()


class RequestAuction(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)


class UserInAuction(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status_art = [('watcher', 'watcher'), ('participant', 'participant'), ('withdrawer', 'withdrawer')]
    status = models.CharField(choices=status_art, max_length=50)
    have_buy = models.BooleanField(default=False)


class CarInAuction(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    status_art = [('sold', 'sold'), ('for sale', 'for sale')]
    status = models.CharField(choices=status_art, max_length=50)


class AutoSold(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    price = models.FloatField()


class MainSection(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name


class TechnicalCondition(models.Model):
    main_section_id = models.ForeignKey(MainSection, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    status_art = [('Y', 'Very Good'), ('x', 'Good'), ('N', 'Bad'), ('UK', 'UnKnown')]
    status = models.CharField(choices=status_art, max_length=50)

    def __str__(self) -> str:
        return str(self.pk)


class AboutUs(models.Model):
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    title = models.TextField()
