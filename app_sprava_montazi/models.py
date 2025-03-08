from datetime import datetime, date

from django.db import models
from django.db.models import Model, DecimalField, CharField, ManyToManyField, \
    IntegerField, TextField, DateField, DateTimeField, ForeignKey, \
    BooleanField, CASCADE, SET_NULL, EmailField


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
    zip_code = CharField(max_length=5, null=False, blank=False,
                         verbose_name='PSČ')
    city = CharField(max_length=32, null=False, blank=False,
                     verbose_name='Město')
    district = CharField(max_length=32, null=False, blank=False,
                         verbose_name='Okres')

    def __str__(self):
        return self.city

    def __repr__(self):
        return self.zip_code + " " + self.city + " " + self.district


class Contact(Model):
    street = CharField(max_length=64, null=False, blank=False,
                       verbose_name='Ulice')
    number = CharField(max_length=16, null=False, blank=False,
                       verbose_name='Číslo')
    zip_code = CharField(max_length=5, null=False, blank=False,
                         verbose_name='PSČ')
    city = CharField(max_length=32, null=False, blank=False,
                     verbose_name='Město')
    phone = CharField(max_length=16, null=False, blank=False,
                      verbose_name='Telefon')
    phone_2 = CharField(max_length=16, null=True, blank=True,
                        verbose_name='Telefon 2')
    email = EmailField(null=True, blank=True, verbose_name='E-mail')

    def __str__(self):
        return f"{self.city}, {self.street} {self.number}"


class Status(Model):
    created = DateTimeField(auto_now_add=True, verbose_name='Vytvořen')
    status = CharField(max_length=32, null=False, blank=False,
                       choices=STATUS_CHOICES, verbose_name='Stav')

    def __str__(self):
        return self.status


class Advice(Model):
    created = DateTimeField(auto_now_add=True, verbose_name='Vytvořeno')
    whom = CharField(max_length=32, null=False, blank=False,
                     choices=WHOM_CHOICES, verbose_name='Komu')
    status = CharField(max_length=32, null=False, blank=False,
                       choices=ADVICE_STATUS_CHOICES, verbose_name='Stav')
    advice = TextField(null=False, blank=False, verbose_name='Popis')

    def __str__(self):
        return self.advice

    @property
    def created_date_format(self):
        if self.created:
            return datetime.strftime(self.created, '%d.%m.%Y')
        return None


class Article(Model):
    article = CharField(max_length=32, null=False, blank=False,
                        verbose_name='Artikl')
    price = IntegerField(null=True, blank=True, verbose_name='Cena')
    quantity = IntegerField(null=True, blank=True, verbose_name='Množství')
    note = TextField(null=True, blank=True, verbose_name='Popis')

    def __str__(self):
        return self.article


class Team(Model):
    company = CharField(max_length=32, null=False, blank=False,
                        verbose_name='Společnost')
    city = CharField(max_length=32, null=False, blank=False,
                     verbose_name='Město')
    phone = CharField(max_length=16, null=False, blank=False,
                      verbose_name='Telefon')
    email = EmailField(max_length=64, null=True, blank=True,
                       verbose_name='E-mail')
    web = CharField(max_length=64, null=True, blank=True,
                    verbose_name='Web')
    price_per_hour = DecimalField(max_digits=10, decimal_places=2,
                                  null=True, blank=True,
                                  verbose_name='Cena za hodinu')
    price_per_km = DecimalField(max_digits=10, decimal_places=2,
                                null=True, blank=True,
                                verbose_name='Cena za km')
    region = CharField(max_length=32, null=True, blank=True,
                       verbose_name='Region')
    terms = TextField(null=True, blank=True, verbose_name='Termíny')
    active = BooleanField(default=True, verbose_name='Aktivní')
    notes = TextField(null=True, blank=True, verbose_name='Poznámky')

    def __str__(self):
        return self.company


class Order(Model):
    mandant = CharField(max_length=4, null=False, blank=False,
                        verbose_name='Mandant')
    store = ForeignKey(Store, on_delete=models.SET_NULL, null=True,
                       blank=False, verbose_name='OD/sklad')
    order_number = CharField(max_length=32, null=False, blank=False,
                             unique=True, verbose_name='Číslo zakázky')
    customer_name = CharField(max_length=64, null=False, blank=False,
                              verbose_name='Jméno zákazníka')
    zip_code = CharField(max_length=5, null=False, blank=False,
                         verbose_name='PSČ')
    place = ForeignKey(Place, on_delete=models.SET_NULL, null=True,
                       blank=False, verbose_name='Oblast')
    contact = ForeignKey(Contact, on_delete=models.SET_NULL, null=True,
                         blank=True, verbose_name='Kontakt')
    evidence_term = DateField(null=True, blank=False,
                              verbose_name='Termín evidence')
    delivery_term = DateField(null=True, blank=True,
                              verbose_name='Termín doručení')
    article = ForeignKey(Article, on_delete=models.SET_NULL, null=True,
                         blank=True, verbose_name='Artikl')
    advice = ForeignKey(Advice, on_delete=models.SET_NULL, null=True,
                        blank=True, verbose_name='Avizace')
    team_type = CharField(max_length=32, null=True, blank=True,
                          choices=TEAM_TYPE_CHOICES,
                          verbose_name='Realizace kým')
    team = ForeignKey(Team, on_delete=SET_NULL, null=True,
                      blank=True, verbose_name='Montážní tým')
    status = ForeignKey(Status, on_delete=models.SET_NULL, null=True,
                        blank=True, verbose_name='Stav')
    notes = TextField(null=True, blank=True, verbose_name='Poznámky')
    created = DateTimeField(auto_now_add=True, verbose_name='Vytvořeno')
    updated = DateTimeField(auto_now=True, verbose_name='Upraveno')

    def __str__(self):
        return self.order_number + " " + self.customer_name

    def __repr__(self):
        return self.order_number + " " + self.customer_name

    @property
    def created_date_format(self):
        if self.created:
            return datetime.strftime(self.created, '%d.%m.%Y')
        return None

    @property
    def updated_date_format(self):
        if self.updated:
            return datetime.strftime(self.updated, '%d.%m.%Y')
        return None

    @property
    def evidence_term_format(self):
        if self.evidence_term:
            return datetime.strftime(self.evidence_term, '%d.%m.%Y')
        return None

    @property
    def delivery_term_format(self):
        if self.delivery_term:
            return datetime.strftime(self.delivery_term, '%d.%m.%Y')
        return None

    class Meta:
        ordering = ['-created']
