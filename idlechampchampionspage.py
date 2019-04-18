import json
from pprint import pprint
import re
from collections import OrderedDict
import math
from decimal import Decimal
from idlechampaccount import ICAccount

API = True

filename = '/home/txtsd/.local/share/Steam/steamapps/common/IdleChampions/IdleDragons_Data/StreamingAssets/downloaded_files/cached_definitions.json'

with open(filename) as f:
    file = f.read()

js = json.loads(file)

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

temp_count = 0
for effect in js_upgrade:
    if '{' in effect['effect']:
        # print(effect)
        str_effect = effect['effect']
        _effect = effect['effect'].replace("'", "\'")
        # print(_effect)
        # effect['effect'] = effect['effect'].replace('\"', '')
        temp = json.loads(_effect)
        # print(temp)
        # effect['effect'] = None
        # effect['effect'] = {}
        # js_upgrade.remove(effect)
        effect['effect'] = temp
        # js_upgrade.append(effect)
        # pprint(effect)

# pprint(js_upgrade)
# exit()

breakout = 0

wikitable = '''
[[Champions]] fight [[monsters]] in [[Idle Champions of the Forgotten Realms]].

Champions have special [[abilities]] and can equip [[gear]].

Strategically place them according to a [[Formation Strategy]] to overwhelm your enemies!

== Champions list ==
{{#vardefine:size|35px}}
{| class="wikitable sortable" style="text-align:center"
|-
! Slot
! data-sort-type="number"|<abbr title="Initial cost of the champion">Cost</abbr>
!
! Name
! data-sort-type="number"|<abbr title="Multiplied Bonus of all 'Damage' abilities">Damage
! data-sort-type="number"|<abbr title="Multiplied Bonus of all 'Damage All' abilities">Damage All
! Age
! Race
! Alignment
! data-sort-type="number"|<abbr title="Strength">Str</abbr>
! data-sort-type="number"|<abbr title="Dexterity">Dex</abbr>
! data-sort-type="number"|<abbr title="Constitution">Con</abbr>
! data-sort-type="number"|<abbr title="Intelligence">Int</abbr>
! data-sort-type="number"|<abbr title="Wisdom">Wis</abbr>
! data-sort-type="number"|<abbr title="Charisma">Cha</abbr>
! data-sort-type="number"|<abbr title="Cooldown of the champion's base attack">Base CD</abbr>
! data-sort-type="number"|<abbr title="Cooldown of the champion's ultimate attack">Ult CD</abbr>
'''


for hero in js_hero:
    if not hero['name'][:2] == 'E1':
        row = '|-' + '\n'
        row += '| ' + str(hero['seat_id']) + '\n'
        row += '| ' + ('{0:.2E}'.format(Decimal(hero['base_cost'])) if (int(hero['base_cost']) / 100) > 1 else hero['base_cost']).replace('E+', 'e') + '\n'
        row += '| ' + '{{{{Icon-Link|{name}|size={{{{#var:size}}}}|notext=yes}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '[[{name}]]'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=damage}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=damageAll}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=age}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=race}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=alignment}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=str}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=dex}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=con}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=int}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=wis}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=cha}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=base_cd}}}}'.format(name=hero['name']) + '\n'
        row += '| ' + '{{{{:{name}|include=ult_cd}}}}'.format(name=hero['name']) + '\n'

        wikitable += (row + '\n')

# Wikitable end
wikitable += '|}\n'
wikitable += '''

{{Navbox-Champions}}
{{Navbox-IdleChampions}}

[[Category:Champions]]'''

with open('output/champions.txt', 'w') as f:
    f.write(wikitable)

if API:
    instance = ICAccount()
    instance.login()

    COMPARE_PARAMS = {
        'action': 'compare',
        'fromtitle': 'Champions',
        'totext': wikitable,
        'prop': 'diff|diffsize|title'
    }
    QUERY_PARAMS = {
        'action': 'compare',
        'fromtitle': 'Champions',
        'totext': wikitable,
        'prop': 'diff|diffsize|title'
    }

    R1 = instance.post(data=COMPARE_PARAMS)
    # print(R1.status_code)
    # print(R1.url)
    resjs = R1.json()

    if resjs['compare']['diffsize'] == 0:
        print('No changes')
    else:
        print('\nDIFF:\t\t(&#160; is &nbsp;) ')
        print(resjs['compare']['body'])
        _summary = input('\nEnter change summary: ')
        EDIT_PARAMS = {
            'action': 'edit',
            'title': 'Champions',
            'text': wikitable,
            'bot': '1',
            'nocreate': '1',
            'summary': _summary
        }
        pprint({key: value for key, value in EDIT_PARAMS.items()
             if key is not 'text'})
        print('Posting...')
        R2 = instance.post(data=EDIT_PARAMS)
        print(R2.status_code)
        pprint(R2.json())
