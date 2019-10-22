import json
from pprint import pprint
import re
from collections import OrderedDict
import math
from decimal import Decimal
from idlechampaccount import ICAccount
import subprocess
import filecmp
import os


COMPARE = True
POST = False
REDOWNLOAD = False
SHOW_CHANGES = False
_summary = None

if POST:
    instance = ICAccount()
    instance.login()

# filename = '/home/txtsd/.local/share/Steam/steamapps/common/IdleChampions/IdleDragons_Data/StreamingAssets/downloaded_files/cached_definitions.json'
filename = '/tmp/cached_definitions.json'
if REDOWNLOAD or not os.path.isfile(filename):
    result = requests.get('http://master.idlechampions.com/~idledragons/post.php?call=getdefinitions')
    with open(filename, 'w') as f:
        if result.status_code == 200:
            f.write(result.text)

monster_filename = 'json/monster_defines.json'

with open(filename) as f:
    file = f.read()
with open(monster_filename) as f:
    monster_file = f.read()

js = json.loads(file)
js_mon = json.loads(monster_file)

js_graphic = js['graphic_defines']
js_attack = js['attack_defines']
js_hero = js['hero_defines']
js_hero_skin = js['hero_skin_defines']
js_upgrade = js['upgrade_defines']
js_premium_item = js['premium_item_defines']
js_sound = js['sound_defines']
js_buff = js['buff_defines']
js_loot = js['loot_defines']
js_achievement = js['achievement_defines']
js_ability = js['ability_defines']
js_effect = js['effect_defines']
js_changelog = js['changelog_defines']
js_text = js['text_defines']
js_chest_type = js['chest_type_defines']
js_effect_key = js['effect_key_defines']
js_tutorial_state = js['tutorial_state_defines']
js_game_rule = js['game_rule_defines']
js_news = js['news_defines']
js_language = js['language_defines']
js_familiar = js['familiar_defines']

page_text = '''
The \'\'\'Bestiary\'\'\' for [[Idle Champions of the Forgotten Realms]].

==Description==
Idle Champions features a wide array of races from the D&D universe as opponents, such as [[Orc]]s, [[Hobgoblin]]s and [[Gelatinous Cube]]s.

==List Of Creatures==
{creature_list_text}

==List of Types==
__type_list_text__

==See also==
[[Bosses]]

__Navbox-IdleChampions__'''

for mon in js_mon:
    if mon['name'] == 'Jarlaxle':
        temp = mon
        js_mon.remove(mon)
        temp['name'] = 'Jarlaxle (Monster)'
        js_mon.append(temp)


__js_mon = sorted(js_mon, key=lambda x: x['id'])
type_list = set()
taglist = {}
types = ['boss',
        'flying',
        'item',
        'melee',
        'ranged',
        'relentless',
        'spawner',
        'static']

for monster in __js_mon:
    for tag in monster['tags']:
        if tag not in taglist:
            type_list.add(tag)

for item in type_list:
    # if item not in types:
        taglist.update({item: set()})

# print(taglist)

for monster in __js_mon:
    for tag in monster['tags']:
        if tag in taglist:
            taglist[tag].add(monster['name'])

# pprint(taglist)
# pprint(type_list)

creature_list = ''
for mon_type in sorted(taglist):
    if mon_type not in types:
        creature_list += '[[{mon_type}]]\n'.format(mon_type=mon_type.capitalize())
        creatures = ''
        # print(mon_type)
        # pprint(sorted(taglist[mon_type], key=lambda x: x['name']))
        for mob in sorted(taglist[mon_type]):
            creatures += '[[{mob}]], '.format(mob=mob)
        creatures = ': ' + creatures
        creatures = creatures[:-2]
        creatures += '\n'
        creature_list += creatures

page_text = page_text.format(creature_list_text=creature_list)

page_text = page_text.replace('__type_list_text__', '{type_list_text}')

# print(page_text)

list_of_types = ''
for mon_type in sorted(taglist):
    if mon_type in types:
        list_of_types += '[[{mon_type}]]\n'.format(mon_type=mon_type.capitalize())
        creatures = ''
        # print(mon_type)
        # pprint(sorted(taglist[mon_type], key=lambda x: x['name']))
        for mob in sorted(taglist[mon_type]):
            creatures += '[[{mob}]], '.format(mob=mob)
        creatures = ': ' + creatures
        creatures = creatures[:-2]
        creatures += '\n'
        list_of_types += creatures

page_text = page_text.format(type_list_text=list_of_types)

# print(page_text)

page_text = page_text.replace('__Navbox-IdleChampions__', '{{Navbox-IdleChampions}}')
# Stub status
page_text = '{{stub}}' + page_text

with open('output/bestiary.txt', 'w') as f:
    f.write(page_text)

if COMPARE:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isdir(os.path.join(dir_path, 'output')):
        os.makedirs(os.path.join(dir_path, 'output'))
    main_file = os.path.join(dir_path, 'output/bestiary.txt')
    posted_file = os.path.join(dir_path, 'output/posted/bestiary.txt')
    try:
        result = filecmp.cmp(main_file, posted_file, shallow=False)
    except FileNotFoundError as e:
        print('No source found')
        result = None

    if result is not None:
        if result:
            print('No changes')
        else:
            print('Changes detected!')
            if SHOW_CHANGES:
                result = subprocess.run(['git', 'diff', '--no-index', posted_file, main_file])
            if POST:
                if _summary is None:
                    _summary = input('Enter change summary: ')
                EDIT_PARAMS = {
                    'action': 'edit',
                    'title': 'Bestiary',
                    'text': page_text,
                    'bot': '1',
                    'nocreate': '1',
                    'summary': _summary
                }
                print('Posting...')
                R2 = instance.post(data=EDIT_PARAMS)
                if R2.status_code == 200:
                    print('Success!')
                    with open('output/posted/bestiary.txt', 'w') as g:
                        g.write(page_text)
                else:
                    print('FAIL!')
