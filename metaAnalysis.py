import json
import matplotlib.pyplot as plt

cardlib_path = 'products/cardlib_pt_2018_8.json'

def piePlot(labels, sizes):

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,  labels=labels, autopct='%1.1f%%',startangle=90)
    ax1.axis('equal') 

    plt.show()


def histPlot(x):
    n, bins, patches = plt.hist(x,20)
    plt.show()

def scatterPlot(x,y):
    plt.scatter(x,y)
    plt.show()




def countExpansions():
    with open(cardlib_path,'r') as f:
        cardlib = json.load(f)
        
        expansions = []
        count = []

        for cardname in cardlib:
            card = cardlib[cardname]
            if 'cardType' not in card:
                continue
            if card['cardType'] == 'Land':
                continue
            if 'expansion' in card:
                exp = card['expansion']
                num = float(card['mainboard']) + float(card['sideboard'])
                if exp in expansions:
                    idx = expansions.index(exp)
                    count[idx] += num
                else:
                    expansions.append(exp)
                    count.append(num)

        print(count)
        count, expansions = zip(*sorted(zip(count, expansions)))
        plt.pie(count,  labels=expansions, autopct='%1.1f%%',startangle=90)
        plt.show()


def countCards():
    with open(cardlib_path,'r') as f:
        cardlib = json.load(f)
        
        count = []

        for cardname in cardlib:
            card = cardlib[cardname]
            num = float(card['mainboard']) + float(card['sideboard'])
            count.append(num)
            if num > 150:
                print(cardname, num)
        
        count = sorted(count)
        print(len(count),count)
        n, bins, patches = plt.hist(count,20)
        plt.show()
    


def priceVsFreq():
    with open(cardlib_path,'r') as f:
        cardlib = json.load(f)
        
        count = []
        prices = []

        for cardname in cardlib:
            card = cardlib[cardname]
            if 'rarity' not in card:
                print(cardname,card)
                continue
            if card['rarity'] not in ['uncommon']:
                continue

            num = float(card['mainboard']) + float(card['sideboard'])
            count.append(num)
            if 'price' in card:
                prices.append(card['price'])
            else:
                prices.append(0)
        
        plt.scatter(count,prices,s=1)
        plt.show()



def countRarities():
    with open(cardlib_path,'r') as f:
        cardlib = json.load(f)
        
        rarities = []
        count = []

        for cardname in cardlib:
            card = cardlib[cardname]
            if 'cardType' in card:
                if card['cardType'] == 'Land':
                    continue
            if 'rarity' in card:
                r = card['rarity']
                num = float(card['mainboard']) + float(card['sideboard'])
                if r in rarities:
                    idx = rarities.index(r)
                    count[idx] += num
                else:
                    rarities.append(r)
                    count.append(num)

        print(count)
        count, rarities = zip(*sorted(zip(count, rarities)))
        plt.pie(count,  labels=rarities, autopct='%1.1f%%',startangle=90)
        plt.show()
        # plt.savefig('products/rarities.png')






countRarities()