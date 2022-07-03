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

promotions_filename = 'json/promotions.json'

with open(filename) as f:
    file = f.read()
with open(promotions_filename) as f:
    promotions_file = f.read()

js = json.loads(file)
js_promo = json.loads(promotions_file)

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

set_promo = set()

for promo in js_promo:
    if promo['promotion_id'] not in set_promo:
        set_promo.add(promo['promotion_id'])
        print(promo)
        print(promo['promotion_id'], promo['name'])





    # # Stub status
    # page_text = '{{stub}}' + '\n' + page_text
    # page_text = (page_text + '\n' + footer)
    # # print(page_text)

    # with open('output/{filename}.txt'.format(filename=name), 'w') as f:
    #     f.write(page_text)

    if COMPARE:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if not os.path.isdir(os.path.join(dir_path, 'output')):
            os.makedirs(os.path.join(dir_path, 'output'))
        main_file = os.path.join(dir_path, 'output/{filename}.txt'.format(filename=name))
        posted_file = os.path.join(
            dir_path, 'output/posted/{filename}.txt'.format(filename=name))
        try:
            result = filecmp.cmp(main_file, posted_file, shallow=False)
        except FileNotFoundError as e:
            print('{name}: No source found'.format(name=name))
            result = None

        if (result is not None) and (result == True):
            print('{name}: No changes'.format(name=name))
        else:
            print('{name}: Changes detected! <----------'.format(name=name))
            if SHOW_CHANGES:
                result = subprocess.run(['git', 'diff', '--no-index', posted_file, main_file])
            if POST:
                if _summary is None:
                    _summary = input('Enter change summary: ')
                EDIT_PARAMS = {
                    'action': 'edit',
                    'title': name,
                    'text': page_text,
                    'bot': '1',
                    'summary': _summary
                    # 'nocreate': '1',
                }
                print('{name}: Posting...'.format(name=name))
                R2 = instance.post(data=EDIT_PARAMS)
                if R2.status_code == 200:
                    if 'error' not in R2.json():
                        print('{name}: Success!'.format(name=name))
                        with open('output/posted/{filename}.txt'.format(filename=name), 'w') as g:
                            g.write(page_text)
                    else:
                        print('{name}: FAIL! Error Message: {error}'.format(
                            name=name, error=R2.json()['error']['info']))
                else:
                    print('{name}: FAIL!'.format(name=name))
