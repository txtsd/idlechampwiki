import json
from pprint import pprint
import re
from collections import OrderedDict
import math
from decimal import Decimal
from idlechampaccount import ICAccount
import filecmp
import os


COMPARE = True
REDOWNLOAD = False
POST = False
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

for mon in js_mon:
    if mon['name'] == 'Jarlaxle':
        temp = mon
        js_mon.remove(mon)
        temp['name'] = 'Jarlaxle (Monster)'
        js_mon.append(temp)

taglist = {}
namelist = {}
__js_mon = sorted(js_mon, key=lambda x: x['id'])
type_list = set()

for monster in __js_mon:
    for tag in monster['tags']:
        type_list.add(tag)

# pprint(__js_mon)
# pprint(type_list)

for monster in __js_mon:
    if monster['name'] not in namelist:
        namelist[monster['name']] = {}
        namelist[monster['name']]['variants'] = []
        namelist[monster['name']]['variants'].append({monster['graphic_id']: {}})
        # print(namelist)
        for variant in namelist[monster['name']]['variants']:
            if variant[monster['graphic_id']] == {}:
                for graphic in js_graphic:
                    if graphic['id'] == monster['graphic_id']:
                        _gfx_name = graphic['graphic']
                        gfx_name = re.search('/.*?([^_]*[_\d]*)$', _gfx_name).group(1)
                        gfx_name_bit = re.search('([^/]*)$', _gfx_name).group(1)
                variant[monster['graphic_id']]['name'] = gfx_name
                variant[monster['graphic_id']]['imgname'] = gfx_name_bit
                variant[monster['graphic_id']]['type'] = set()
                variant[monster['graphic_id']]['type'].add(monster['type'])
                variant[monster['graphic_id']]['tags'] = set()
                for tag in monster['tags']:
                    variant[monster['graphic_id']]['tags'].add(tag)
                variant[monster['graphic_id']]['a_id'] = list()
                variant[monster['graphic_id']]['properties'] = list()
                for attack in js_attack:
                    if attack['id'] == monster['attack_id']:
                        atk_name = attack['name']
                variant[monster['graphic_id']]['a_id'].append(atk_name)
                if 'properties' in monster:
                    if 'more_attacks' in monster['properties']:
                        if 'attack_id' in monster['properties']['more_attacks'][0]:
                            for attack in js_attack:
                                if attack['id'] == monster['properties']['more_attacks'][0]['attack_id']:
                                    atk_name = attack['name']
                            variant[monster['graphic_id']]['a_id'].append(atk_name)
                    if 'hits_based_damage' in monster['properties']:
                        if monster['properties']['hits_based_damage'] == True:
                            variant[monster['graphic_id']]['properties'].append('hits_based_damage')
                    if 'passable' in monster['properties']:
                        if monster['properties']['passable'] == False:
                            variant[monster['graphic_id']]['properties'].append('impassable')
                    if 'armor_based_damage' in monster['properties']:
                        if monster['properties']['armor_based_damage'] == True:
                            variant[monster['graphic_id']]['properties'].append('armor_based_damage')
                    if 'die_after_damage_hero' in monster['properties']:
                        if monster['properties']['die_after_damage_hero'] == True:
                            variant[monster['graphic_id']]['properties'].append('die_after_damage_hero')
                    if 'insta_kill' in monster['properties']:
                        if monster['properties']['insta_kill'] == True:
                            variant[monster['graphic_id']]['properties'].append('insta_kill')
                    if 'indestructible' in monster['properties']:
                        if monster['properties']['indestructible'] == True:
                            variant[monster['graphic_id']]['properties'].append('indestructible')
                    if 'dies_at_formation' in monster['properties']:
                        if monster['properties']['dies_at_formation'] == True:
                            variant[monster['graphic_id']]['properties'].append('dies_at_formation')


        # print(namelist[monster['name']])
    elif monster['name'] in namelist:
        namelist[monster['name']]['variants'].append({monster['graphic_id']: {}})
        # print('\t', namelist[monster['name']])
        for variant in namelist[monster['name']]['variants']:
            if variant == {monster['graphic_id']: {}}:
                for graphic in js_graphic:
                    if graphic['id'] == monster['graphic_id']:
                        _gfx_name = graphic['graphic']
                        gfx_name = re.search('/.*?([^_]*[_\d]*)$', _gfx_name).group(1)
                        gfx_name_bit = re.search('([^/]*)$', _gfx_name).group(1)
                variant[monster['graphic_id']]['name'] = gfx_name
                variant[monster['graphic_id']]['imgname'] = gfx_name_bit
                variant[monster['graphic_id']]['type'] = set()
                variant[monster['graphic_id']]['type'].add(monster['type'])
                variant[monster['graphic_id']]['tags'] = set()
                for tag in monster['tags']:
                    variant[monster['graphic_id']]['tags'].add(tag)
                variant[monster['graphic_id']]['a_id'] = list()
                variant[monster['graphic_id']]['properties'] = list()
                for attack in js_attack:
                    if attack['id'] == monster['attack_id']:
                        atk_name = attack['name']
                variant[monster['graphic_id']]['a_id'].append(atk_name)
                if 'properties' in monster:
                    if 'more_attacks' in monster['properties']:
                        if 'attack_id' in monster['properties']['more_attacks'][0]:
                            for attack in js_attack:
                                if attack['id'] == monster['properties']['more_attacks'][0]['attack_id']:
                                    atk_name = attack['name']
                            variant[monster['graphic_id']]['a_id'].append(atk_name)
                    if 'hits_based_damage' in monster['properties']:
                        if monster['properties']['hits_based_damage'] == True:
                            variant[monster['graphic_id']]['properties'].append('hits_based_damage')
                    if 'passable' in monster['properties']:
                        if monster['properties']['passable'] == False:
                            variant[monster['graphic_id']]['properties'].append('impassable')
                    if 'armor_based_damage' in monster['properties']:
                        if monster['properties']['armor_based_damage'] == True:
                            variant[monster['graphic_id']]['properties'].append('armor_based_damage')
                    if 'die_after_damage_hero' in monster['properties']:
                        if monster['properties']['die_after_damage_hero'] == True:
                            variant[monster['graphic_id']]['properties'].append('die_after_damage_hero')
                    if 'insta_kill' in monster['properties']:
                        if monster['properties']['insta_kill'] == True:
                            variant[monster['graphic_id']]['properties'].append('insta_kill')
                    if 'indestructible' in monster['properties']:
                        if monster['properties']['indestructible'] == True:
                            variant[monster['graphic_id']]['properties'].append('indestructible')
                    if 'dies_at_formation' in monster['properties']:
                        if monster['properties']['dies_at_formation'] == True:
                            variant[monster['graphic_id']]['properties'].append('dies_at_formation')
        # print('\t', namelist[monster['name']])

# pprint(namelist)

for name in namelist:
    page_text = '<ul class="hlist">'
    category_list = set()
    for variant in namelist[name]['variants']:
        variant_page = '\n{_infobox}'

        infobox = '<li>' + '\n'

        infobox += ('{{Monster' + '\n')
        item = variant.popitem()[1]
        infobox += ('| name = ' + item['name'] + '\n')
        infobox += ('| imgname = ' + item['imgname'] + '\n')
        infobox += ('| attack_1 = ' + item['a_id'][0] + '\n')
        if len(item['a_id']) > 1:
            infobox += ('| attack_2 = ' + item['a_id'][1] + '\n')
        if len(item['tags']) > 0:
            for enum, tag in enumerate(sorted(item['tags'])):
                infobox += ('| tags' + str(enum + 1) + ' = ' + tag.title() + '\n')
                category_list.add(tag.title())
        if len(item['properties']) > 0:
            for prop in sorted(item['properties']):
                infobox += ('| ' + prop + ' = ' + 'true' + '\n')
                category_list.add(prop)

        infobox += ('}}' + '\n' + '</li>' + '\n')

        # print(infobox)

        page_text += variant_page.format(_infobox=infobox)
    page_text += '</ul>'
    for cat in sorted(category_list):
        page_text += '\n[[Category:{category}]]'.format(category=cat)

    # print(page_text)
    # print('')

    with open('output/{filename}.txt'.format(filename=name), 'w') as f:
        f.write(page_text)

    if COMPARE:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if not os.path.isdir(os.path.join(dir_path, 'output')):
            os.makedirs(os.path.join(dir_path, 'output'))
        main_file = os.path.join(dir_path, 'output/{filename}.txt'.format(filename=name))
        posted_file = os.path.join(dir_path, 'output/posted/{filename}.txt'.format(filename=name))
        try:
            result = filecmp.cmp(main_file, posted_file, shallow=False)
        except FileNotFoundError as e:
            print('{name}: No source found'.format(name=name))
            result = None

        if (result is not None) and (result == True):
            print('{name}: No changes'.format(name=name))
        else:
            print('{name}: Changes detected! <----------'.format(name=name))
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
                        print('{name}: FAIL! Error Message: {error}'.format(name=name, error=R2.json()['error']['info']))
                else:
                    print('{name}: FAIL!'.format(name=name))
