from django.db.models.base import Model
from requests.models import to_native_string
from builder.models import Card, Monster, Spell_Trap, Pendulum, Link
from django.core.management.base import BaseCommand, CommandError
import requests
import json
import time

#API shell for the ygoprodeck.com API run from the command line
#This is used to get up-to-date card information for the deck builder
#Entering "python manage.py update" in the command line will call this script

class Command(BaseCommand):
    help = 'Updates the Card Database'

    def handle(self, *args, **kwargs):
        endpoint = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
        response = requests.get(endpoint + '?format=tcg')
        if (response.ok):
            cards = response.json()
            start_time = round(time.time() * 1000)
            count = 0
            
            #Loop to parse cards from json dictionary
            for key in cards['data']:
                id = key['id']
                if not Card.objects.filter(id = id).exists():
                    name = key['name']
                    type = key['type']
                    race = key['race']
                    prices = key['card_prices']
                    TCGP_price = prices[0]['tcgplayer_price']

                    if 'ban_tcg' in key:
                        ban_status = key['banlist_info'][0]['ban_tcg']
                        if ban_status == 'Banned':
                            ban_status = 'B'
                        elif ban_status == 'Limited':
                            ban_status = 'L'
                        elif ban_status == 'Semi-Limited':
                            ban_status = 'S'
                    else:
                        ban_status = 'U'
                
                    if 'archetype' in key:
                        archetype = key['archetype']
                    else:
                        archetype = 'None'
                
                    card = Card(id = id, name = name, type = type, race = race, TCGP_price = TCGP_price,
                        ban_status = ban_status, archetype = archetype)
                    card.save()

                    if type == 'Spell Card' or type == 'Trap Card':
                        desc = key['desc']
                        spell_trap = Spell_Trap(desc = desc, card = card)
                        spell_trap.save()
                    elif type == 'Link Monster':
                        atk = key['atk']
                        linkval = key['linkval']
                        linkmarkers = ''
                        for marker in key['linkmarkers']:
                            linkmarkers = linkmarkers + marker + '_'    #The individual link markers are spliced out later
                        desc = key['desc']
                        attr = key['attribute']
                        link = Link(atk = atk, linkval = linkval, linkmarkers = linkmarkers, desc = desc, attr = attr, card = card)
                        link.save()
                    elif 'Pendulum' in type:
                        atk = key['atk']
                        df = key['def']
                        attr = key['attribute']
                        level = key['level']
                        desc = key['desc']
                        pend = Pendulum(atk = atk, df = df, attr = attr, level = level, desc = desc, card = card)
                        pend.save()
                    else:
                        atk = key['atk']
                        df = key['def']
                        attr = key['attribute']
                        level = key['level']
                        desc = key['desc']
                        monster = Monster(atk = atk, df = df, attr = attr, level = level, desc = desc, card = card)
                        monster.save()

                    count = count + 1

            #end Card loop
            stop_time = round(time.time() * 1000)
            ttime = stop_time - start_time
            print(count, ' cards added in ', ttime, 'ms')
    
        else:
            print(response)