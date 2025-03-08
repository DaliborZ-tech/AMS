from datetime import datetime, date

from django.db import models
from django.db.models import Model, DecimalField, CharField, ManyToManyField, IntegerField, \
    TextField, DateField, DateTimeField, ForeignKey, BooleanField, CASCADE, \
    EmailField


STATUS_CHOICES = [
    ('New', 'Nový'),
    ('Adviced', 'Zatermínován'),
    ('Realized', 'Realizovaný'),
    ('Billed', 'Vyúčtovaný'),
]

ADVICE_STATUS_CHOICES = [
    ('Success', 'Úspěšný'),
    ('Failed', 'Neúspěšný'),
]

TEAM_TYPE_CHOICES = [
    ('By customer', 'Zákazníkem'),
    ('By delivery crew', 'Dopravcem'),
    ('By assembly crew', 'Montážníky'),
]

WHOM_CHOICES = [
    ('To customer', 'Zákazníkovi'),
    ('To delivery crew', 'Dopravci'),
    ('To assembly crew', 'Montážníkům'),
    ('To customer care', 'Zákaznickému servisu')
]


class Store(Model):
    mndt = CharField(max_length=4, null=False, blank=False)
    numb = IntegerField(null=True, blank=True)
    store = CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return self.store


class Place(Model):
    zip_code = CharField(max_length=5, null=False, blank=False)
    city = CharField(max_length=32, null=False, blank=False)
    district = CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return self.city

    def __repr__(self):
        return self.zip_code + " " + self.city + " " + self.district


class Contact(Model):
    street = CharField(max_length=64, null=False, blank=False)
    number = CharField(max_length=16, null=False, blank=False)
    zip_code = CharField(max_length=5, null=False, blank=False)
    city = CharField(max_length=32, null=False, blank=False)
    phone = CharField(max_length=16, null=False, blank=False)
    phone_2 = CharField(max_length=16, null=True, blank=True)
    email = EmailField(null=True, blank=True)

    def __str__(self):
        order = self.order_set.first()
        if order:
            return order.customer_name
        return f"{self.city}, {self.street} {self.number}"


class Status(Model):
    created = DateTimeField(auto_now_add=True)
    status = CharField(max_length=32, null=False, blank=False, choices=STATUS_CHOICES)

    def __str__(self):
        return self.status


class AdviceStatus(Model):
    advice_status = CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return self.advice_status


class Advice(Model):
    created = DateTimeField(auto_now_add=True)
    whom = CharField(max_length=32, null=False, blank=False, choices=WHOM_CHOICES)
    status = CharField(max_length=32, null=False, blank=False, choices=ADVICE_STATUS_CHOICES)
    advice = TextField(null=False, blank=False)

    def __str__(self):
        return self.advice

    def created_date_format(self):
        if self.created:
            return datetime.strftime(self.created, '%d.%m.%Y')
        return None


class Article(Model):
    article = CharField(max_length=32, null=False, blank=False)
    price = IntegerField(null=True, blank=True)
    quantity = IntegerField(null=True, blank=True)
    note = TextField(null=True, blank=True)

    def __str__(self):
        return self.article


class Team(Model):
    company = CharField(max_length=32, null=False, blank=False)
    city = CharField(max_length=32, null=False, blank=False)
    phone = CharField(max_length=16, null=False, blank=False)
    email = EmailField(max_length=64, null=True, blank=True)
    web = CharField(max_length=64, null=True, blank=True)
    price_per_hour = DecimalField(null=True, blank=True)
    price_per_km = DecimalField(null=True, blank=True)
    region = CharField(max_length=32, null=True, blank=True)
    terms = TextField(null=True, blank=True)
    active = BooleanField(default=True)
    notes = TextField(null=True, blank=True)

    def __str__(self):
        return self.company


class Order(Model):
    mandant = CharField(max_length=4)
    store = ForeignKey(
        Store, on_delete=models.SET_NULL, null=True, blank=False)
    order_number = CharField(max_length=32, null=False, blank=False, unique=True)
    customer_name = CharField(max_length=64, null=False, blank=False)
    zip_code = CharField(max_length=5, null=False, blank=False)
    place = ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=False)
    contact = ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    evidence_term = DateField(null=True, blank=False)
    delivery_term = DateField(null=True, blank=True)
    article = ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True)
    advice = ForeignKey(Advice, on_delete=models.SET_NULL, null=True, blank=True)
    team_type = CharField(
        max_length=32, null=True, blank=True, choices=TEAM_TYPE_CHOICES)
    status = ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    notes = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number + " " + self.customer_name

    def __repr__(self):
        return self.order_number + " " + self.customer_name

    def created_date_format(self):
        if self.created:
            return datetime.strftime(self.created, '%d.%m.%Y')
        return None

    def updated_date_format(self):
        if self.updated:
            return datetime.strftime(self.updated, '%d.%m.%Y')
        return None

    def evidence_term_format(self):
        if self.evidence_term:
            return datetime.strftime(self.evidence_term, '%d.%m.%Y')
        return None

    def delivery_term_format(self):
        if self.delivery_term:
            return datetime.strftime(self.delivery_term, '%d.%m.%Y')
        return None

    class Meta:
        ordering = ['-created']
