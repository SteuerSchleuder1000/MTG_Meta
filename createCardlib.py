from urllib.request import urlopen
import json
from time import sleep
import os


cardTypes = ['Creature','Instant','Sorcery','Land','Planeswalker','Enchantment']

'''

Todo:
    - Plot prices vs playrate(% of decks, % of cards)
        - by rarity
        - by expansion?
    - Plot expansion makeup
    - histogram
    - tournament success

    scraping:
    top 32 -> day 2 coverage -> ca 50 per round

'''

def saveJson(json_obj,name):
    with open(name, 'w') as outfile:
        json.dump(json_obj, outfile)


def lookUpOriginalPrinting(cardInfo):
    sleep(0.1)
    url = cardInfo['prints_search_uri']
    response = urlopen(url)
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    
    for card in json_obj['data']:
        if not card['reprint']:
            return card['set_name']



def getCardInfo(cardname):
    sleep(0.1)
    url = 'https://api.scryfall.com/cards/named?exact='+cardname
    response = urlopen(url)
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)

    if 'eur' not in json_obj:
        json_obj['eur'] = -1
    return json_obj
    


def createCardlib(cardlib):
    itt = 0
    for cardname in cardlib:
        itt += 1
        print(round(itt/len(cardlib)*100,2),'%: ',cardname)
        info = getCardInfo(cardname)
        card = cardlib[cardname]
        if info:
            card['price'] = float(info['eur'])
            card['expansion'] = info['set_name'] if not info['reprint'] else lookUpOriginalPrinting(info)
            card['rarity'] = info['rarity']
            card['colorId'] = info['color_identity']
            card['cmc'] = info['cmc']
            if 'power' in info and 'toughness' in info:
                card['power'] = info['power']
                card['toughness'] = info['toughness']

            for t in cardTypes:
                if t in info['type_line']:
                    card['cardType'] = t
                    break
                
        
    saveJson(cardlib,'products/cardlib_pt_2018_8.json')



def readDecklist():
    path = 'decklists/PT_2018_August/'
    all_files = os.listdir(path)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)

    cardDict = {}
    numCards = 0
    numDecks = 0

    for txt in txt_files:
        with open(path+txt, 'r') as decklist:
            dl = decklist.readlines()
            dl = [x.strip() for x in dl]

            numDecks += 1
            mainboard = True
            # totPrice = 0

            for line in dl:
                if line == '':
                    mainboard = False
                    continue

                line = line.split()
                quantity = float(line[0])
                cardname = '_'.join(line[1:])

                numCards += quantity
                if cardname in cardDict:
                    cardDict[cardname]['decks'] += 1
                    if mainboard:
                        cardDict[cardname]['mainboard'] += quantity
                    else:
                        cardDict[cardname]['sideboard'] += quantity

                else:
                    cardDict[cardname] = {  
                        'decks': 1,
                        'mainboard': quantity if mainboard else 0,
                        'sideboard': 0 if mainboard else quantity,
                    }

    createCardlib(cardDict)


readDecklist()