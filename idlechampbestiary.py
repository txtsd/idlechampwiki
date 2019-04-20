import json
from pprint import pprint
import re
from collections import OrderedDict
import math
from decimal import Decimal
from idlechampaccount import ICAccount

API = True
POST = True
SHOW_CHANGES = False
_summary = None

if API:
    instance = ICAccount()
    instance.login()

filename = '/home/txtsd/.local/share/Steam/steamapps/common/IdleChampions/IdleDragons_Data/StreamingAssets/downloaded_files/cached_definitions.json'

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
{creature_list}

==See also==
[[Bosses]]

{{{{Navbox-IdleChampions}}}}'''

# Stub status
page_text = '{{{{stub}}}}' + page_text


taglist = {}
for rule in js_game_rule:
    if rule['rule_name'] == 'enemy_hover_tags':
        for tag in rule['rule']['tags']:
            taglist.update({tag: set()})

# pprint(taglist)

for monster in js_mon:
    for tag in monster['tags']:
        if tag in taglist:
            taglist[tag].add(monster['name'])

# pprint(taglist)

creature_list = ''
for mon_type in taglist:
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

page_text = page_text.format(creature_list=creature_list)

with open('output/bestiary.txt', 'w') as f:
    f.write(page_text)

if API:
    COMPARE_PARAMS = {
        'action': 'compare',
        'fromtitle': 'Bestiary',
        'totext': page_text,
        'prop': 'diff|diffsize|title'
    }

    R1 = instance.post(data=COMPARE_PARAMS)
    # print(R1.status_code)
    # print(R1.url)
    resjs = R1.json()

    if 'compare' in resjs:
        if resjs['compare']['diffsize'] == 0:
            print('Bestiary: No changes')
        else:
            print('Bestiary: Changes detected!')
            if SHOW_CHANGES:
                print('\nDIFF:\t\t(&#160; is &nbsp;) ')
                print(resjs['compare']['body'])
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
                # pprint({key: value for key, value in EDIT_PARAMS.items() if key is not 'text'})
                print('Bestiary: Posting...')
                R2 = instance.post(data=EDIT_PARAMS)
                if (R2.status_code == 200) or (R2.status_code == '200'):
                    print('Bestiary: Success!')
                else:
                    print('Bestiary: FAIL!')
                # pprint(R2.json())
    else:
        pprint(resjs)
