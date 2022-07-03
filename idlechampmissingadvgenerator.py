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
REDOWNLOAD = False
POST = False
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

adv_filename = 'json/adventure_defines.json'
area_filename = 'json/adventure_area_defines.json'
camp_filename = 'json/campaign_defines.json'
monster_filename = 'json/monster_defines.json'

with open(filename) as f:
    file = f.read()
with open(adv_filename) as f:
    adv_file = f.read()
with open(area_filename) as f:
    area_file = f.read()
with open(camp_filename) as f:
    camp_file = f.read()
with open(monster_filename) as f:
    monster_file = f.read()

js = json.loads(file)
js_adv = json.loads(adv_file)
js_area = json.loads(area_file)
js_camp = json.loads(camp_file)
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

for mon in js_mon:
    if mon['name'] == 'Jarlaxle':
        temp = mon
        js_mon.remove(mon)
        temp['name'] = 'Jarlaxle (Monster)'
        js_mon.append(temp)

# taglist = {}
# for rule in js_game_rule:
#     if rule['rule_name'] == 'enemy_hover_tags':
#         for tag in rule['rule']['tags']:
#             taglist.update({tag: set()})

# # pprint(taglist)

# for monster in js_adv:
#     for tag in monster['tags']:
#         if tag in taglist:
#             taglist[tag].add(monster['name'])

_js_adv = sorted(js_adv, key=lambda x: x['id'])
__js_adv = sorted(_js_adv, key=lambda x: x['area_set_id'])
__js_adv = sorted(__js_adv, key=lambda x: x['location_id'])
__js_adv = sorted(__js_adv, key=lambda x: x['campaign_id'])

__js_area = sorted(js_area, key=lambda x: x['id'])
__js_area = sorted(__js_area, key=lambda x: x['area_id'])
__js_area = sorted(__js_area, key=lambda x: x['area_set_id'])
# pprint(__js_area)

__js_mon = sorted(js_mon, key=lambda x: x['id'])

# pprint(__js_adv)
set_advs = set()

print('id' + ',' + 'campaign_id' + ',' + 'location_id' + ',' + 'area_set_id' + ',' + 'name')
for adv in _js_adv:
    if adv['id'] not in set_advs:
        set_advs.add(adv['id'])
        name = adv['name']
        if name == 'Free Play':
            for _adv in __js_adv:
                if adv['variant_adventure_id'] == _adv['id']:
                    name = _adv['name'] + ' ' + name
        if 'variant_adventure_id' in adv:
            name = ''⟶ + name
        print(str(adv['id']) + ',' + str(adv['campaign_id']) + ',' + str(adv['location_id']) + ',' + str(adv['area_set_id']) + ',' + name)
