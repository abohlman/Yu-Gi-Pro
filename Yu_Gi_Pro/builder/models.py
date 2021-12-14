from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):   #Stores universal card attributes pulled from the API
    BAN_VALUES = (
        ('B', 'Banned'),
        ('L', 'Limited'),
        ('S', 'Semi-Limited'),
        ('U', 'Unlimited'),
    )
    id = models.CharField(primary_key=True, max_length=10)   #Card code
    name = models.CharField(max_length=200)   #Card Name
    type = models.CharField(max_length=20)   #Type of card eg. Normal Monster, Spell, etc.
    race = models.CharField(max_length=50)   #Type of type eg. Continuous spell, Dragon, etc.
    archetype = models.CharField(max_length=50)
    TCGP_price = models.FloatField() #Average of 5 returned prices
    ban_status = models.CharField(max_length=1, choices=BAN_VALUES)

class Monster(models.Model):   #Stores card attributes for Non-Link or Pendulums
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    atk = models.IntegerField()
    df = models.IntegerField()    #short for defense because def is reserved
    desc = models.TextField()
    attr = models.CharField(max_length=10)
    level = models.IntegerField()

class Spell_Trap(models.Model): #Stores card attributes for Spells and Traps
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    desc = models.TextField()

class Pendulum(models.Model):   #Attributes are identical to monsters but I have a feeling they will need to be seperated out
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    atk = models.IntegerField()
    df = models.IntegerField()    #short for defense because def is reserved
    desc = models.TextField()
    attr = models.CharField(max_length=10)
    level = models.IntegerField()

class Link(models.Model):  #Stores attributes for link monsters because they insist on being different
    MARKERS = (
        ('T', 'Top'),
        ('TL', 'Top-Left'),
        ('TR', 'Top-Right'),
        ('L', 'Left'),
        ('R', 'Right'),
        ('B', 'Bottom'),
        ('BL', 'Bottom-Left'),
        ('BR', 'Bottom-Right'),
    )
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    atk = models.IntegerField()
    desc = models.TextField()
    attr = models.CharField(max_length=10)
    linkval = models.IntegerField()
    linkmarkers = models.CharField(max_length=20)    #This will probably be incorrect but fuck it

class Deck(models.Model):   #Stores basic deck info
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Deck_Card(models.Model):  #Links Cards to Decks
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    main_amount = models.IntegerField() #Number of copies in main or extra deck
    side_amount = models.IntegerField() #Number of copies in side deck
