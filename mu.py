
import os
import json

'''
    creates matchup data from event coverage
    reads top performing decks (/decklists) -> name, archetypes
    reads player matchups
        -> checks if both player have decklist
        -> apply results in matchup table

'''

def saveTable(table):
    with open('table.json', 'w') as outfile:
        json.dump(table, outfile)

def main():
    path = 'decklists/PT_2018_August/'
    all_files = os.listdir(path)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)

    topPlayers = []
    archetypes = []

    for txt in txt_files:
        txt = txt.replace('.txt','')
        txt = txt.split()

        idx = txt.index('-')
        name = txt[:idx]
        archetype =  ' '.join(txt[idx+1:])

        if archetype not in archetypes:
            archetypes.append(archetype)

        topPlayers.append({'name': name, 'archetype': archetype})
    
    numArch = len(archetypes)
    table = [[[0,0] for i in range(numArch)] for i in range(numArch)] # [[[wins, losses]]]
    games = 0

    with open('matchup.csv','r') as f:
        matchups = f.readlines()

        for line in matchups:
            p1 = line[1].split()
            p2 = line[5].split()

            a1 = None
            a2 = None

            for p in topPlayers:
                found = True
                for n in p1:
                    if n not in p['name']: # all of matchup names have to match name parts in the decklist name
                        found = False
                        break
                if found:
                    a1 = p['archetype']
                    break
            
            for p in topPlayers:
                found = True
                for n in p2:
                    if n not in p['name']:
                        found = False
                        break
                if found:
                    a2 = p['archetype']
                    break
            
            if a1 and a2:
                games += 1
                result = 0 if 'Won' in line[3] else 1
                idx1 = archetypes.index(a1)
                idx2 = archetypes.index(a2)
                table[idx1][idx2][result] += 1

                print(a1,a2,result)
    
    print(games)
    print(table)



main()