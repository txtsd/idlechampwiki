import json
from pprint import pprint
import re
from collections import OrderedDict
import math
from decimal import Decimal
import html
from idlechampaccount import ICAccount
import subprocess
import filecmp
import os
import requests
import tempfile

COMPARE = True
POST = False
REDOWNLOAD = False
SHOW_CHANGES = False
_summary = None

PRINT_UPGRADES = False
PRINT_TABLE = False
PRINT_MISSING_ROWS = False
PRINT_MULTIPLE_ABILTIES = False
PRINT_REQUIRED_ABILTIES = False

if POST:
    instance = ICAccount()
    instance.login()


# filename = '/home/txtsd/.local/share/Steam/steamapps/common/IdleChampions/IdleDragons_Data/StreamingAssets/downloaded_files/cached_definitions.json'
filename = '/tmp/cached_definitions.json'
if REDOWNLOAD or not os.path.isfile(filename):
    result = requests.get('http://master.idlechampions.com/~idledragons/post.php?call=getdefinitions')
    with open(filename, 'w') as f:
        if result.status_code == 200:
            # text = result.text
            # text = re.sub('\\u00fb', 'û', text)
            # text = re.sub('\\u00a9', '©', text)
            # f.write(text)
            f.write(result.text)
            # f.write(result.text.encode('utf-8').decode('unicode-escape'))

with open(filename) as f:
    file = f.read()

js = json.loads(html.unescape(file))

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
        str_effect = effect['effect']
        _effect = effect['effect'].replace("'", "\'")
        temp = json.loads(_effect)
        effect['effect'] = temp

# pprint(js_upgrade)
# exit()

breakout = 0

for hero in js_hero:
    if not re.search('^E\d', hero['name']):
        champ_str = '''
{{{{Champion
| name = {{{{SUBJECTPAGENAME}}}}{skin}
| class = {class_}
| race = {race}
| age  = {age}
| alignment = {alignment}
| group = {group}
| str={str_} | dex={dex}
| con={con} | int={int_}
| wis={wis} | cha={cha}
| base_cooldown = {b_cd}
| ulti_cooldown = {u_cd}
| swap1 = {swap1}
| swap2 = {swap2}
| swap3 = {swap3}
| swap4 = {swap4}
}}}}
\'\'\'{fullname}\'\'\' is one of the [[champions]] of [[Idle Champions of the Forgotten Realms]].{extra_info}

==Backstory==
{{{{Quote|{backstory}}}}}

==Abilities and Levels==
{abilities}

{wikitable}

== Equipment ==
{equipment}
==Trivia==
{trivia}
==Media==
{media}

{{{{Navbox-Champions}}}}
{{{{Navbox-IdleChampions}}}}

[[Category:Champions]]'''

        # Basic information
        id_ = hero['id']
        # if id_ in [2, 25]:
        #     continue
        name = hero['name']
        skinnames = []
        for skin in js_hero_skin:
            if hero['id'] == skin['hero_id']:
                skinnames.append(skin['name'])
        skin = ''
        if not len(skinnames) == 0:
            for enum, skinname in enumerate(skinnames):
                skin += ('\n' + '| skin' + str(enum + 1) + ' = ' + skinname)
        _class = hero['character_sheet_details']['class']
        _race = hero['character_sheet_details']['race']
        _age = hero['character_sheet_details']['age']
        _alignment = hero['character_sheet_details']['alignment']
        _str = hero['character_sheet_details']['ability_scores']['str']
        _dex = hero['character_sheet_details']['ability_scores']['dex']
        _con = hero['character_sheet_details']['ability_scores']['con']
        _int = hero['character_sheet_details']['ability_scores']['int']
        _wis = hero['character_sheet_details']['ability_scores']['wis']
        _cha = hero['character_sheet_details']['ability_scores']['cha']
        fullname = hero['character_sheet_details']['full_name']
        extra_info = ''
        system_desc = hero['character_sheet_details']['system_description'] if 'system_description' in hero['character_sheet_details'] else ''
        backstory = hero['character_sheet_details']['backstory']

        class_ = '<onlyinclude>{{{{#ifeq:{{{{{{include|class}}}}}}|class|{class__}}}}}</onlyinclude>'.format(
            class__=_class)
        race = '<onlyinclude>{{{{#ifeq:{{{{{{include|race}}}}}}|race|{race}}}}}</onlyinclude>'.format(
            race=_race)
        age = '<onlyinclude>{{{{#ifeq:{{{{{{include|age}}}}}}|age|{age}}}}}</onlyinclude>'.format(
            age=_age)
        alignment = '<onlyinclude>{{{{#ifeq:{{{{{{include|alignment}}}}}}|alignment|{alignment}}}}}</onlyinclude>'.format(
            alignment=_alignment)
        str_ = '<onlyinclude>{{{{#ifeq:{{{{{{include|str}}}}}}|str|{str}}}}}</onlyinclude>'.format(
            str=_str)
        dex = '<onlyinclude>{{{{#ifeq:{{{{{{include|dex}}}}}}|dex|{dex}}}}}</onlyinclude>'.format(
            dex=_dex)
        con = '<onlyinclude>{{{{#ifeq:{{{{{{include|con}}}}}}|con|{con}}}}}</onlyinclude>'.format(
            con=_con)
        int_ = '<onlyinclude>{{{{#ifeq:{{{{{{include|int}}}}}}|int|{int_}}}}}</onlyinclude>'.format(
            int_=_int)
        wis = '<onlyinclude>{{{{#ifeq:{{{{{{include|wis}}}}}}|wis|{wis}}}}}</onlyinclude>'.format(
            wis=_wis)
        cha = '<onlyinclude>{{{{#ifeq:{{{{{{include|cha}}}}}}|cha|{cha}}}}}</onlyinclude>'.format(
            cha=_cha)

        if name == 'Drizzt':
            extra_info = ' He is obtained as reward of the [[Overdue Rendezvous]] [[Variants|Variant]] of the [[Underdeep Cartography]] [[Adventures|Adventure]].'
        elif name == 'Stoki':
            extra_info = ' She is obtained from the [[Highharvestide]] Event.'
        elif name == 'Krond':
            extra_info = ' He is obtained from the [[Liars\' Night]] Event.'
        elif name == 'Gromma':
            extra_info = ' She is obtained from the [[Feast of the Moon]] Event.'
        elif name == 'Dhadius':
            extra_info = ' He is obtained from the [[Simril]] Event.'
        elif name == 'Barrowin':
            extra_info = ' She is obtained from the [[Wintershield]] Event.'
        elif name == 'Regis':
            extra_info = ' He is obtained from the [[Midwinter]] Event.'
        elif name == 'Birdsong':
            extra_info = ' She is obtained from the [[Grand Revel]] Event.'
        elif name == 'Zorbu':
            extra_info = ' He is obtained from the [[Fleetswake]] Event.'
        elif name == 'Strix':
            extra_info = ' She is obtained from the [[Festival of Fools]] Event.'
        elif name == 'Nrakk':
            extra_info = ' He is obtained from the [[Greengrass]] Event.'
        elif name == 'Catti-brie':
            extra_info = ' She is obtained from [[The Running]] Event.'
        elif name == 'Evelyn':
            extra_info = ' She is obtained from [[The Great Modron March]] Event.'
        elif name == 'Binwin':
            extra_info = ' He is obtained from the [[Dragondown]] Event.'
        elif name == 'Deekin':
            extra_info = ' He is obtained from the [[Founder\'s Day]] Event.'
        elif name == 'Diath':
            extra_info = ' He is obtained from the [[Midsummer]] Event.'
        elif name == 'Azaka':
            extra_info = ' She is obtained as reward of the [[Azaka\'s Procession]] [[Variants|Variant]] of the [[Tomb of the Nine Gods]] [[Adventures|Adventure]].'
        elif name == 'Ishi':
            extra_info = ' She is obtained from the [[Ahghairon\'s Day]] Event.'
        elif name == 'Wulfgar':
            extra_info = ' He is obtained from the [[Brightswords]] Event.'
        elif name == 'Farideh':
            extra_info = ' She is obtained from the [[Highharvestide]] Event.'
        elif name == 'Donaar':
            extra_info = ' He is obtained from the [[Liars\' Night]] Event.'
        elif name == 'Vlahnya':
            extra_info = ' She is obtained from the [[Feast of the Moon]] Event.'
        elif name == 'Warden':
            extra_info = ' He is obtained from the [[Simril]] Event.'
        elif name == 'Nerys':
            extra_info = ' She is obtained from the [[Wintershield]] Event.'
        elif name == 'K\'thriss':
            extra_info = ' He is obtained from the [[Midwinter]] Event.'
        elif name == 'Paultin':
            extra_info = ' He is obtained from the [[Grand Revel]] Event.'
        elif name == 'Black Viper':
            extra_info = ' She is obtained from the [[Fleetswake]] Event.'
        elif name == 'Rosie':
            extra_info = ' She is obtained from the [[Festival of Fools]] Event.'
        elif name == 'Aila':
            extra_info = ' She is obtained from the [[Greengrass]] Event.'
        elif name == 'Spurt':
            extra_info = ' He is obtained from [[The Running]] Event.'
        elif name == 'Qillek':
            extra_info = ' He is obtained from [[The Great Modron March]] Event.'
        elif name == 'Korth':
            extra_info = ' He is obtained from the [[Dragondown]] Event.'
        elif name == 'Walnut':
            extra_info = ' She is obtained from the [[Founder\'s Day]] Event.'
        # elif name == 'Walnut':
        #     extra_info = ''

        if not system_desc == '':
            extra_info += '\n\n{system_desc}'.format(system_desc=system_desc)

        # Cost things
        cost_curve = hero['cost_curves']['1']
        health_curve = hero['health_curves']['1']
        base_cost = int(hero['base_cost'])
        base_damage = int(hero['base_damage'])
        base_health = int(hero['base_health'])

        # Group
        _tags = hero['tags']
        if 'companion' in _tags:
            group = 'Companions of the Hall'
        elif 'forcegrey' in _tags:
            group = 'Force Grey'
        elif 'wafflecrew' in _tags:
            group = 'Waffle Crew'
        elif 'cteam' in _tags:
            group = 'Acquisitions Incorporated: The “C” Team'
        elif 'baldursgate' in _tags:
            group = 'Heroes of Baldur\'s Gate'
        elif 'cneoriginal' in _tags:
            group = ''
        elif 'aerois' in _tags:
            group = 'Heroes of Aerois'
        else:
            group = ''

        # Swaps
        _swap = []
        for _hero in js_hero:
            if not re.search('^E\d', _hero['name']):
                if _hero['seat_id'] == hero['seat_id']:
                    if not _hero['id'] == hero['id']:
                        _swap.append(_hero['name'])
        swap1 = _swap[0] if len(_swap) >= 1 else ''
        swap2 = _swap[1] if len(_swap) >= 2 else ''
        swap3 = _swap[2] if len(_swap) >= 3 else ''
        swap4 = _swap[3] if len(_swap) >= 4 else ''

        # Abilities
        if name == 'Minsc':
            abilities = '''
\'\'\'{a_base} - Base Attack\'\'\'

{a_base_desc}
{gained_abilities}
\'\'\'{a_ult} - Ultimate Attack\'\'\'

{a_ult_desc}

===Specialization Choices===

\'\'\'{{{{Spec|{spec_1}}}}}\'\'\'

{spec_desc_1}

\'\'\'{{{{Spec|{spec_2}}}}}\'\'\'

{spec_desc_2}

\'\'\'{{{{Spec|{spec_3}}}}}\'\'\'

{spec_desc_3}

\'\'\'{{{{Spec|{spec_4}}}}}\'\'\'

{spec_desc_4}

\'\'\'{{{{Spec|{spec_5}}}}}\'\'\'

{spec_desc_5}
'''
        elif name == 'Asharra':
            abilities = '''
\'\'\'{a_base} - Base Attack\'\'\'

{a_base_desc}
{gained_abilities}
\'\'\'{a_ult} - Ultimate Attack\'\'\'

{a_ult_desc}

===Specialization Choices===

\'\'\'<u>Specialization Choice 1</u>\'\'\'

\'\'\'{{{{Spec|{spec_1}}}}}\'\'\'

{spec_desc_1}

\'\'\'{{{{Spec|{spec_2}}}}}\'\'\'

{spec_desc_2}

\'\'\'{{{{Spec|{spec_3}}}}}\'\'\'

{spec_desc_3}

\'\'\'<u>Specialization Choice 2</u>\'\'\'

\'\'\'{{{{Spec|{spec_4}}}}}\'\'\'

{spec_desc_4}

\'\'\'{{{{Spec|{spec_5}}}}}\'\'\'

{spec_desc_5}

\'\'\'{{{{Spec|{spec_6}}}}}\'\'\'

{spec_desc_6}
'''
        elif name == 'Tyril':
            abilities = '''
{gained_abilities}
===Specialization Choices===

\'\'\'{{{{Spec|{spec_1}}}}}\'\'\'

{spec_desc_1}

:\'\'\'{a_base_1} - Base Attack\'\'\'

:{a_base_1_desc}
:\'\'\'{a_ult_1} - Ultimate Attack\'\'\'

:{a_ult_1_desc}
\'\'\'{{{{Spec|{spec_2}}}}}\'\'\'

{spec_desc_2}

:\'\'\'{a_base_2} - Base Attack\'\'\'

:{a_base_2_desc}
:\'\'\'{a_ult_2} - Ultimate Attack\'\'\'

:{a_ult_2_desc}

'''
        elif name in [
            'Krond',
            'Gromma',
            'Birdsong',
        ]:
            abilities = '''
\'\'\'{a_base} - Base Attack\'\'\'

{a_base_desc}
{gained_abilities}
\'\'\'{a_ult} - Ultimate Attack\'\'\'

{a_ult_desc}

===Specialization Choice===

\'\'\'{{{{Spec|{spec_1}}}}}\'\'\'

{spec_desc_1}

\'\'\'{{{{Spec|{spec_2}}}}}\'\'\'

{spec_desc_2}

\'\'\'{{{{Spec|{spec_3}}}}}\'\'\'

{spec_desc_3}
'''
        elif name in [
            'Regis',
            'Ishi',
        ]:
            abilities = '''
\'\'\'{a_base} - Base Attack\'\'\'

{a_base_desc}
{gained_abilities}
\'\'\'{a_ult} - Ultimate Attack\'\'\'

{a_ult_desc}

===Specialization Choices===

\'\'\'<u>Specialization Choice 1</u>\'\'\'

\'\'\'{{{{Spec|{spec_1}}}}}\'\'\'

{spec_desc_1}

\'\'\'{{{{Spec|{spec_2}}}}}\'\'\'

{spec_desc_2}

\'\'\'<u>Specialization Choice 2</u>\'\'\'

\'\'\'{{{{Spec|{spec_3}}}}}\'\'\'

{spec_desc_3}

\'\'\'{{{{Spec|{spec_4}}}}}\'\'\'

{spec_desc_4}

\'\'\'{{{{Spec|{spec_5}}}}}\'\'\'

{spec_desc_5}
'''
        elif name == 'Zorbu':
            abilities = '''
\'\'\'{a_base} - Base Attack\'\'\'

{a_base_desc}
{gained_abilities}
\'\'\'{a_ult} - Ultimate Attack\'\'\'

{a_ult_desc}

===Specialization Choices===

\'\'\'<u>Specialization Choice 1</u>\'\'\'

\'\'\'{{{{Spec|{spec_1}}}}}\'\'\'

{spec_desc_1}

\'\'\'{{{{Spec|{spec_2}}}}}\'\'\'

{spec_desc_2}

\'\'\'{{{{Spec|{spec_3}}}}}\'\'\'

{spec_desc_3}

\'\'\'{{{{Spec|{spec_4}}}}}\'\'\'

{spec_desc_4}

\'\'\'{{{{Spec|{spec_5}}}}}\'\'\'

{spec_desc_5}

\'\'\'<u>Specialization Choice 2</u>\'\'\'

\'\'\'{{{{Spec|{spec_6}}}}}\'\'\'

{spec_desc_6}

\'\'\'{{{{Spec|{spec_7}}}}}\'\'\'

{spec_desc_7}
'''
        elif name == 'Wulfgar':
            abilities = '''
\'\'\'{a_base} - Base Attack\'\'\'

{a_base_desc}
{gained_abilities}
\'\'\'{a_ult} - Ultimate Attack\'\'\'

{a_ult_desc}

===Specialization Choices===

\'\'\'{{{{Spec|{spec_1}}}}}\'\'\'

{spec_desc_1}

\'\'\'{{{{Spec|{spec_2}}}}}\'\'\'

{spec_desc_2}

\'\'\'{{{{Spec|{spec_3}}}}}\'\'\'

{spec_desc_3}
'''
        elif name == 'Walnut':
            abilities = '''
\'\'\'{a_base} - Base Attack\'\'\'

{a_base_desc}
{gained_abilities}
\'\'\'{a_ult} - Ultimate Attack\'\'\'

{a_ult_desc}

===Specialization Choices===

\'\'\'<u>Specialization Choice 1</u>\'\'\'

\'\'\'{{{{Spec|{spec_1}}}}}\'\'\'

{spec_desc_1}

\'\'\'{{{{Spec|{spec_2}}}}}\'\'\'

{spec_desc_2}

\'\'\'{{{{Spec|{spec_3}}}}}\'\'\'

{spec_desc_3}

\'\'\'<u>Specialization Choice 2</u>\'\'\'

\'\'\'{{{{Spec|{spec_4}}}}}\'\'\'

{spec_desc_4}

\'\'\'{{{{Spec|{spec_5}}}}}\'\'\'

{spec_desc_5}
'''
        else:
            abilities = '''
\'\'\'{a_base} - Base Attack\'\'\'

{a_base_desc}
{gained_abilities}
\'\'\'{a_ult} - Ultimate Attack\'\'\'

{a_ult_desc}

\'\'\'<u>Specialization Choice</u>\'\'\'

\'\'\'{{{{Spec|{spec_1}}}}}\'\'\'

{spec_desc_1}

\'\'\'{{{{Spec|{spec_2}}}}}\'\'\'

{spec_desc_2}
'''
        # Base & Ult Attacks and Cooldowns
        _b_a_id = hero['base_attack_id']
        _u_a_id = hero['ultimate_attack_id']

        for attack in js_attack:
            # Tyril special case base attack and ultimate
            if name == 'Tyril':
                if attack['id'] == _b_a_id:
                    a_base_1 = attack['name']
                    a_base_1_desc = attack['description']
                if attack['id'] == _u_a_id:
                    a_ult_1 = attack['name']
                    a_ult_1_desc = attack['description']
                    if ('long_description' in attack) and not (attack['long_description'] == ''):
                        a_ult_1_desc = attack['long_description']
                if attack['id'] == 32:
                    a_base_2 = attack['name']
                    a_base_2_desc = attack['description']
                if attack['id'] == 27:
                    a_ult_2 = attack['name']
                    a_ult_2_desc = attack['description']
                    if ('long_description' in attack) and not (attack['long_description'] == ''):
                        a_ult_2_desc = attack['long_description']
            if attack['id'] == _b_a_id:
                _b_cd = attack['cooldown']
                b_cd = '<onlyinclude>{{{{#ifeq:{{{{{{include|base_cd}}}}}}|base_cd|{base_cd}}}}}</onlyinclude>'.format(
                    base_cd=_b_cd)
                a_base = attack['name']
                a_base_desc = attack['description'].replace('$attack_num_targets', str(attack['num_targets']))
                if attack['id'] == 134:
                    a_base_desc = a_base_desc\
                        .replace('$stun_chance', str(attack['animations'][0]['stun_chance']))\
                        .replace('$stun_time', str(attack['animations'][0]['stun_on_hit']))
                if ('long_description' in attack) and not (attack['long_description'] == ''):
                    if attack['id'] == 139:
                        a_base_desc += '\n'
                        a_base_desc += '* '
                        a_base_desc += attack['long_description']
                        a_base_desc = a_base_desc\
                            .replace('$(attack_indexed_effect_amount 0)', attack['animations'][0]['effects_on_monsters'][0]['effect_string'].split(',')[1])\
                            .replace('$(attack_indexed_effect_amount 1)', attack['animations'][0]['effects_on_monsters'][1]['effect_string'].split(',')[1])\
                            .replace('$(attack_indexed_effect_amount 2)', attack['animations'][0]['effects_on_monsters'][2]['effect_string'].split(',')[1])\
                            .replace('$(attack_indexed_effect_amount 3)', attack['animations'][0]['effects_on_monsters'][3]['effect_string'].split(',')[1])\
                            .replace(';', '\n* ')
                    else:
                        a_base_desc = attack['long_description']
            elif attack['id'] == _u_a_id:
                _u_cd = attack['cooldown']
                u_cd = '<onlyinclude>{{{{#ifeq:{{{{{{include|ult_cd}}}}}}|ult_cd|{ult_cd}}}}}</onlyinclude>'.format(
                    ult_cd=_u_cd)
                a_ult = attack['name']
                a_ult_desc = attack['description'].replace('$ishi_ult_time', '15').replace('$(nrakk_ult_buffed 200)', '200')
                if ('long_description' in attack) and not (attack['long_description'] == ''):
                    a_ult_desc = attack['long_description'].replace('$ishi_ult_time', '15').replace('$(nrakk_ult_buffed 200)', '200')
            # Gromma's ult id is wrong
            if name == 'Gromma':
                if attack['id'] == 59:
                    a_ult = attack['name']
                    a_ult_desc = attack['long_description']

        # Another go at the table
        # __upgrades = OrderedDict()
        __upgrades = []
        _upgrades = []
        ab_table = {}
        for upgrade in js_upgrade:
            if upgrade['hero_id'] == id_:
                __upgrades.append(upgrade)

        __upgrades = sorted(__upgrades, key=lambda x: x['required_level'])
        if PRINT_UPGRADES is True:
            pprint(__upgrades)

        for upgrade in js_upgrade:
            _upgrades.append(upgrade)
        _upgrades = sorted(_upgrades, key=lambda x: x['required_level'])

        if PRINT_MULTIPLE_ABILTIES is True:
            req_level_thing = {}
            print(name, 'PRINT_MULTIPLE_ABILTIES')
            for upgrade in __upgrades:
                if not upgrade['required_level'] == 9999:
                    # if not 'specialization_name' in upgrade:
                    if isinstance(req_level_thing, list):
                        temp = {}
                        temp['level'] = upgrade['required_level']
                        temp['req_id'] = upgrade['required_upgrade_id']
                        temp['full'] = upgrade
                        req_level_thing.append(temp)
                    elif not 'level' in req_level_thing:
                        req_level_thing['level'] = upgrade['required_level']
                        req_level_thing['req_id'] = upgrade['required_upgrade_id']
                        req_level_thing['full'] = upgrade
                    else:
                        temp = req_level_thing
                        req_level_thing = []
                        req_level_thing.append(temp)
                        temp2 = {}
                        temp2['level'] = upgrade['required_level']
                        temp2['req_id'] = upgrade['required_upgrade_id']
                        temp2['full'] = upgrade
                        req_level_thing.append(temp2)

            prev_item = {'level': 0}
            for item in req_level_thing:
                if item['level'] == prev_item['level']:
                    print(item['full'])
                    print(prev_item['full'])
                prev_item = item
            # pprint(req_level_thing)

        if PRINT_REQUIRED_ABILTIES is True:
            required_thing = {}
            print(name, 'PRINT_REQUIRED_ABILTIES')
            for upgrade in __upgrades:
                if not upgrade['required_level'] == 9999:
                    if not upgrade['required_upgrade_id'] == 0:
                        if isinstance(required_thing, list):
                            temp = {}
                            temp['level'] = upgrade['required_level']
                            temp['req_id'] = upgrade['required_upgrade_id']
                            temp['full'] = upgrade
                            required_thing.append(temp)
                        elif not 'level' in required_thing:
                            required_thing['level'] = upgrade['required_level']
                            required_thing['req_id'] = upgrade['required_upgrade_id']
                            required_thing['full'] = upgrade
                        else:
                            temp = required_thing
                            required_thing = []
                            required_thing.append(temp)
                            temp2 = {}
                            temp2['level'] = upgrade['required_level']
                            temp2['req_id'] = upgrade['required_upgrade_id']
                            temp2['full'] = upgrade
                            required_thing.append(temp2)
                        print('PRINT_REQUIRED_ABILTIES', upgrade)

            # for item in required_thing:
            #     print(item['full'])

        def parse_description(desc):
            pass

        def parse_effect(effect):
            if isinstance(effect, dict):
                # effect_key = effect['effect_string'].split(',')[0]
                # effect_id = effect['effect_string'].split(',')[2]
                # print('dict', effect)
                effect_desc = effect['description']
                effect = effect['effect_string']
            if isinstance(effect, str):
                # print(effect)
                if len(effect.split(',')) == 1:
                    effect_key = effect
                if len(effect.split(',')) == 2:
                    # print('2', effect)
                    effect_key = effect.split(',')[0]
                    effect_id = effect.split(',')[1]
                elif len(effect.split(',')) == 3:
                    # print('3', effect)
                    effect_key = effect.split(',')[0]
                    effect_amount = effect.split(',')[1]
                    effect_id = effect.split(',')[2]
                elif len(effect.split(',')) > 3:
                    # print('>3', effect)
                    effect_key = effect.split(',')[0]
                    effect_ids = []
                    if effect_key in [
                        'buff_upgrades',
                        'buff_attacks_damage',  # found while doing equipment
                        'hero_dps_multiplier_if_attack',  # found while doing equipment
                    ]:
                        effect_amount = effect.split(',')[1]
                        for __id in effect.split(',', 2)[2].split(','):
                            effect_ids.append(__id)
                    elif effect_key == 'buff_upgrade':
                        # print(effect)
                        effect_amount = effect.split(',')[1]
                        # print(effect.split(',', 2)[2].split(',')[0])
                        effect_id = effect.split(',', 2)[2].split(',')[0]
                        # print(effect.split(',', 2)[2].split(',')[1])
                        effect_extra = effect.split(',', 2)[2].split(',')[1]
                    elif effect_key == 'effect_def':
                        for __id in effect.split(',', 1)[1].split(','):
                            effect_ids.append(__id)
                    elif effect_key == 'buff_upgrade_per_any_tagged_crusader_mult':  # Bruenor
                        effect_amount = effect.split(',')[1]
                        effect_id = effect.split(',')[2]
                        effect_extra = effect.split(',')[3]
                    elif effect_key == 'targets_with_tag_gold_multiplier_mult':  # Ishi
                        effect_amount = effect.split(',')[1]
                        effect_extra = effect_rest = effect.split(',', 1)[1]
                    elif effect_key == 'buff_upgrade_by_tag_mult':  # Diath
                        effect_amount = effect.split(',')[1]
                        effect_id = effect.split(',')[3]
                    elif effect_key in [
                        'hero_dps_mult_per_crusader_where_mult',  # Rosie
                        'change_base_attack_every',  # Rosie
                    ]:
                        effect_id = effect.split(',')[1]  # Actually amount
                    else:
                        effect_rest = effect.split(',', 1)[1]
                    # print(effect.split(',', 2))
                    # print(effect_ids)

            else:
                print('uh')
                exit()
            if effect_key == 'effect_def':
                if len(effect.split(',')) < 3:
                    for effect in js_effect:
                        if str(effect['id']) == effect_id:
                            desc = effect['description']
                            if 'buff_upgrade_per_any_tagged_crusader_mult' in effect['effect_keys'][0]['effect_string']:
                                __effect = parse_effect(effect['effect_keys'][0]['effect_string'])
                                # print(__effect)
                            if any(
                                y in desc for y in [
                                    '$amount%',
                                    '$(amount)%',
                                    '$chance%',
                                    '$percent%',
                                ]
                            ):
                                unit = '%'
                            elif any(
                                y in desc for y in [
                                    '$amount seconds',
                                    '$(amount) seconds',
                                ]
                            ):
                                unit = ' sec'

                            for __effect in effect['effect_keys']:
                                # print(effect)
                                # print(__effect['effect_string'])
                                _effect = parse_effect(__effect['effect_string'])
                                if not _effect:
                                    # _effect = []
                                    continue
                                # print(_effect['amount'])
                                # print(desc)
                                if _effect['key'] == 'grant_temporary_hp_with_cooldown':
                                    desc = desc\
                                        .replace('$(tmp_hp_cooldown cooldown)', _effect['cooldown'])\
                                        .replace('$optional_percent_limit', _effect['percent'])
                                if _effect['key'] == 'add_health_plus_tag_targets_percent_health':
                                    desc = desc\
                                        .replace('$percent', _effect['percent'])
                                if _effect['key'] == 'bonus_damage_range':
                                    desc = desc\
                                        .replace('$min_amount', _effect['min_amount'])\
                                        .replace('$damage_type', _effect['damage_type'])
                                if _effect['key'] == 'hero_dps_mult_by_tag_additive':
                                    desc = desc\
                                        .replace('$(amount___2)', _effect['amount'])
                                if _effect['key'] == 'revive_with_health_transfer':
                                    desc = desc\
                                        .replace('$gain_percent', _effect['gain_percent'])\
                                        .replace('$lose_percent', _effect['lose_percent'])\
                                        .replace('$wait_time', _effect['wait_time'])
                                if _effect['key'] == 'increase_attack_cooldown':
                                    desc = desc\
                                        .replace('$(seconds_plural amount)', _effect['amount'])\
                                        .replace('$(amount___2)', _effect['amount___2'])
                                if _effect['key'] == 'stun_does_cooldown_and_damage_mult':
                                    desc = desc\
                                        .replace('$cooldown', _effect['cooldown'])
                                if _effect['key'] == 'azaka_weretiger':
                                    desc = desc\
                                        .replace('$azaka_attacks', _effect['azaka_attacks'])\
                                        .replace('$azaka_time', _effect['azaka_time'])
                                if _effect['key'] == 'buff_attack_monster_effects_index':
                                    desc = desc\
                                        .replace('$amount___' + _effect['index'], _effect['amount'])
                                if _effect['key'] == 'gold_multiplier_reduce':
                                    desc = desc\
                                        .replace('$amount___2', _effect['amount'])
                                if _effect['key'] == 'monster_effect_on_attacked':
                                    desc = desc\
                                        .replace('$(time_str amount)', _effect['amount'] + ' second')
                                if _effect['key'] == 'bonus_damage_monster_percent_from_party_range':
                                    desc = desc\
                                        .replace('$start_percent', _effect['start'])\
                                        .replace('$end_percent', _effect['end'])
                                if _effect['key'] == 'add_percent_targets_max_health':
                                    desc = desc\
                                        .replace('$(targets_desc_plural targets)', _effect['targets'] + name)
                                if _effect['key'] == 'overwhelm_start_increase':
                                    desc = desc\
                                        .replace('$amount___2', _effect['amount'])
                                if _effect['key'] == 'hero_dps_multiplier_reduced_by_age':
                                    desc = desc\
                                        .replace('$reduce', _effect['reduce'])\
                                        .replace('$every_years', _effect['every_years'])\
                                        .replace('$(start_years)', _effect['start_years'])\
                                        .replace('$min', _effect['min'])
                                if _effect['key'] == 'buff_upgrade_by_target_tag_mult':
                                    desc = desc\
                                        .replace('$(not_buffed amount___2)', _effect['amount'])
                                if effect['id'] == 141:
                                    desc = desc\
                                        .replace('$seconds', str(__effect['seconds']))\
                                        .replace('$hits', str(__effect['hits']))\
                                        .replace('$(value stun_time)', str(__effect['stun_time']))
                                if _effect['key'] == 'binwin_multi_attack':
                                    desc = desc\
                                        .replace('$(binwin_odds_buff base_odds)', _effect['base_odds'])\
                                        .replace('$cooldown_added', _effect['cooldown_added'])\
                                        .replace('$reduce_odds', _effect['reduce_odds'])
                                if effect['id'] == 165:
                                    desc = desc\
                                        .replace('$upgrade_base_stack', _effect['amount'])
                                if effect['id'] == 226:
                                    if 'for_time' in __effect:
                                        desc = desc\
                                            .replace('$for_time', str(__effect['for_time']))
                                if _effect['key'] == 'buff_upgrade_per_stunned_enemy':
                                    desc = desc\
                                        .replace('$cap_percent', _effect['cap_percent'])
                                if effect['id'] == 204 or effect['id'] == 203:
                                    # Could be a bug that description only uses 1 $amount var
                                    if 'monster_effect' in __effect:
                                        desc = desc\
                                            .replace('$amount___2', _effect['amount'])
                                if _effect['key'] == 'add_attack_stun':
                                    desc = desc\
                                        .replace('$duration', _effect['duration'])\
                                        .replace('$(attack_names_and optional_attack_ids)', _effect['name'])
                                if effect['id'] == 233:
                                    if 'monster_effect_time' in __effect:
                                        desc = desc\
                                            .replace('$(monster_effect_time___2)', str(__effect['monster_effect_time']))
                                if _effect['key'] == 'reduce_attack_cooldown_per_any_tagged_crusader':
                                    desc = desc\
                                        .replace('$(seconds_plural amount___2)', _effect['amount'] + ' seconds')
                                if _effect['key'] in ['chance_add_attack_targets', 'chance_attack_adds_dot']:
                                    desc = desc\
                                        .replace('$chance', _effect['chance'])
                                if effect['id'] == 351:
                                    desc = desc\
                                        .replace('$kill_count', _effect['kill_count'])\
                                        .replace('$time', _effect['time'])\
                                        .replace('$(if spurt_is_spirit)^^(', '. \'\'')\
                                        .replace(')$fi$(only_when_purchased)^^Current Wasp Swarm Kills: $spurt_wasp_kills', '\'\'')
                                if effect['id'] == 342:
                                    desc = desc\
                                        .replace('$(if spurt_is_spirit)^^(', '. \'\'')\
                                        .replace('$fi', '\'\'')
                                if effect['id'] == 345:
                                    desc = desc\
                                        .replace('$(if spurt_is_spirit)^^(', '. \'\'')\
                                        .replace('$fi', '\'\'')
                                desc = desc.replace('$amount___2', '$interim___2')
                                if effect['id'] == 360:
                                    desc = desc\
                                        .replace('$increase_by_slot', _effect['amount'])
                                if effect['id'] == 361:
                                    desc = desc\
                                        .replace(' $(if upgrade_purchased 2318)Champions exactly two slots away from Qillek provide twice the bonus each.', '')
                                if effect['id'] == 369:
                                    desc = desc\
                                        .replace('$cooldown_buff', _effect['amount'])
                                if effect['id'] == 371:
                                    desc = desc\
                                        .replace('$fighting_spirit_cooldown', _effect['amount'])
                                if effect['id'] == 370:
                                    desc = desc\
                                        .replace('$calculated_stack_time', _effect['time'])
                                if effect['id'] == 373:
                                    desc = desc\
                                        .replace('$charges', _effect['amount'])\
                                        .replace('$(time_str charge_timer)', _effect['timer'] + ' seconds')
                                if effect['id'] == 372:
                                    desc = desc\
                                        .replace('$chance', _effect['chance'])\
                                        .replace('$ult_reduce_seconds', _effect['ult_reduce'])
                                if effect['id'] == 376:
                                    desc = desc\
                                        .replace('$(if upgrade_purchased 2393)all Champions$(elif upgrade_purchased 2392)adjacent champions and champions in the top or bottom of their column$(elif upgrade_purchased 2391)champions up to two slots away$(or)', '')\
                                        .replace('$(not_buffed amount)', _effect['amount'])
                                if effect['id'] == 377:
                                    desc = desc\
                                        .replace('$(duration)', _effect['duration'])\
                                        .replace('$duration', _effect['duration'])
                                if effect['id'] == 378:
                                    desc = desc\
                                        .replace('$(round amount)', _effect['amount'])
                                desc = desc.replace('$amount___2', '$interim___2')
                                desc = desc\
                                    .replace('$amount', _effect['amount'])\
                                    .replace('$(amount)', _effect['amount'])\
                                    .replace('$(not_buffed amount)', _effect['amount'])\
                                    .replace('%%', '%')
                                desc = desc.replace('$interim___2', '$amount___2')
                                # print(desc)
                            if _effect:
                                desc = desc\
                                    .replace(' \r\n\r\nAila\'s Contibution: $(aila_synergy)%\r\nTotal Aerois Synergy Pool: $(aerois_synergy)%', '')\
                                    .replace('  \r\n\r\nQillek\'s Contibution: $(qillek_synergy)%\r\nTotal Aerois Synergy Pool: $(aerois_synergy)%', '')\
                                    .replace('$(if upgrade_purchased 1550) or Champions within 2 slots distance of $target$(elif upgrade_purchased 1548) or Champions adjacent to $target', '')\
                                    .replace('$(describe_rarity rarity)', 'Epic')\
                                    .replace('$(tmp_hp_cooldown cooldown)', '10')\
                                    .replace('$optional_percent_limit', '200')\
                                    .replace('$only_when_purchased (Current Attackers: $num_attacking_monsters)', '')\
                                    .replace('$asharra_kir_sabal_desc', '')\
                                    .replace('Bruenor_hero', 'Bruenor')\
                                    .replace('$(if upgrade_purchased 1897). Hex is spread to nearby enemies when a Hex cursed enemy is killed.$(fi)', '')\
                                    .replace('$(if upgrade_purchased 1897). Hex is spread to nearby enemies when a Hex cursed enemy is killed.$(fi)', '')\
                                    .replace('. (multiplicative, then buffed by $(upgrade_bonus 2037)%)', ' (multiplicative).')\
                                    .replace('$(if upgrade_purchased 1192)or anyone kills an enemy affected by Silver Lining $(fi)', '')\
                                    .replace('$(if upgrade_purchased 2329) ($(mult_value chance 2)% chance for Champions not adjacent to Korth)$fi', '')\
                                    .replace('$only_when_purchased^^$korth_resurrection_charges', '')\
                                    .replace('$(if upgrade_purchased 2112)33$(or)', '')\
                                    .replace('$(if upgrade_purchased 2112)12.5$(or)', '')\
                                    .replace(' $jewel_thief_description', '')\
                                    .replace('$(if upgrade_purchased 2111)or second $(fi)', '')\
                                    .replace('$(if upgrade_purchased 2111)Black Viper attacks 0.5s faster after she Sneak Attacks.$(fi)', '')\
                                    .replace('$(if jewel_thief_upgrade_unlocked 0)Warlocks, Rangers, $(fi)', '')\
                                    .replace('$(if jewel_thief_upgrade_unlocked 1)200$(or)', '')\
                                    .replace('$(if jewel_thief_upgrade_unlocked 1)10$(or)', '')\
                                    .replace('$(if upgrade_purchased 2153)fourth$(or)', '')\
                                    .replace(' $hordesperson_description', '')\
                                    .replace('$weretiger_description', '')\
                                    .replace('$(if not upgrade_purchased 1152)Adjacent$(or)All$(fi)', 'Adjacent')\
                                    .replace('$only_when_purchased^(Current Stacks: $upgrade_stacks)', '')\
                                    .replace('$only_when_purchased^^Current Stacks: $upgrade_stacks', '')\
                                    .replace('$only_when_purchased^^(Current Bounty of the Hall: $companion_bounty_pool%)', '')\
                                    .replace('$(fi)', '')\
                                    .replace('$target', name)\
                                    .replace('$(target)', name)\
                                    .replace('$source_hero', name)\
                                    .replace('$source', name)\
                                    .replace('$first_effect_key_target', name)\
                                    .replace('$(upgrade_hero id)', name)\
                                    .replace('$(upgrade_name id)', _effect['name'] if ('_effect' in locals() and 'name' in _effect) else '')
                                # print(desc)
                                return {
                                    'desc': desc,
                                    'key': effect_key,
                                    'id': effect_id,
                                    'unit': unit if 'unit' in locals() else ''
                                }
                else:
                    # print('more effects than expected')
                    if effect_key == 'effect_def':  # Vlahnya
                        return {
                            'key': effect_key,
                            'ids': effect.split(',', 1)[1],
                        }
                    # exit()
            elif effect_key == 'set_ultimate_attack':
                for attack in js_attack:
                    if str(attack['id']) == effect_id:
                        desc = attack['description']
                        name_ = attack['name']
                        return {
                            'name': name_,
                            'desc': desc,
                            'key': effect_key,
                            'id': effect_id,
                            'amount': '',
                        }
            elif effect_key in [
                'hero_dps_multiplier_mult',
                'global_dps_multiplier_mult',
                'buff_ultimate',
                'health_add',
                'gold_multiplier_mult',
                'temporary_hp_cooldown_reduce',  # Calliope not handled yet
                # 'add_attack_targets',  # Asharra
                'owner_killing_blow_gold_bonus',  # Makos
                'increase_aoe_radius',  # Nrakk
                'increase_stun_time',  # Nrakk
                # 'increase_num_unique_hits',  # Binwin
                'reduce_hordesperson_drops',  # K'thriss
                # 'storm_aura_shielding_storm',  # Aila
                'reduce_ultimate_cooldown',  # found while doing equipment
                'health_mult',  # found while doing equipment
                'buff_nrakk_ultimate',  # found while doing equipment
                'buff_ishi_ultimate_time',  # found while doing equipment
                'increase_health_by_source_percent',  # Evelyn
                'increase_monster_spawn_time_mult',  # Deekin
                'return_source_dps_when_hit',  # Farideh
                'heal',  # Donaar, Celeste
                'gold_multiplier_reduce',  # K'thriss
                'increase_armored_damage',  # Wulfgar
                'stunned_monster_extra_gold',  # Wulfgar
                'increase_damage_when_monster_stunned',  # Wulfgar
                'heal_most_damaged',  # Nerys
                'buff_incoming_formation_abilities',  # Black Viper
                'add_hit_effect_to_source',  # Black Viper
                'hero_dps_mult_per_crusader_where_mult',  # Rosie
                'change_base_attack_every',  # Rosie
                'attacking_monsters_global_dps_mult',  # Nayeli
                'asharra_take_flight',  # Asharra
                'dhadius_stacking_damage_buff',  # Dhadius
                'buff_dhadius_chance_same_orb',  # Dhadius
                'bonus_damage_when_monster_damaged',  # Zorbu
                'bonus_damage_when_monster_attacking',  # Zorbu
                'global_dps_multiplier_per_dead_champion_additive',  # Strix
                'add_ally_effective_heal_effects',  # Evelyn
                'buff_azaka_weretiger_time_reduce',  # Azaka
                'reduce_azaka_weretiger_attacks',  # Azaka
                'increase_ultimate_cooldown',  # Spurt
                'time_scale',
                'increase_damage_against_korth_marked',  # Korth
                'lizardfolk_tactics_additional_cooldown_reduction',  # Korth
                'rapid_strike_chance_buff',  # Korth
                'bruenor_bounty_contribution',  # Bruenor
                'hero_dps_mult_per_mark_of_ki',  # Stoki
            ]:
                return {
                    'key': effect_key,
                    'amount': effect_id
                }
            elif effect_key == 'add_attack_targets':  # Asharra
                for ___effect in js_effect_key:
                    if ___effect['key'] == 'add_attack_targets':
                        desc = ___effect['descriptions']['desc']
                if len(effect.split(',')) == 3:
                    _amount = effect_amount
                    optional_attack_id = effect.split(',')[2]
                else:
                    _amount = effect_id
                return {
                    'key': effect_key,
                    'amount': _amount,
                    'desc': desc,
                }
            elif effect_key in [
                'buff_upgrade',
                'buff_crit_chance',
                'buff_upgrade_base_stack',
                'reduce_upgrade_every_num_attacks',  # Rosie
            ]:
                for upgrade in __upgrades:
                    if str(upgrade['id']) == effect_id:
                        name_ = upgrade['name']
                        return {
                            'name': name_,
                            'key': effect_key,
                            'id': effect_id,
                            'amount': effect_amount + '%'
                        }
            elif effect_key == 'buff_upgrades':
                # for upgrade in __upgrades:
                #     desc = effect['desc']
                #     if str(upgrade['id']) == effect_id:
                #         # name_ = upgrade['name']
                #         desc = effect_desc
                return {
                    'desc': effect_desc if 'effect_desc' in locals() else None,  # Regis doesn't have upgrade desc
                    'ids': effect_ids,
                    'key': effect_key,
                    'amount': effect_amount
                }
            elif effect_key == 'add_attack_nearby_targets':  # Not handled
                return {
                    'key': effect_key,
                    'targets': '+' + effect.split(',')[1],
                    'amount': effect.split(',')[2] + '%'
                }
            elif effect_key in [
                'reduce_overwhelm_effect',  # Gromma
                'buff_binwin_multi_attack_chance',  # Binwin
                'increase_num_unique_hits',  # Binwin
            ]:
                for _effect in js_effect_key:
                    if _effect['key'] == effect_key:
                        desc = _effect['descriptions']['desc']
                if effect_key in [
                    'reduce_overwhelm_effect',  # Gromma
                    'buff_binwin_multi_attack_chance',  # Binwin
                ]:
                    _amount = effect.split(',')[1] + '%'
                    desc = desc.replace('$amount', effect.split(',')[1])
                    desc = desc.replace('$target', name)
                elif effect_key in [
                    'increase_num_unique_hits',  # Binwin
                ]:
                    desc = desc.replace('$(as_multiplier amount)', str(
                        int(int(effect.split(',')[1]) / 100) + 1))
                    _amount = '+' + effect.split(',')[1]
                elif effect_key in [
                    'reduce_upgrade_every_num_attacks',  # Rosie
                ]:
                    _amount = '-' + effect.split(',')[1]
                return {
                    # 'name': upgrade['name'],
                    'key': effect_key,
                    'amount': _amount,
                    'desc': desc,
                }
            elif effect_key == 'attack_crit_chance':
                for _effect in js_effect_key:
                    if _effect['key'] == effect_key:
                        desc = _effect['descriptions']['desc']
                desc = desc\
                    .replace('$source', name)\
                    .replace('$(buffed_crit_chance chance)', effect.split(',')[2])\
                    .replace('$amount', effect.split(',')[1])
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'chance': effect.split(',')[2],
                    'upgrade_id': effect.split(',')[3],
                    'desc': desc,
                }
            elif effect_key == 'add_sneak_attack_hit':  # Black Viper
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'desc': effect_desc,
                }
            elif effect_key in ['aila_storm_aura']:  # Aila
                return {
                    'key': effect_key,
                    'amount': effect_amount,
                    'cooldown': effect_id,
                }
            elif effect_key in ['storm_aura_storm_soul']:  # Aila
                # print(effect)
                return {
                    'key': effect_key,
                    'amount': effect_id,
                }
            elif effect_key == 'storm_aura_raging_storm':  # Aila
                for _effect in js_effect_key:
                    if _effect['key'] == effect_key:
                        desc = _effect['descriptions']['desc']
                return {
                    'key': effect_key,
                    'radius': effect_amount,
                    'amount': effect_id,
                    'desc': desc,
                }
            elif effect_key == 'storm_aura_shielding_storm':  # Aila
                for _effect in js_effect_key:
                    if _effect['key'] == effect_key:
                        desc = _effect['descriptions']['desc']
                return {
                    'key': effect_key,
                    'amount': effect_id,
                    'desc': desc,
                }
            elif effect_key == 'reduce_storm_aura_seconds':  # Aila
                for _effect in js_effect_key:
                    if _effect['key'] == effect_key:
                        desc = _effect['descriptions']['desc']
                return {
                    'key': effect_key,
                    'amount': effect_id,
                    'desc': desc
                }
            elif effect_key == 'buff_aila_ult_bonus_dmg':  # Aila
                for _effect in js_effect_key:
                    if _effect['key'] == effect_key:
                        desc = _effect['descriptions']['desc']
                return {
                    'key': effect_key,
                    'amount': effect_id,
                    'desc': desc
                }
            elif effect_key in [
                'buff_chance_attack_miss',  # Diath
                'buff_attack_stun_chance',
                'global_dps_mult_by_tag_mult',  # Deekin
                'global_dps_multiplier_mult_area_tags',  # Azaka
                'hero_dps_mult_per_tagged_crusader',  # Ishi
                'hero_dps_mult_per_tagged_crusader_mult',  # Farideh
                'buff_stunned_monster_crit_chance',  # Wulfgar
                'increase_monster_effect_limit_max',  # Warden
                'increase_monster_with_tags_damage',  # Nerys
                'gold_mult_per_target_crusader',  # Paultin
                'hero_dps_mult_per_target_crusader',  # Paultin
                'hero_dps_mult_per_tagged_crusader_mult_amount_before',  # Paultin
                # 'buff_upgrade',  # Paultin
                'reduce_attack_cooldown_per_any_tagged_crusader',  # Rosie
                'increase_monster_damage_if_affected_by',  # Gromma
                'single_target_damage_buff',  # Minsc
                'single_hit_attacks_again',  # Nrakk
                'add_crit_effect',  # Catti-brie
            ]:
                return {
                    'key': effect_key,
                    'amount': effect_amount,
                    'attack_id': effect_id,
                    # 'desc': desc,
                }
            elif effect_key in [
                'buff_attacks_damage',  # found while doing equipment
                'hero_dps_multiplier_if_attack',  # found while doing equipment
                'targets_with_tag_gold_multiplier_mult',  # Ishi
            ]:
                # print(effect)
                return {
                    'key': effect_key,
                    'amount': effect_amount,
                    'ids': effect_ids,
                    # 'desc': desc,
                }
            elif effect_key in [
                'buff_upgrade_per_any_tagged_crusader_mult',  # Bruenor
                'buff_upgrade_per_attacking_monster',  # Evelyn
                'reduce_upgrade_every_num_attacks',  # Rosie
            ]:
                for upgrade in __upgrades:
                    if upgrade['id'] == int(effect_id):
                        _name = upgrade['name']
                return {
                    'key': effect_key,
                    'amount': effect_amount,
                    'id': effect_id,
                    'name': _name,
                }
            elif effect_key in [
                'buff_upgrade_by_tag_mult',  # Diath
            ]:
                for upgrade in __upgrades:
                    if upgrade['id'] == int(effect_id):
                        _name = upgrade['name']
                return {
                    'key': effect_key,
                    'amount': effect_amount,
                    'id': effect_id,
                    'name': _name,
                }
            elif effect_key == 'hero_dps_multiplier_reduced_by_age':  # Gromma
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'reduce': effect.split(',')[2],
                    'start_years': effect.split(',')[3],
                    'every_years': effect.split(',')[4],
                    'min': effect.split(',')[5],
                }
            elif effect_key == 'add_percent_targets_max_health':  # Barrowin
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'targets': 'Champions in the same column as ',
                }
            elif effect_key == 'overwhelm_start_increase':  # Barrowin
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1]
                }
            elif effect_key == 'monster_effect_on_attacked':  # Barrowin
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1]
                }
            elif effect_key == 'buff_attacks_damage':  # Krond Loot
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'ids': effect.split(',', 1)[1]
                }
            # elif effect_key == 'revive_with_health_transfer':  # Strix
            #     return {
            #         'key': effect_key,
            #         'gain': effect.split(',')[1],
            #         'lose': effect.split(',')[2],
            #         'wait': effect.split(',')[3],
            #     }
            elif effect_key == 'bonus_damage_monster_percent_from_party_range':  # Catti-brie
                for _effect in js_effect_key:
                    if _effect['key'] == effect_key:
                        desc = _effect['descriptions']['desc']
                return {
                    'key': effect_key,
                    'desc': desc,
                    'amount': effect.split(',')[1],
                    'start': effect.split(',')[2],
                    'end': effect.split(',')[3],
                }
            elif effect_key == 'binwin_multi_attack':  # Binwin
                for _effect in js_effect_key:
                    if _effect['key'] == effect_key:
                        desc = _effect['descriptions']['desc']
                return {
                    'key': effect_key,
                    'desc': desc,
                    'amount': effect.split(',')[1],
                    'base_odds': effect.split(',')[2],
                    'cooldown_added': effect.split(',')[3],
                    'reduce_odds': effect.split(',')[4],
                }
            elif effect_key == 'add_monster_hit_effects':  # Wulfgar
                if len(effect.split(',')) == 2:
                    return {
                        'key': effect_key,
                        'amount': effect_id,
                    }
                elif effect == effect_key:
                    pass
                else:
                    # print(effect)
                    return {
                        'key': effect_key,
                        'amount': effect.split(',')[1],
                        'ids': effect.split(',', 2)[2]
                    }
            elif effect_key == 'buff_upgrade_per_stunned_enemy':  # Wulfgar
                    return {
                        'key': effect_key,
                        'id': effect.split(',')[1],
                        'amount': effect.split(',')[2],
                        'cap_percent': effect.split(',')[3],
                    }
            elif effect_key == 'add_attack_stun':  # Vlahnya
                atk_name = ''
                for _attack in js_attack:
                    if str(_attack['id']) == effect.split(',', 4)[4]:
                        atk_name = _attack['name']
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'duration': effect.split(',')[2],
                    'ids': effect.split(',', 4)[4],
                    'name': atk_name,
                }
            elif effect_key == 'attacking_companion':  # Warden
                    return {
                        'key': effect_key,
                        'amount': effect.split(',')[1],
                        'attack_id': effect.split(',')[2],
                        'companion_gfx_id': effect.split(',')[3],
                    }
            elif effect_key == 'sneak_attack_hit':  # Black Viper
                    return {
                        'key': effect_key,
                        'amount': effect.split(',')[2],
                        'num_hits': effect.split(',')[1],
                    }
            elif effect_key == 'add_attack_aoe_targets':  # Gromma
                    return {
                        'key': effect_key,
                        'amount': effect.split(',')[1],
                        'radius': effect.split(',')[2],
                    }
            elif effect_key == 'change_upgrade_targets':  # Evelyn
                for upgrade in __upgrades:
                    if not upgrade['required_level'] == 9999:
                        if upgrade['id'] == int(effect_id):
                            _name = upgrade['name']
                return {
                    'key': effect_key,
                    'name': _name,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'gold_mult_per_tagged_crusader':  # Jarlaxle
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'hero_dps_mult_per_target_tag_crusader_mult_amount_before':  # Jarlaxle
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'hero_dps_mult_per_target_loot_rarity':  # Jarlaxle
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'grant_temporary_hp_with_cooldown':  # Calliope
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'interval': effect.split(',')[2],
                    'cooldown': effect.split(',')[3],
                    'percent': effect.split(',')[4],
                }
            elif effect_key == 'buff_upgrades_per_active_upgrade_tag_mult':  # Asharra
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'non_boss_wave_chances_extra_enemies':  # Minsc
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'monster_with_tag_more_damage':  # Minsc
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'damage_buff_on_upgrade_tag_targets':  # Minsc
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'chance_attack_adds_dot':  # Delina
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'chance': effect.split(',')[4],
                }
            elif effect_key == 'hero_dps_mult_per_target_crusader_prebonus_mult':  # Delina
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'chance_add_attack_targets':  # Delina
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'chance': effect.split(',')[2],
                }
            elif effect_key == 'buff_upgrade_per_any_tagged_crusader':  # Makos
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'global_dps_multiplier_mult_minus_targets':  # Tyril
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'reduce_damage_with_limit':  # Tyril
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'limit': effect.split(',')[2],
                }
            elif effect_key == 'target_attacking_monsters_hero_dps_mult':  # Tyril
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'limit': effect.split(',')[2],
                }
            elif effect_key == 'add_health_plus_tag_targets_percent_health':  # Jamilah
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'percent': effect.split(',')[4],
                }
            elif effect_key == 'hero_dps_multiplier_from_temp_hp':  # Jamilah
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'hero_dps_mult_per_target_unique_attacker':  # Jamilah
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'change_base_attack_per_num_attacking':  # Arkhan
                return {
                    'key': effect_key,
                    'attack_id': effect.split(',')[1],
                    'min_attackers': effect.split(',')[2],
                    'amount': '',  # hack
                }
            elif effect_key == 'receive_all_formation_abilities_for':  # Arkhan
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'change_base_attack':  # Hitch
                return {
                    'key': effect_key,
                    'attack_id': effect.split(',')[1],
                    'amount': '',  # hack
                }
            elif effect_key == 'hero_dps_mult_per_target_crusader_mult':  # Hitch
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'damage_reduction_ranged':  # Gromma
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'bonus_damage_range':  # Drizzt
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'min_amount': effect.split(',')[2],
                    'damage_type': effect.split(',')[3],
                }
            elif effect_key == 'targets_with_tag_hero_dps_mult':  # Drizzt
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'hero_dps_mult_by_tag_additive':  # Drizzt
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'increase_monster_damage_from':  # Regis
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'buff_effects_from_upgrade_fa':  # Birdsong
                for upgrade in __upgrades:
                    if not upgrade['required_level'] == 9999:
                        if upgrade['id'] == int(effect_id):
                            _name = upgrade['name']
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'name': _name,
                }
            elif effect_key == 'increase_monster_damage_percent_to_party':  # Strix
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'revive_with_health_transfer':  # Strix
                return {
                    'key': effect_key,
                    'gain_percent': effect.split(',')[1],
                    'lose_percent': effect.split(',')[2],
                    'wait_time': effect.split(',')[3],
                    'amount': '',  # hack
                }
            elif effect_key == 'reduce_attack_cooldown_if_formation_under_attack':  # Strix
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'increase_attack_cooldown':  # Strix
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'amount___2': str(int(int(effect.split(',')[1])*2)),
                }
            elif effect_key == 'add_attack_aoe_targets_every':  # Nrakk
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'radius': effect.split(',')[2],
                    'every_num_attacks': effect.split(',')[3],
                }
            elif effect_key == 'bonus_damage_every':  # Nrakk
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'stun_does_cooldown_and_damage_mult':  # Nrakk
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'limit': effect.split(',')[2],
                    'cooldown': effect.split(',')[3],
                }
            elif effect_key == 'add_target_to_upgrade':  # Deekin
                return {
                    'key': effect_key,
                    'amount': '',  # hack
                }
            elif effect_key == 'buff_upgrade_or_has_tracked_effect':  # Deekin
                return {
                    'key': effect_key,
                    'amount': '',  # hack
                }
            elif effect_key == 'azaka_weretiger':  # Azaka
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'azaka_time': effect.split(',')[2],
                    'azaka_attacks': effect.split(',')[3],
                }
            elif effect_key == 'gold_mult_if_monsters_on_screen':  # Ishi
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'buff_attack_monster_effects_index_additive':  # Donaar
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'index': effect.split(',')[2],
                }
            elif effect_key == 'buff_attack_monster_effects_index':  # Donaar
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'index': effect.split(',')[2],
                }
            elif effect_key == 'force_add_target_to_upgrade':  # Donaar
                return {
                    'key': effect_key,
                    'amount': '',
                }
            elif effect_key == 'attack_hits_again':  # Warden
                return {
                    'key': effect_key,
                    'amount': '',
                }
            elif effect_key == 'spread_monster_effect':  # Warden
                return {
                    'key': effect_key,
                    'amount': '',
                }
            elif effect_key == 'fire_trigger_by_upgrade_id':  # Nerys
                return {
                    'key': effect_key,
                    'amount': '',
                }
            elif effect_key == 'kthriss_hordesperson':  # K'thriss
                return {
                    'key': effect_key,
                    'amount': '',
                }
            elif effect_key == 'blackviper_jewel_thief':  # Black Viper
                return {
                    'key': effect_key,
                    'amount': '',
                }
            elif effect_key == 'increase_jewel_thief_drop_rate':  # Black Viper
                return {
                    'key': effect_key,
                    'amount': '',
                }
            elif effect_key == 'increase_jewel_thief_damage_bonus':  # Black Viper
                return {
                    'key': effect_key,
                    'amount': '',
                }
            elif effect_key == 'return_source_damage_when_hit':  # Rosie
                return {
                    'key': effect_key,
                    'amount': '',
                }
            elif effect_key == 'buff_upgrade_per_any_tagged_crusader_where':  # Rosie
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'increase_storm_soul_stun_seconds':  # Aila
                return {
                    'key': effect_key,
                    'amount': '',
                }
            elif effect_key == 'increase_raging_storm_stun_seconds':  # Aila
                return {
                    'key': effect_key,
                    'amount': '',
                }
            elif effect_key == 'spurt_waspiration':  # Spurt
                return {
                    'key': effect_key,
                    'kill_count': effect.split(',')[1],
                    'time': effect.split(',')[2],
                    'amount': '',
                }
            elif effect_key == 'aila_aerois_synergy_contribution':  # Aila
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'amount_max': effect.split(',')[2],
                }
            elif effect_key == 'upgrade_buff_from_aerois_synergy_pool':  # Aila
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'upgrade_id': effect.split(',')[2],
                }
            elif effect_key == 'heal_by_distance_from_source':  # Qillek
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'distance': effect.split(',')[2],
                }
            elif effect_key == 'add_upgrade_bonus_by_target':  # Qillek
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'qilleck_aerois_synergy_contribution':  # Qillek
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'amount_min': effect.split(',')[2],
                    'increase': effect.split(',')[3],
                }
            elif effect_key == 'korth_lizardfolk_tactics':  # Korth
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                }
            elif effect_key == 'korth_fighting_spirit':  # Korth
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'cooldown': effect.split(',')[2],
                }
            elif effect_key == 'korth_calculated':  # Korth
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'time': effect.split(',')[2],
                }
            elif effect_key == 'korth_rapid_strike':  # Korth
                return {
                    'key': effect_key,
                    'chance': effect.split(',')[1],
                    'ult_reduce': effect.split(',')[2],
                    'amount': '',
                }
            elif effect_key == 'korth_resurrection':  # Korth
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'timer': effect.split(',')[2],
                }
            elif effect_key == 'walnut_jobs_done':  # Walnut
                for upgrade in __upgrades:
                    if upgrade['id'] == int(effect.split(',')[2]):
                        _name = upgrade['name']
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'upgrade_id': effect.split(',')[2],
                    'duration': effect.split(',')[3],
                    'name': _name,
                }
            elif effect_key == 'wolfnut':  # Walnut
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'attack_id': effect.split(',')[2],
                }
            elif effect_key == 'walnut_cosigners':  # Walnut
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'attack_id': effect.split(',')[2],
                }
            elif effect_key == 'buff_upgrade_by_target_tag_mult':
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'upgrade_id': effect.split(',')[4],
                }
            elif effect_key == 'grant_temporary_hp_with_cooldown':
                return {
                    'key': effect_key,
                    'amount': effect.split(',')[1],
                    'interval': effect.split(',')[2],
                    'cooldown': effect.split(',')[3],
                    'optional_percent_limit': effect.split(',')[4],
                }
            # elif effect_key == 'reduce_upgrade_every_num_attacks':  # Rosie
            #         return {
            #             'key': effect_key,
            #             'amount': effect.split(',')[2],
            #             'num_hits': effect.split(',')[1],
            #         }
            elif effect_key == 'do_nothing':
                return {
                    'key': effect_key,
                    'amount': '',
                }
            print('error:', effect)
            return False

        for upgrade in __upgrades:
            if not upgrade['required_level'] == 9999:
                # If Unlock Specialization
                if 'specialization_name' in upgrade:
                    # if upgrade['name'] == upgrade['specialization_name']:
                    #     print(name, upgrade)
                    # print('specialization')
                    if not upgrade['required_level'] in ab_table:
                        ab_table[upgrade['required_level']] = {'unlockSpec': True}
                    ab_table[upgrade['required_level']]['unlockSpec'] = True
                    spec_desc = upgrade['specialization_description']
                    spec_name = upgrade['specialization_name']
                    if 'spec7title' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec8title'] = spec_desc
                    elif 'spec6title' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec7title'] = spec_desc
                    elif 'spec5title' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec6title'] = spec_desc
                    elif 'spec4title' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec5title'] = spec_desc
                    elif 'spec3title' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec4title'] = spec_desc
                    elif 'spec2title' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec3title'] = spec_desc
                    elif 'spec1title' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec2title'] = spec_desc
                    else:
                        ab_table[upgrade['required_level']]['spec1title'] = spec_desc
                    if 'spec7name' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec8name'] = spec_name
                    elif 'spec6name' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec7name'] = spec_name
                    elif 'spec5name' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec6name'] = spec_name
                    elif 'spec4name' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec5name'] = spec_name
                    elif 'spec3name' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec4name'] = spec_name
                    elif 'spec2name' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec3name'] = spec_name
                    elif 'spec1name' in ab_table[upgrade['required_level']]:
                        ab_table[upgrade['required_level']]['spec2name'] = spec_name
                    else:
                        ab_table[upgrade['required_level']]['spec1name'] = spec_name
                # If Unlock Ability
                if upgrade['upgrade_type'] == 'unlock_ability':
                    # print('unlockAbility')
                    if 'specialization_name' not in upgrade:
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {'unlockAbility': True}
                        effect = None
                        # print(upgrade)
                        effect = parse_effect(upgrade['effect'])
                        if effect:
                            # print(effect)
                            if effect['key'] == 'reduce_overwhelm_effect':
                                # print('unlock_ability -> reduce_overwhelm_effect')
                                ab_table[upgrade['required_level']
                                         ]['redOverwhelm'] = effect['amount'] + '%'
                                # desc = effect['desc'].replace('$target', name)
                                ab_table[upgrade['required_level']]['abTitle'] = effect['desc']
                                ab_table[upgrade['required_level']]['abName'] = upgrade['name']
                            elif effect['key'] == 'attack_crit_chance':
                                # print('attack_crit_chance')
                                ab_table[upgrade['required_level']
                                         ]['AttCritChance'] = effect['chance'] + '%'
                                ab_table[upgrade['required_level']]['AttCritDmg'] = effect['amount']
                                ab_table[upgrade['required_level']]['abTitle'] = effect['desc']
                                ab_table[upgrade['required_level']]['abName'] = upgrade['name']
                            elif effect['key'] == 'increase_num_unique_hits':
                                # print('increase_num_unique_hits')
                                desc = effect['desc']
                                desc = desc.replace('$target', name)
                                ab_table[upgrade['required_level']]['IncHits'] = effect['amount'] + '%'
                                ab_table[upgrade['required_level']]['abTitle'] = desc
                                ab_table[upgrade['required_level']]['abName'] = upgrade['name']
                            elif effect['key'] == 'effect_def':
                                # print('just a multiple effect_def. should be in Vlahnya.')
                                desc = effect['desc'] if 'desc' in effect else ''
                                if desc == '':
                                    if not name == 'Aila':
                                        desc = upgrade['tip_text']      # Vlahnya
                                        ids = effect['ids']
                                    for _effect in js_effect:
                                        if str(_effect['id']) in ids.split(','):
                                            if not _effect['id'] == 237:
                                                _effect_name = _effect['properties']['effect_name']
                                                _effect_desc = _effect['description']\
                                                    .replace('\r\n', '')\
                                                    .replace('$(if not incoming_desc)Increases the damage of Champions ahead of $source by $(with_upgrade_bonus 1656,3 amount)% for each stack:$(fi)', '')\
                                                    .replace('$only_when_purchased (Current stacks: $(upgrade_stacks_num 1656,0)/$max_stacks at $(upgrade_bonus 1656,0)% effectiveness = $(active_upgrade_value_with_bonuses 1656,0 1656,3)%)', '')\
                                                    .replace('$only_when_purchased (Current stacks: $(upgrade_stacks_num 1656,1)/$max_stacks at $(upgrade_bonus 1656,1)% effectiveness = $(active_upgrade_value_with_bonuses 1656,1 ', '')\
                                                    .replace('$only_when_purchased (Current stacks: $(upgrade_stacks_num 1656,1)/$max_stacks at $(upgrade_bonus 1656,1)% effectiveness  = $(active_upgrade_value_with_bonuses 1656,1 1656,3)%)', '')\
                                                    .replace('$only_when_purchased (Current stacks: $(upgrade_stacks_num 1656,2)/$max_stacks at $(upgrade_bonus 1656,2)% effectiveness = $(active_upgrade_value_with_bonuses 1656,2 1656,3)%)$(if not incoming_desc)Each trigger\'s stack decreases by 20% every 10 secondsTotal Bonus: $(active_upgrade_value 1656,3)%$(fi)', '')\
                                                    .replace('$base_stack_amount', str(_effect['effect_keys'][0]['base_stack_amount']))\
                                                    .replace('$source', name)
                                                desc += '\n\n'
                                                desc += ('* ' + _effect_name)
                                                desc += '\n\n'
                                                desc += (': ' + _effect_desc)
                                if isinstance(ab_table[upgrade['required_level']], list):
                                    temp = {'unlockAbility': True}
                                    temp['abTitle'] = desc
                                    temp['abName'] = upgrade['name']
                                    ab_table[upgrade['required_level']].append(temp)
                                elif not 'abTitle' in ab_table[upgrade['required_level']]:
                                    ab_table[upgrade['required_level']]['abTitle'] = desc
                                    ab_table[upgrade['required_level']]['abName'] = upgrade['name']
                                else:
                                    temp = ab_table[upgrade['required_level']]
                                    ab_table[upgrade['required_level']] = []
                                    ab_table[upgrade['required_level']].append(temp)
                                    temp2 = {'unlockAbility': True}
                                    temp2['abTitle'] = desc
                                    temp2['abName'] = upgrade['name']
                                    ab_table[upgrade['required_level']].append(temp2)
                            elif effect['key'] == 'reduce_upgrade_every_num_attacks':  # Rosie
                                # print('reduce_upgrade_every_num_attacks')
                                # _effect = parse_effect
                                # desc = effect['desc']
                                for _effect_key in js_effect_key:
                                    if effect['key'] == _effect_key['key']:
                                        desc = _effect_key['descriptions']['desc']
                                desc = desc\
                                    .replace('$(upgrade_hero id)', name)\
                                    .replace('$(upgrade_name id)', effect['name'])\
                                    .replace('$amount', effect['amount'])
                                ab_table[upgrade['required_level']]['abTitle'] = desc
                                ab_table[upgrade['required_level']]['abName'] = upgrade['name']
                            elif effect['key'] in ['aila_storm_aura', 'storm_aura_storm_soul']:  # Aila
                                # print('aila_storm_aura or storm_aura_storm_soul')
                                ab_table[upgrade['required_level']]['abTitle'] = upgrade['tip_text']
                                ab_table[upgrade['required_level']]['abName'] = upgrade['name']
                            elif effect['key'] in [
                                'storm_aura_shielding_storm',  # Aila
                                'storm_aura_raging_storm',  # Aila
                            ]:
                                # print('storm_aura_shielding_storm')
                                # for _effect_key in js_effect_key:
                                #     if effect['key'] == _effect_key['key']:
                                #         desc = _effect_key['descriptions']['desc']
                                desc = effect['desc']
                                desc = desc\
                                    .replace('$amount', effect['amount'])\
                                    .replace('$(if not upgrade_purchased 2206)0.5 seconds$(or)', '')\
                                    .replace('$(fi)', '')
                                ab_table[upgrade['required_level']]['abTitle'] = desc
                                ab_table[upgrade['required_level']]['abName'] = upgrade['name']
                            elif 'specialization_name' in upgrade:  # Nerys
                                pass
                                # print('spec, not unlock ability')
                                # ab_table[upgrade['required_level']]['REQUIRE'] = upgrade['name'] if not upgrade['name'] == '' else upgrade['specialization_name']
                            elif not effect['key'] in ['health_add']:
                                # print('unlock_ability but not health_add')
                                print(upgrade)
                                print(effect)
                                ab_table[upgrade['required_level']]['abTitle'] = effect['desc']
                                ab_table[upgrade['required_level']]['abName'] = upgrade['name']
                #  Special Celeste Ability Unlock
                elif upgrade['upgrade_type'] == 'increase_health':
                    effect = None
                    effect = parse_effect(upgrade['effect'])
                    if effect:
                        if effect['key'] == 'effect_def':
                            if not upgrade['required_level'] in ab_table:
                                ab_table[upgrade['required_level']] = {'unlockAbility': True}
                            desc = effect['desc']
                            desc = desc\
                                .replace('$target', name)\
                                .replace('$source', name)\
                                .replace('$(upgrade_hero id)', name)\
                                .replace('$(upgrade_name id)', effect['name'] if 'name' in effect else '')\
                                .replace(' $amount%', '')\
                                .replace(' $(amount)%', '')\
                                .replace(' $amount seconds', '')\
                                .replace(' $(amount) seconds', '')\
                                .replace(' for $(amount)', '')\
                                .replace(' for $amount', '')
                            if isinstance(ab_table[upgrade['required_level']], list):
                                temp = {'unlockAbility': True}
                                temp['abTitle'] = desc
                                temp['abName'] = upgrade['name']
                                ab_table[upgrade['required_level']].append(temp)
                            elif not 'abTitle' in ab_table[upgrade['required_level']]:
                                ab_table[upgrade['required_level']]['abTitle'] = desc
                                ab_table[upgrade['required_level']]['abName'] = upgrade['name']
                            else:
                                temp = ab_table[upgrade['required_level']]
                                ab_table[upgrade['required_level']] = []
                                ab_table[upgrade['required_level']].append(temp)
                                temp2 = {'unlockAbility': True}
                                temp2['abTitle'] = desc
                                temp2['abName'] = upgrade['name']
                                ab_table[upgrade['required_level']].append(temp2)
                    # elif effect['key'] == 'buff_upgrade':
                    #     for _upgrade in __upgrades:
                    #         if (not upgrade['required_upgrade_id'] == 0) and (not upgrade['required_upgrade_id'] == 9999):
                    #             if int(effect['id']) == _upgrade['id']:
                    #                 # print(_upgrade)
                    #                 # print(effect)
                    #                 _amount = effect['amount']
                    #                 # print(upgrade)
                    #                 # print(_upgrade)
                    #                 for __upgrade in __upgrades:
                    #                     if (not upgrade['required_upgrade_id'] == 0) and (not upgrade['required_upgrade_id'] == 9999):
                    #                         if upgrade['required_upgrade_id'] == __upgrade['id']:
                    #                             specname = __upgrade['specialization_name']
                    #                 # if 'specialization_name' in _upgrade:
                    #                 if not upgrade['required_level'] in ab_table:
                    #                     ab_table[upgrade['required_level']] = {}
                    #                 if isinstance(ab_table[upgrade['required_level']], list):
                    #                     # temp[effect['name']] = '{amount}'.format(amount=_amount)
                    #                     temp[effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=specname, amount=_amount)
                    #                     ab_table[upgrade['required_level']].append(temp)
                    #                 elif not effect['name'] in ab_table[upgrade['required_level']]:
                    #                     # ab_table[upgrade['required_level']][effect['name']] = '{amount}'.format(amount=_amount)
                    #                     ab_table[upgrade['required_level']][effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=specname, amount=_amount)
                    #                 else:
                    #                     temp = ab_table[upgrade['required_level']]
                    #                     ab_table[upgrade['required_level']] = []
                    #                     ab_table[upgrade['required_level']].append(temp)
                    #                     temp2 = {}
                    #                     # temp2[effect['name']] = '{amount}'.format(amount=_amount)
                    #                     temp2[effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=specname, amount=_amount)
                    #                     ab_table[upgrade['required_level']].append(temp2)
                #  Special Calliope Ability Unlock
                elif upgrade['upgrade_type'] is None:
                    # if not upgrade['hero_id'] == 6:  # If not Asharra
                    effect = None
                    effect = parse_effect(upgrade['effect'])
                    if effect:
                        if effect['key'] == 'effect_def':
                            if not upgrade['required_level'] in ab_table:
                                ab_table[upgrade['required_level']] = {'unlockAbility': True}
                            # print(ab_table[upgrade['required_level']])
                            ab_table[upgrade['required_level']]['abTitle'] = effect['desc']
                            ab_table[upgrade['required_level']]['abName'] = upgrade['name']
                            pass
                        # Asharra
                        elif effect['key'] == 'add_attack_targets':  # Asharra
                            if not upgrade['required_level'] in ab_table:
                                ab_table[upgrade['required_level']] = {}
                            ab_table[upgrade['required_level']]['add_attack_targets'] = ' +' + effect['amount']
                            ab_table[upgrade['required_level']]['abName'] = 'add_attack_targets'
                # Upgrade ability
                elif upgrade['upgrade_type'] == 'upgrade_ability':
                    effect = None
                    effect = parse_effect(upgrade['effect'])
                    if effect:
                        if effect['key'] == 'add_attack_targets':  # Asharra
                            if not upgrade['required_level'] in ab_table:
                                ab_table[upgrade['required_level']] = {}
                            ab_table[upgrade['required_level']]['add_attack_targets'] = ' +' + effect['amount']
                            ab_table[upgrade['required_level']]['abName'] = 'add_attack_targets'
                        if name == 'Asharra':
                            if effect['key'] == 'buff_upgrades':  # Asharra Bond buff
                                if len(effect['ids']) == 3:
                                    if not upgrade['required_level'] in ab_table:
                                        ab_table[upgrade['required_level']] = {}
                                    ab_table[upgrade['required_level']]['spec1upg'] = effect['amount'] + '%'
                                    ab_table[upgrade['required_level']]['abName'] = 'spec1upg'
                                elif len(effect['ids']) == 6:
                                    if not upgrade['required_level'] in ab_table:
                                        ab_table[upgrade['required_level']] = {}
                                    ab_table[upgrade['required_level']]['spec2upg'] = effect['amount'] + '%'
                                    ab_table[upgrade['required_level']]['spec1upg'] = effect['amount'] + '%'
                                    ab_table[upgrade['required_level']]['abName'] = 'spec2upg'
                                else:
                                    print('ugh')
                        elif name == 'Minsc':
                            if effect['key'] == 'buff_upgrades':  # Asharra Bond buff
                                if len(effect['ids']) == 5:
                                    if not upgrade['required_level'] in ab_table:
                                        ab_table[upgrade['required_level']] = {}
                                    ab_table[upgrade['required_level']]['specupg'] = effect['amount'] + '%'
                                    ab_table[upgrade['required_level']]['abName'] = 'specupg'
                        elif name == 'Regis':
                            if effect['key'] == 'buff_upgrades':  # Asharra Bond buff
                                if len(effect['ids']) == 2:
                                    if not upgrade['required_level'] in ab_table:
                                        ab_table[upgrade['required_level']] = {}
                                    ab_table[upgrade['required_level']]['spec1upg'] = effect['amount'] + '%'
                                    ab_table[upgrade['required_level']]['abName'] = 'spec1upg'
                                elif len(effect['ids']) == 3:
                                    if not upgrade['required_level'] in ab_table:
                                        ab_table[upgrade['required_level']] = {}
                                    ab_table[upgrade['required_level']]['spec2upg'] = effect['amount'] + '%'
                                    # ab_table[upgrade['required_level']]['spec1upg'] = effect['amount'] + '%'
                                    ab_table[upgrade['required_level']]['abName'] = 'spec2upg'
                                else:
                                    print('ugh')
                                    exit()
                        elif name == 'Zorbu':
                            if effect['key'] == 'buff_upgrade':  # Asharra Bond buff
                                if effect['id'] in ['843', '844', '845', '846', '847']:
                                    if not upgrade['required_level'] in ab_table:
                                        ab_table[upgrade['required_level']] = {}
                                    ab_table[upgrade['required_level']]['spec1upg'] = effect['amount']
                                    ab_table[upgrade['required_level']]['abName'] = 'spec1upg'
                                elif effect['id'] in ['850', '851']:
                                    if not upgrade['required_level'] in ab_table:
                                        ab_table[upgrade['required_level']] = {}
                                    ab_table[upgrade['required_level']]['spec2upg'] = effect['amount']
                                    ab_table[upgrade['required_level']]['abName'] = 'spec2upg'
                        elif name =='Gromma':
                            if effect['key'] == 'effect_def':
                                if not upgrade['required_level'] in ab_table:
                                    ab_table[upgrade['required_level']] = {'unlockAbility': True}
                                # print(ab_table[upgrade['required_level']])
                                _effect = None
                                _effect = parse_effect(upgrade['effect'])
                                desc = _effect['desc']
                                desc = desc\
                                    .replace('$target', name)\
                                    .replace('$source', name)\
                                    .replace('$(upgrade_hero id)', name)\
                                    .replace('$(upgrade_name id)', effect['name'] if 'name' in effect else '')
                                    # .replace('$amount', _effect['amount'])
                                if isinstance(ab_table[upgrade['required_level']], list):
                                    temp = {'unlockAbility': True}
                                    temp['abTitle'] = desc
                                    temp['abName'] = upgrade['name']
                                    ab_table[upgrade['required_level']].append(temp)
                                elif not 'abTitle' in ab_table[upgrade['required_level']]:
                                    ab_table[upgrade['required_level']]['abTitle'] = desc
                                    ab_table[upgrade['required_level']]['abName'] = upgrade['name']
                                else:
                                    temp = ab_table[upgrade['required_level']]
                                    ab_table[upgrade['required_level']] = []
                                    ab_table[upgrade['required_level']].append(temp)
                                    temp2 = {'unlockAbility': True}
                                    temp2['abTitle'] = desc
                                    temp2['abName'] = upgrade['name']
                                    ab_table[upgrade['required_level']].append(temp2)
                                # print(ab_table[upgrade['required_level']])
                        elif name == 'Ishi':
                            if effect['key'] == 'buff_upgrade':  # Asharra Bond buff
                                if effect['id'] in ['1239', '1240']:
                                    if not upgrade['required_level'] in ab_table:
                                        ab_table[upgrade['required_level']] = {}
                                    ab_table[upgrade['required_level']]['spec1upg'] = effect['amount']
                                    ab_table[upgrade['required_level']]['abName'] = 'spec1upg'
                                elif effect['id'] in ['1243', '1244', '1245']:
                                    if not upgrade['required_level'] in ab_table:
                                        ab_table[upgrade['required_level']] = {}
                                    ab_table[upgrade['required_level']]['spec2upg'] = effect['amount']
                                    ab_table[upgrade['required_level']]['abName'] = 'spec2upg'
                # If Ultimate
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'set_ultimate_attack':
                        # print('ultimate')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {'unlockUltimate': True}
                        for attack in js_attack:
                            if str(attack['id']) == effect['id']:
                                desc = effect['desc']
                                desc = desc.replace('$ishi_ult_time', '15')  # Ishi
                                ab_table[upgrade['required_level']]['abTitle'] = desc
                                ab_table[upgrade['required_level']]['abName'] = effect['name']
                    elif (id_ == 43 and upgrade['upgrade_type'] == 'unlock_ultimate'):
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {'unlockUltimate': True}
                        for _effect in js_effect:
                            if int(effect['id']) == _effect['id']:
                                effect_string = _effect['effect_keys'][0]['effect_string']
                                __effect = parse_effect(effect_string)
                                ab_table[upgrade['required_level']]['abTitle'] = desc
                                ab_table[upgrade['required_level']]['abName'] = __effect['name']
                # If Damage
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'hero_dps_multiplier_mult':
                        # print('ifdamage')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        if (not upgrade['required_upgrade_id'] == 0) and (not upgrade['required_upgrade_id'] == 9999):
                            for _upgrade in __upgrades:
                                if not _upgrade['required_level'] == 9999:
                                    if (not upgrade['required_upgrade_id'] == 0) and (not upgrade['required_upgrade_id'] == 9999):
                                        if upgrade['required_upgrade_id'] == _upgrade['id']:
                                            specname = _upgrade['specialization_name']
                            ab_table[upgrade['required_level']]['dmg'] = '{{{{Spec|{spec}|{amount}%}}}}'.format(spec=specname, amount=effect['amount'])
                        else:
                            ab_table[upgrade['required_level']]['dmg'] = effect['amount'] + '%'
                # If Damage All
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'global_dps_multiplier_mult':
                        # print('ifdamageall')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        if (not upgrade['required_upgrade_id'] == 0) and (not upgrade['required_upgrade_id'] == 9999):
                            for _upgrade in __upgrades:
                                if not _upgrade['required_level'] == 9999:
                                    if (not upgrade['required_upgrade_id'] == 0) and (not upgrade['required_upgrade_id'] == 9999):
                                        if upgrade['required_upgrade_id'] == _upgrade['id']:
                                            specname = _upgrade['specialization_name']
                            ab_table[upgrade['required_level']]['dmg_all'] = '{{{{Spec|{spec}|{amount}%}}}}'.format(spec=specname, amount=effect['amount'])
                        else:
                            ab_table[upgrade['required_level']]['dmg_all'] = effect['amount'] + '%'
                # If Gold Mult
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'gold_multiplier_mult':
                        # print('ifgoldX')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        ab_table[upgrade['required_level']]['GoldFind'] = effect['amount'] + '%'
                # If health
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'health_add':
                        # print('health')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        # if 'tanking' in hero['tags']:
                        # ab_table[upgrade['required_level']]['Health'] = ' +' + effect['amount']
                        ###################print(effect)
                        ###################print(upgrade)
                        spec = None
                        for _upgrade in __upgrades:
                            # print(upgrade['required_upgrade_id'], _upgrade['id'])
                            if upgrade['required_upgrade_id'] == _upgrade['id']:
                                spec = _upgrade['specialization_name']
                        _amount = effect['amount']
                        if isinstance(ab_table[upgrade['required_level']], list):
                            temp['Health'] = '{{{{Spec|{spec}|+{amount}}}}}'.format(spec=spec, amount=_amount)
                            ab_table[upgrade['required_level']].append(temp)
                        elif not 'Health' in ab_table[upgrade['required_level']]:
                            # ab_table[upgrade['required_level']]['Health'] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=spec, amount=_amount)
                            if spec is None:
                                ab_table[upgrade['required_level']]['Health'] = ' +{amount}'.format(amount=_amount)
                            else:
                                ab_table[upgrade['required_level']]['Health'] = '{{{{Spec|{spec}|+{amount}}}}}'.format(spec=spec, amount=_amount)
                        else:
                            temp = ab_table[upgrade['required_level']]
                            ab_table[upgrade['required_level']] = []
                            ab_table[upgrade['required_level']].append(temp)
                            temp2 = {}
                            # temp2['Health'] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=spec, amount=_amount)
                            temp2['Health'] = '{{{{Spec|{spec}|+{amount}}}}}'.format(spec=spec, amount=_amount)
                            ab_table[upgrade['required_level']].append(temp2)
                # If spec upgrade
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'buff_upgrade':
                        # print('spec upgrade')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        _unit = effect['unit'] if 'unit' in effect else ''
                        _amount = effect['amount'] + _unit
                        if 'specialization_name' in upgrade:
                            _spec = upgrade['specialization_name']
                            if isinstance(ab_table[upgrade['required_level']], list):
                                temp[effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=_spec, amount=_amount)
                                ab_table[upgrade['required_level']].append(temp)
                                # print(id_, 'spec_upg', name, upgrade)
                            elif not effect['name'] in ab_table[upgrade['required_level']]:
                                ab_table[upgrade['required_level']][effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=_spec, amount=_amount)
                                # print(id_, 'spec_upg', name, upgrade)
                            else:
                                temp = ab_table[upgrade['required_level']]
                                ab_table[upgrade['required_level']] = []
                                ab_table[upgrade['required_level']].append(temp)
                                temp2 = {}
                                temp2[effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=_spec, amount=_amount)
                                ab_table[upgrade['required_level']].append(temp2)
                                # print(id_, 'spec_upg', name, upgrade)
                        else:
                            for _upgrade in __upgrades:
                                if not _upgrade['required_level'] == 9999:
                                    if (not upgrade['required_upgrade_id'] == 0) and (not upgrade['required_upgrade_id'] == 9999):
                                        if 'specialization_name' in _upgrade:
                                            _effect = parse_effect(_upgrade['effect'])
                                            if _effect['key'] == 'buff_upgrade':
                                                if not name in ['Catti-brie', 'Hitch']:
                                                    if isinstance(ab_table[upgrade['required_level']], list):
                                                        temp[effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=_upgrade['specialization_name'], amount=_amount)
                                                        ab_table[upgrade['required_level']].append(temp)
                                                        # print(id_, '~~~~~~~~~~~~', name, upgrade, _upgrade, _effect)
                                                        # print('{{{{Spec|{spec}|{amount}}}}}'.format(spec=_upgrade['specialization_name'], amount=_amount))
                                                    elif not effect['name'] in ab_table[upgrade['required_level']]:
                                                        ab_table[upgrade['required_level']][effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=_upgrade['specialization_name'], amount=_amount)
                                                        # print(id_, '~~~~~~~~~~~~', name, upgrade, _upgrade, _effect)
                                                        # print('{{{{Spec|{spec}|{amount}}}}}'.format(spec=_upgrade['specialization_name'], amount=_amount))
                                                    else:
                                                        temp = ab_table[upgrade['required_level']]
                                                        ab_table[upgrade['required_level']] = []
                                                        ab_table[upgrade['required_level']].append(temp)
                                                        temp2 = {}
                                                        temp2[effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=_upgrade['specialization_name'], amount=_amount)
                                                        ab_table[upgrade['required_level']].append(temp2)
                                                        # print(id_, '~~~~~~~~~~~~', name, upgrade, _upgrade, _effect)
                                                        # print('{{{{Spec|{spec}|{amount}}}}}'.format(spec=_upgrade['specialization_name'], amount=_amount))
                                            elif int(effect['id']) == _upgrade['id']:
                                                if not name in ['Zorbu', 'Ishi']:
                                                    if isinstance(ab_table[upgrade['required_level']], list):
                                                        temp[effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=_upgrade['specialization_name'], amount=_amount)
                                                        ab_table[upgrade['required_level']].append(temp)
                                                        # print(id_, '*************', name, upgrade, _upgrade, effect)
                                                        # print('{{{{Spec|{spec}|{amount}}}}}'.format(spec=_upgrade['specialization_name'], amount=_amount))
                                                    elif not effect['name'] in ab_table[upgrade['required_level']]:
                                                        ab_table[upgrade['required_level']][effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=_upgrade['specialization_name'], amount=_amount)
                                                        # print(id_, '*************', name, upgrade, _upgrade, effect)
                                                        # print('{{{{Spec|{spec}|{amount}}}}}'.format(spec=_upgrade['specialization_name'], amount=_amount))
                                                    else:
                                                        temp = ab_table[upgrade['required_level']]
                                                        ab_table[upgrade['required_level']] = []
                                                        ab_table[upgrade['required_level']].append(temp)
                                                        temp2 = {}
                                                        temp2[effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=_upgrade['specialization_name'], amount=_amount)
                                                        ab_table[upgrade['required_level']].append(temp2)
                                                        # print(id_, '*************', name, upgrade, _upgrade, effect)
                                                        # print('{{{{Spec|{spec}|{amount}}}}}'.format(spec=_upgrade['specialization_name'], amount=_amount))
                                        elif int(effect['id']) == _upgrade['id']:
                                            # if name not in ['Gromma']:
                                                for __upgrade in __upgrades:
                                                    if not __upgrade['required_level'] == 9999:
                                                        if (not upgrade['required_upgrade_id'] == 0) and (not upgrade['required_upgrade_id'] == 9999):
                                                            if upgrade['required_upgrade_id'] == __upgrade['id']:
                                                                specname = __upgrade['specialization_name']
                                                                # print("I\'m here")
                                                                # print(specname)
                                                if isinstance(ab_table[upgrade['required_level']], list):
                                                    temp = {}
                                                    temp[effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=specname, amount=_amount)
                                                    # print('before', ab_table[upgrade['required_level']])
                                                    ab_table[upgrade['required_level']].append(temp)
                                                    # print('after', ab_table[upgrade['required_level']])
                                                    # print(id_, 'onlybuffupg_reqid_nospec_if', name, upgrade)
                                                    # print(id_, 'onlybuffupg_reqid_nospec_if', name, '\t', _upgrade)
                                                    # print(id_, 'onlybuffupg_reqid_nospec_if', name, '\t\t', ab_table[upgrade['required_level']])
                                                    # print(id_, 'onlybuffupg_reqid_nospec_if', name, '\t\t\t', effect)
                                                    # print(id_, 'onlybuffupg_reqid_nospec_if', name, '\t\t\t\t', specname)
                                                elif not effect['name'] in ab_table[upgrade['required_level']]:
                                                    # print('before', ab_table[upgrade['required_level']])
                                                    ab_table[upgrade['required_level']][effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=specname, amount=_amount)
                                                    # print('after', ab_table[upgrade['required_level']])
                                                    # print(id_, 'onlybuffupg_reqid_nospec_elif', name, upgrade)
                                                    # print(id_, 'onlybuffupg_reqid_nospec_elif', name, '\t', _upgrade)
                                                    # print(id_, 'onlybuffupg_reqid_nospec_elif', name, '\t\t', ab_table[upgrade['required_level']])
                                                    # print(id_, 'onlybuffupg_reqid_nospec_elif', name, '\t\t\t', effect)
                                                    # print(id_, 'onlybuffupg_reqid_nospec_elif', name, '\t\t\t\t', specname)
                                                else:
                                                    temp = None
                                                    temp = ab_table[upgrade['required_level']]
                                                    ab_table[upgrade['required_level']] = []
                                                    ab_table[upgrade['required_level']].append(temp)
                                                    temp2 = {}
                                                    temp2[effect['name']] = '{{{{Spec|{spec}|{amount}}}}}'.format(spec=specname, amount=_amount)
                                                    # print('before', ab_table[upgrade['required_level']])
                                                    ab_table[upgrade['required_level']].append(temp2)
                                                    # print('after', ab_table[upgrade['required_level']])
                                                    # print(id_, 'onlybuffupg_reqid_nospec_else', name, upgrade)
                                                    # print(id_, 'onlybuffupg_reqid_nospec_else', name, '\t', _upgrade)
                                                    # print(id_, 'onlybuffupg_reqid_nospec_else', name, '\t\t', ab_table[upgrade['required_level']])
                                                    # print(id_, 'onlybuffupg_reqid_nospec_else', name, '\t\t\t', effect)
                                                    # print(id_, 'onlybuffupg_reqid_nospec_else', name, '\t\t\t\t', specname)
                                    elif upgrade['required_upgrade_id'] == 0:
                                        if int(effect['id']) == _upgrade['id']:
                                            if isinstance(ab_table[upgrade['required_level']], list):
                                                temp[effect['name']] = '{amount}'.format(amount=_amount)
                                                ab_table[upgrade['required_level']].append(temp)
                                                # print(id_, 'onlybuffupg_special_case', name, upgrade)
                                            elif not effect['name'] in ab_table[upgrade['required_level']]:
                                                ab_table[upgrade['required_level']][effect['name']] = '{amount}'.format(amount=_amount)
                                                # print(id_, 'onlybuffupg_special_case', name, upgrade)
                                            else:
                                                temp = ab_table[upgrade['required_level']]
                                                ab_table[upgrade['required_level']] = []
                                                ab_table[upgrade['required_level']].append(temp)
                                                temp2 = {}
                                                temp2[effect['name']] = '{amount}'.format(amount=_amount)
                                                ab_table[upgrade['required_level']].append(temp2)
                                                # print(id_, 'onlybuffupg_special_case', name, upgrade)
                                    # print('\n')

                # Buff Ultimate
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'buff_ultimate':
                        # print('buff ultimate')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        ab_table[upgrade['required_level']]['buffUlt'] = effect['amount'] + '%'
                # Increase targets and damage
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'add_attack_nearby_targets':
                        # print('add_attack_nearby_targets')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        ab_table[upgrade['required_level']]['incTarAmt'] = '+' + effect['targets']
                        ab_table[upgrade['required_level']]['incTarDmg'] = effect['amount'] + '%'
                # Reduce overwhelm effect
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'reduce_overwhelm_effect':
                        # print('reduce_overwhelm_effect')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        ab_table[upgrade['required_level']]['redOverwhelm'] = effect['amount'] + '%'
                # Increase AOE Radius
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'increase_aoe_radius':
                        # print('increase_aoe_radius')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        ab_table[upgrade['required_level']]['incAOERad'] = effect['amount'] + '%'
                # Increase AOE Radius
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'increase_stun_time':
                        # print('increase_stun_time')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        ab_table[upgrade['required_level']]['incStunTime'] = effect['amount'] + ' sec'
                # Buff Crit Chance
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'buff_crit_chance':
                        # print('buff_crit_chance')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        # print(ab_table[upgrade['required_level']])
                        # ab_table[upgrade['required_level']]['CritChance'] = effect['amount']
                        if isinstance(ab_table[upgrade['required_level']], list):
                            temp = {}
                            temp['CritChance'] = effect['amount']
                            ab_table[upgrade['required_level']].append(temp)
                        elif not 'abTitle' in ab_table[upgrade['required_level']]:
                            ab_table[upgrade['required_level']]['CritChance'] = effect['amount']
                        else:
                            temp = ab_table[upgrade['required_level']]
                            ab_table[upgrade['required_level']] = []
                            ab_table[upgrade['required_level']].append(temp)
                            temp2 = {}
                            temp2['CritChance'] = effect['amount']
                            ab_table[upgrade['required_level']].append(temp2)
                # Buff Extra attack chance
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'buff_binwin_multi_attack_chance':
                        # print('buff_binwin_multi_attack_chance')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        ab_table[upgrade['required_level']]['ExtraAtkChance'] = effect['amount']
                # Buff Upgrade base stack
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'buff_upgrade_base_stack':
                        # print('buff_upgrade_base_stack')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        # ab_table[upgrade['required_level']
                        #          ]['buff_upgrade_base_stack'] = effect['amount']
                        ab_table[upgrade['required_level']]['buff_upgrade_base_stack'] = effect['amount']
                # buff_aila_ult_bonus_dmg
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'buff_aila_ult_bonus_dmg':
                        # print('buff_aila_ult_bonus_dmg')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        ab_table[upgrade['required_level']
                                 ]['buffUlt'] = effect['amount'] + '%'
                # Calliope College of Lore
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] == 'temporary_hp_cooldown_reduce':
                        # print('buff_aila_ult_bonus_dmg')
                        if not upgrade['required_level'] in ab_table:
                            ab_table[upgrade['required_level']] = {}
                        ab_table[upgrade['required_level']
                                 ]['tempHPCDred'] = effect['amount'] + ' secs'
                # Do Nothing
                effect = None
                effect = parse_effect(upgrade['effect'])
                if effect:
                    if effect['key'] in [
                        # 'owner_killing_blow_gold_bonus',
                        # 'increase_num_unique_hits',
                        'buff_chance_attack_miss',
                        'buff_attack_stun_chance',
                        'reduce_hordesperson_drops',
                        'add_sneak_attack_hit',
                        'reduce_storm_aura_seconds',
                    ]:
                        pass

        if PRINT_TABLE is True:
            pprint(ab_table)

        if PRINT_MISSING_ROWS is True:
            print(name, 'PRINT_MISSING_ROWS')
            for upgrade in __upgrades:
                if not upgrade['required_level'] == 9999:
                    if not upgrade['required_level'] in ab_table:
                        print(upgrade)
                    if ab_table[upgrade['required_level']] == {}:
                        print(upgrade)

        #######################################################################

        # Finish abilities section
        gained_abilities = ''
        gained_abilities_template = '''
\'\'\'{ability_name} - Ability\'\'\'

{ability_description}
'''
        for entry in ab_table:
            # print(isinstance(ab_table[entry], list))
            if isinstance(ab_table[entry], list):
                for listitem in ab_table[entry]:
                    # print(listitem)
                    if ('unlockAbility' in listitem) and (not 'unlockSpec' in listitem):
                        gained_abilities += gained_abilities_template.format(
                            ability_name=listitem['abName'],
                            ability_description=listitem['abTitle'],
                        )
            elif ('unlockAbility' in ab_table[entry]) and (not 'unlockSpec' in ab_table[entry]):
                # pprint(ab_table)
                gained_abilities += gained_abilities_template.format(
                    ability_name=ab_table[entry]['abName'],
                    ability_description=ab_table[entry]['abTitle'],
                )

        # Specializations
        _specs = []
        for upgrade in js_upgrade:
            if upgrade['hero_id'] == id_:
                if 'specialization_name' in upgrade:
                    _specs.append((upgrade['specialization_name'],
                                   upgrade['specialization_description']))
        spec_1 = _specs[0][0] if len(_specs) >= 1 else ''
        spec_desc_1 = _specs[0][1] if len(_specs) >= 1 else ''
        spec_2 = _specs[1][0] if len(_specs) >= 2 else ''
        spec_desc_2 = _specs[1][1] if len(_specs) >= 2 else ''
        spec_3 = _specs[2][0] if len(_specs) >= 3 else ''
        spec_desc_3 = _specs[2][1] if len(_specs) >= 3 else ''
        spec_4 = _specs[3][0] if len(_specs) >= 4 else ''
        spec_desc_4 = _specs[3][1] if len(_specs) >= 4 else ''
        spec_5 = _specs[4][0] if len(_specs) >= 5 else ''
        spec_desc_5 = _specs[4][1] if len(_specs) >= 5 else ''
        spec_6 = _specs[5][0] if len(_specs) >= 6 else ''
        spec_desc_6 = _specs[5][1] if len(_specs) >= 6 else ''
        spec_7 = _specs[6][0] if len(_specs) >= 7 else ''
        spec_desc_7 = _specs[6][1] if len(_specs) >= 7 else ''

        if name == 'Minsc':
            abilities = abilities.format(
                a_base=a_base,
                a_base_desc=a_base_desc,
                a_ult=a_ult,
                a_ult_desc=a_ult_desc,
                spec_1=spec_1,
                spec_desc_1=spec_desc_1,
                spec_2=spec_2,
                spec_desc_2=spec_desc_2,
                spec_3=spec_3,
                spec_desc_3=spec_desc_3,
                spec_4=spec_4,
                spec_desc_4=spec_desc_4,
                spec_5=spec_5,
                spec_desc_5=spec_desc_5,
                gained_abilities=gained_abilities,
            )
        elif name == 'Asharra':
            abilities = abilities.format(
                a_base=a_base,
                a_base_desc=a_base_desc,
                a_ult=a_ult,
                a_ult_desc=a_ult_desc,
                spec_1=spec_1,
                spec_desc_1=spec_desc_1,
                spec_2=spec_2,
                spec_desc_2=spec_desc_2,
                spec_3=spec_3,
                spec_desc_3=spec_desc_3,
                spec_4=spec_4,
                spec_desc_4=spec_desc_4,
                spec_5=spec_5,
                spec_desc_5=spec_desc_5,
                spec_6=spec_6,
                spec_desc_6=spec_desc_6,
                gained_abilities=gained_abilities,
            )
        elif name == 'Tyril':
            abilities = abilities.format(
                a_base_1=a_base_1,
                a_base_1_desc=a_base_1_desc,
                a_ult_1=a_ult_1,
                a_ult_1_desc=a_ult_1_desc,
                a_base_2=a_base_2,
                a_base_2_desc=a_base_2_desc,
                a_ult_2=a_ult_2,
                a_ult_2_desc=a_ult_2_desc,
                spec_1=spec_1,
                spec_desc_1=spec_desc_1,
                spec_2=spec_2,
                spec_desc_2=spec_desc_2,
                gained_abilities=gained_abilities,
            )
        elif name in [
            'Krond',
            'Gromma',
            'Birdsong',
        ]:
            abilities = abilities.format(
                a_base=a_base,
                a_base_desc=a_base_desc,
                a_ult=a_ult,
                a_ult_desc=a_ult_desc,
                spec_1=spec_1,
                spec_desc_1=spec_desc_1,
                spec_2=spec_2,
                spec_desc_2=spec_desc_2,
                spec_3=spec_3,
                spec_desc_3=spec_desc_3,
                gained_abilities=gained_abilities,
            )
        elif name in [
            'Regis',
            'Ishi',
        ]:
            abilities = abilities.format(
                a_base=a_base,
                a_base_desc=a_base_desc,
                a_ult=a_ult,
                a_ult_desc=a_ult_desc,
                spec_1=spec_1,
                spec_desc_1=spec_desc_1,
                spec_2=spec_2,
                spec_desc_2=spec_desc_2,
                spec_3=spec_3,
                spec_desc_3=spec_desc_3,
                spec_4=spec_4,
                spec_desc_4=spec_desc_4,
                spec_5=spec_5,
                spec_desc_5=spec_desc_5,
                gained_abilities=gained_abilities,
            )
        elif name == 'Zorbu':
            abilities = abilities.format(
                a_base=a_base,
                a_base_desc=a_base_desc,
                a_ult=a_ult,
                a_ult_desc=a_ult_desc,
                spec_1=spec_1,
                spec_desc_1=spec_desc_1,
                spec_2=spec_2,
                spec_desc_2=spec_desc_2,
                spec_3=spec_3,
                spec_desc_3=spec_desc_3,
                spec_4=spec_4,
                spec_desc_4=spec_desc_4,
                spec_5=spec_5,
                spec_desc_5=spec_desc_5,
                spec_6=spec_6,
                spec_desc_6=spec_desc_6,
                spec_7=spec_7,
                spec_desc_7=spec_desc_7,
                gained_abilities=gained_abilities,
            )
        elif name == 'Wulfgar':
            abilities = abilities.format(
                a_base=a_base,
                a_base_desc=a_base_desc,
                a_ult=a_ult,
                a_ult_desc=a_ult_desc,
                spec_1=spec_1,
                spec_desc_1=spec_desc_1,
                spec_2=spec_2,
                spec_desc_2=spec_desc_2,
                spec_3=spec_3,
                spec_desc_3=spec_desc_3,
                gained_abilities=gained_abilities,
            )
        elif name == 'Walnut':
            abilities = abilities.format(
                a_base=a_base,
                a_base_desc=a_base_desc,
                a_ult=a_ult,
                a_ult_desc=a_ult_desc,
                spec_1=spec_1,
                spec_desc_1=spec_desc_1,
                spec_2=spec_2,
                spec_desc_2=spec_desc_2,
                spec_3=spec_3,
                spec_desc_3=spec_desc_3,
                spec_4=spec_4,
                spec_desc_4=spec_desc_4,
                spec_5=spec_5,
                spec_desc_5=spec_desc_5,
                gained_abilities=gained_abilities,
            )
        else:
            abilities = abilities.format(
                a_base=a_base,
                a_base_desc=a_base_desc,
                a_ult=a_ult,
                a_ult_desc=a_ult_desc,
                spec_1=spec_1,
                spec_desc_1=spec_desc_1,
                spec_2=spec_2,
                spec_desc_2=spec_desc_2,
                gained_abilities=gained_abilities,
            )
        # Finish abilities section

        #######################################################################

        table_contents = [
            'cost',
            'dmg',
            'dmg_all',
            'ult',
            'unlockAbility',
            'unlockUltimate',
            'unlockSpec',
            'abTitle',
            'abName',
            'buffUlt',
        ]

        # Wikitable
        _wikitable = '''| class="wikitable levels-table" style="text-align:center"
|-
! width="75px" | Level
! width="75px" | <abbr title="Cost of gold form previous skill-unlock to this.">Cost</abbr>
! Damage
! Damage All
'''.format(a_ult=a_ult)

        # Wikitable columns
        spec_set = []
        add_these_specs = []
        abilities_set = []
        new_columns = []

        for _upgrade in __upgrades:
            if 'specialization_name' in _upgrade:
                if _upgrade['name'] == _upgrade['specialization_name']:
                    spec_set.append(_upgrade['name'])
        ult_name = ''
        for entry in ab_table:
            if 'abName' in ab_table[entry]:
                if 'unlockUltimate' in ab_table[entry]:
                    _wikitable += '! <abbr title="Ultimate Attack">{ability_name}</abbr>\n'.format(
                        ability_name=ab_table[entry]['abName'])
                    ult_name = ab_table[entry]['abName']

        for entry in ab_table:
            if isinstance(ab_table[entry], list):
                for listitem in ab_table[entry]:
                    if ('unlockAbility' in listitem) and (not 'unlockSpec' in listitem):
                        if listitem['abName'] not in abilities_set:
                            abilities_set.append(listitem['abName'])
            elif 'abName' in ab_table[entry]:
                if ('unlockAbility' in ab_table[entry]) and (not 'unlockSpec' in ab_table[entry]):
                    if ab_table[entry]['abName'] not in abilities_set:
                        abilities_set.append(ab_table[entry]['abName'])

        # See if columns should be included
        has_entries = []
        for entry in ab_table:
            for ability in abilities_set:
                if ability in ab_table[entry]:
                    has_entries.append(ability)


        has_entries = set(has_entries)
        # print(abilities_set)
        # print(spec_set)
        # print(has_entries)

        for entry in ab_table:
            if isinstance(ab_table[entry], list):
                for listitem in ab_table[entry]:
                    if ('unlockAbility' in listitem) and (not 'unlockSpec' in listitem):
                        if listitem['abName'] in abilities_set and listitem['abName'] in has_entries:
                            _wikitable += '! {ability_name}\n'.format(ability_name=listitem['abName'])
            elif 'abName' in ab_table[entry]:
                if ('unlockAbility' in ab_table[entry]) and (not 'unlockSpec' in ab_table[entry]):
                    if (ab_table[entry]['abName'] in abilities_set) and (ab_table[entry]['abName'] in has_entries):
                        _wikitable += '! {ability_name}\n'.format(ability_name=ab_table[entry]['abName'])

        for spec in spec_set:
            for entry in ab_table:
                if spec in ab_table[entry]:
                    add_these_specs.append(spec)
        add_these_specs = set(add_these_specs)
        # print(add_these_specs)

        for spec in spec_set:
            if spec in add_these_specs:
                _wikitable += '! {ability_name}\n'.format(ability_name=spec)

        for entry in ab_table:
            if 'Health' in ab_table[entry]:
                if not 'Health' in new_columns:
                    _wikitable += '! {ability_name}\n'.format(ability_name='Health')
                if 'Health' not in new_columns:
                    new_columns.append('Health')
            if 'CritChance' in ab_table[entry]:
                if not 'CritChance' in new_columns:
                    _wikitable += '! {ability_name}\n'.format(ability_name='CritChance')
                if 'CritChance' not in new_columns:
                    new_columns.append('CritChance')
            if 'GoldFind' in ab_table[entry]:
                if not 'GoldFind' in new_columns:
                    _wikitable += '! {ability_name}\n'.format(ability_name='Gold Find')
                if 'GoldFind' not in new_columns:
                    new_columns.append('GoldFind')
            if 'add_attack_targets' in ab_table[entry]:
                if not 'add_attack_targets' in new_columns:
                    _wikitable += '! {ability_name}\n'.format(ability_name=' +Targets')
                if 'add_attack_targets' not in new_columns:
                    new_columns.append('add_attack_targets')
            if 'buff_upgrade_base_stack' in ab_table[entry]:
                if not 'buff_upgrade_base_stack' in new_columns:
                    _wikitable += '! {ability_name}\n'.format(ability_name=' Story of Doom Base Value')
                if 'buff_upgrade_base_stack' not in new_columns:
                    new_columns.append('buff_upgrade_base_stack')
            if 'spec1upg' in ab_table[entry]:
                if not 'spec1upg' in new_columns:
                    _wikitable += '! {ability_name}\n'.format(ability_name='Buff Spec 1')
                if 'spec1upg' not in new_columns:
                    new_columns.append('spec1upg')
            if 'spec2upg' in ab_table[entry]:
                if not 'spec2upg' in new_columns:
                    _wikitable += '! {ability_name}\n'.format(ability_name='Buff Spec 2')
                if 'spec2upg' not in new_columns:
                    new_columns.append('spec2upg')
            if 'specupg' in ab_table[entry]:
                if not 'specupg' in new_columns:
                    _wikitable += '! {ability_name}\n'.format(ability_name='Buff Spec')
                if 'specupg' not in new_columns:
                    new_columns.append('specupg')
            # if 'tempHPCDred' in ab_table[entry]:
            #     if not 'tempHPCDred' in new_columns:
            #         _wikitable += '! {ability_name}\n'.format(ability_name='Temp HP CD')
            #     if 'tempHPCDred' not in new_columns:
            #         new_columns.append('tempHPCDred')

        # Wikitable fields
        # print('abilities_set', abilities_set)
        # print('new_columns', new_columns)
        previous_entry = 0
        _previous_cost = 0
        totals = {'dmg': 1, 'dmg_all': 1}
        for ability in abilities_set:
            totals[ability] = 0
        for column in new_columns:
            totals[column] = 0
        for entry in ab_table:
            _cost = 0
            _rounded_cost = 0
            row = '|-' + '\n'
            row += '|' + str(entry) + '\n'
            for index in range(previous_entry - 1, entry - 1):
                if not index == -1:
                    _cost += (base_cost * pow(cost_curve, index))
                    _rounded_cost += round(base_cost * pow(cost_curve, index))
                # print(index, float(base_cost * pow(cost_curve, index)), _cost, _rounded_cost)
            if (_rounded_cost / 1000) < 1:
                cost = str(_rounded_cost)
            else:
                cost = ('{0:.2E}'.format(Decimal(_rounded_cost))).replace('E+', 'e')
            row += '|' + cost + '\n'
            previous_entry = entry
            _previous_cost = _cost
            if 'unlockSpec' in ab_table[entry]:
                colspan = 3
                if 'spec7name' in ab_table[entry]:
                    row += '| colspan={colspan} | <abbr title="{spec1} or {spec2} or {spec3} or {spec4} or {spec5} or {spec6} or {spec7}">Unlock Specialization Choice</abbr>\n'.format(
                        spec1=ab_table[entry]['spec1name'],
                        spec2=ab_table[entry]['spec2name'],
                        spec3=ab_table[entry]['spec3name'],
                        spec4=ab_table[entry]['spec4name'],
                        spec5=ab_table[entry]['spec5name'],
                        spec6=ab_table[entry]['spec6name'],
                        spec7=ab_table[entry]['spec7name'],
                        colspan=colspan
                    )
                elif 'spec6name' in ab_table[entry]:
                    row += '| colspan={colspan} | <abbr title="{spec1} or {spec2} or {spec3} or {spec4} or {spec5} or {spec6}">Unlock Specialization Choice</abbr>\n'.format(
                        spec1=ab_table[entry]['spec1name'],
                        spec2=ab_table[entry]['spec2name'],
                        spec3=ab_table[entry]['spec3name'],
                        spec4=ab_table[entry]['spec4name'],
                        spec5=ab_table[entry]['spec5name'],
                        spec6=ab_table[entry]['spec6name'],
                        colspan=colspan
                    )
                elif 'spec5name' in ab_table[entry]:
                    row += '| colspan={colspan} | <abbr title="{spec1} or {spec2} or {spec3} or {spec4} or {spec5}">Unlock Specialization Choice</abbr>\n'.format(
                        spec1=ab_table[entry]['spec1name'],
                        spec2=ab_table[entry]['spec2name'],
                        spec3=ab_table[entry]['spec3name'],
                        spec4=ab_table[entry]['spec4name'],
                        spec5=ab_table[entry]['spec5name'],
                        colspan=colspan
                    )
                elif 'spec4name' in ab_table[entry]:
                    row += '| colspan={colspan} | <abbr title="{spec1} or {spec2} or {spec3} or {spec4}">Unlock Specialization Choice</abbr>\n'.format(
                        spec1=ab_table[entry]['spec1name'],
                        spec2=ab_table[entry]['spec2name'],
                        spec3=ab_table[entry]['spec3name'],
                        spec4=ab_table[entry]['spec4name'],
                        colspan=colspan
                    )
                elif 'spec3name' in ab_table[entry]:
                    row += '| colspan={colspan} | <abbr title="{spec1} or {spec2} or {spec3}">Unlock Specialization Choice</abbr>\n'.format(
                        spec1=ab_table[entry]['spec1name'],
                        spec2=ab_table[entry]['spec2name'],
                        spec3=ab_table[entry]['spec3name'],
                        colspan=colspan
                    )
                else:
                    row += '| colspan={colspan} | <abbr title="{spec1} or {spec2}">Unlock Specialization Choice</abbr>\n'.format(
                        spec1=ab_table[entry]['spec1name'],
                        spec2=ab_table[entry]['spec2name'],
                        colspan=colspan
                    )
            elif isinstance(ab_table[entry], list) and any('unlockAbility' in x for x in ab_table[entry]):
                didit = False
                colspan = len(has_entries) + len(new_columns) + len(add_these_specs) + 3
                row += '| colspan={colspan} | Unlock '.format(colspan=colspan)
                for listitem in ab_table[entry]:
                    if 'unlockAbility' in listitem:
                        didit = True
                        row += '<abbr title="{ability_title}">{ability_name}</abbr> or '.format(
                            ability_name=listitem['abName'],
                            ability_title=listitem['abTitle'].replace('"', "'") if 'abTitle' in listitem else '',
                            colspan=colspan
                        )
                if didit:
                    row = row[:-4]
                row += '\n'
            elif 'unlockAbility' in ab_table[entry]:
                colspan = len(has_entries) + len(new_columns) + len(add_these_specs) + 3
                row += '| colspan={colspan} | <abbr title="{ability_title}">Unlock {ability_name}</abbr>\n'.format(
                    ability_name=ab_table[entry]['abName'],
                    ability_title=ab_table[entry]['abTitle'] if 'abTitle' in ab_table[entry] else '',
                    colspan=colspan
                )
            elif 'unlockUltimate' in ab_table[entry]:
                colspan = len(has_entries) + len(new_columns) + len(add_these_specs) + 3
                row += '| colspan={colspan} | <abbr title="{ability_title}">Unlock {ability_name}</abbr>\n'.format(
                    ability_name=ab_table[entry]['abName'],
                    ability_title=ab_table[entry]['abTitle'] if 'abTitle' in ab_table[entry] else '',
                    colspan=colspan
                )
            else:
                dmg_num = re.search('(\d+)' , ab_table[entry]['dmg']).group() if 'dmg' in ab_table[entry] else 0
                totals['dmg'] *= (int(float(dmg_num) / 100) + 1) if 'dmg' in ab_table[entry] else 1
                row += '|' + (ab_table[entry]['dmg'] if 'dmg' in ab_table[entry] else '') + '\n'
                dmgall_num = re.search('(\d+)' , ab_table[entry]['dmg_all']).group() if 'dmg_all' in ab_table[entry] else 0
                totals['dmg_all'] *= (int(float(dmgall_num) / 100) + 1) if 'dmg_all' in ab_table[entry] else 1
                row += '|' + (ab_table[entry]['dmg_all']
                              if 'dmg_all' in ab_table[entry] else '') + '\n'
                row += '|' + (ab_table[entry]['buffUlt']
                              if 'buffUlt' in ab_table[entry] else '') + '\n'
            if isinstance(ab_table[entry], list):
                for listitem in ab_table[entry]:
                    if ('unlockSpec' in listitem) or (not 'unlockAbility' in listitem) or (not 'unlockUltimate' in listitem):
                        # print('entry', listitem)
                        doit = True
                    if 'unlockAbility' in listitem or 'unlockUltimate' in listitem:
                        doit = False
            else:
                if ('unlockSpec' in ab_table[entry]) or (not 'unlockAbility' in ab_table[entry]) or (not 'unlockUltimate' in ab_table[entry]):
                    # print('entry', ab_table[entry])
                    doit = True
                if 'unlockAbility' in ab_table[entry] or 'unlockUltimate' in ab_table[entry]:
                    doit = False

            if doit == True:
                for ability in abilities_set:
                    if ability in has_entries:
                        # print('building wikitable (ability):', ability)
                        if isinstance(ab_table[entry], list):
                            # print('building wikitable (if):', ab_table[entry])
                            # row += '|' + '\n'
                            row += '|'
                            didit = False
                            for listitem in ab_table[entry]:
                                if ability in listitem:
                                    row += listitem[ability] + '\n'
                                    didit = True
                            if didit:
                                row = row[:-1]
                            row += '\n'
                        elif ability in ab_table[entry]:
                            # print('building wikitable (elif):', ab_table[entry])
                            row += '|' + ab_table[entry][ability] + '\n'
                        else:
                            # print('building wikitable (else):', ab_table[entry])
                            row += '|' + '\n'
                for spec in spec_set:
                    if spec in add_these_specs:
                        if spec in ab_table[entry]:
                            row += '|' + ab_table[entry][spec] + '\n'
                        else:
                            row += '|' + '\n'
                if len(new_columns) > 0:
                    for column in new_columns:
                        # print('building wikitable (column):', ability)
                        if isinstance(ab_table[entry], list):
                            # print('building wikitable (if):', ab_table[entry])
                            # row += '|' + '\n'
                            row += '|'
                            didit = False
                            for listitem in ab_table[entry]:
                                if column in listitem:
                                    row += listitem[column] + '\n'
                                    didit = True
                            if didit:
                                row = row[:-1]
                            row += '\n'
                        elif column in ab_table[entry]:
                            # print('building wikitable (elif):', ab_table[entry])
                            row += '|' + ab_table[entry][column] + '\n'
                        else:
                            # print('building wikitable (else):', ab_table[entry])
                            row += '|' + '\n'

            _wikitable += row



        for entry in ab_table:
            row = '|-' + 'style="background:#181818;border:4px;border-top-style:double"' + '\n'
            row += '|' + '\'\'\'Total:\'\'\'' + '\n'
            row += '|' + '\n'
            _dmg = (totals['dmg'] - 1) * 100
            if (_dmg / 10000) >= 1:
                _dmg = ('{0:.2E}'.format(Decimal(_dmg))).replace('E+', 'e')
            row += '|' + \
                '<onlyinclude>{{{{#ifeq:{{{{{{include|damage}}}}}}|damage|{dmg}%}}}}</onlyinclude>'.format(
                    dmg=_dmg) + '\n'
            _dmg_all = (totals['dmg_all'] - 1) * 100
            if (_dmg_all / 10000) >= 1:
                _dmg_all = ('{0:.2E}'.format(Decimal(_dmg_all))).replace('E+', 'e')
            row += '|' + \
                '<onlyinclude>{{{{#ifeq:{{{{{{include|damageAll}}}}}}|damageAll|{dmg_all}%}}}}</onlyinclude>'.format(
                    dmg_all=_dmg_all) + '\n'
            for ability in has_entries:
                row += '|' + '\n'
            for spec in spec_set:
                if spec in add_these_specs:
                    row += '|' + '\n'
            if len(new_columns) > 0:
                for column in new_columns:
                    row += '|' + '\n'
            row += '|' + '\n'

        _wikitable += row

        # Wikitable end
        _wikitable += '|}'
        _wikitable = '{' + _wikitable

        # Equipment
        eq_table = {
            'slot1': {'desc': 0, '1': 0, '2': 0, '3': 0, '4': 0},
            'slot2': {'desc': 0, '1': 0, '2': 0, '3': 0, '4': 0},
            'slot3': {'desc': 0, '1': 0, '2': 0, '3': 0, '4': 0},
            'slot4': {'desc': 0, '1': 0, '2': 0, '3': 0, '4': 0},
            'slot5': {'desc': 0, '1': 0, '2': 0, '3': 0, '4': 0},
            'slot6': {'desc': 0, '1': 0, '2': 0, '3': 0, '4': 0},
        }
        for loot in js_loot:
            if loot['hero_id'] == id_:
                # print(loot['hero_id'])
                # print(loot)
                slot_id = 'slot' + str(loot['slot_id'])
                rarity = loot['rarity']
                # desc = loot['description']
                desc = ''
                effect = None
                effect = parse_effect(loot['effects'][0]['effect_string'])
                # print(effect)
                effect_amt = effect['amount']
                if '.' in effect_amt:
                    effect_amt = float(effect_amt.replace('%', '').replace(' sec', ''))
                else:
                    effect_amt = int(effect_amt.replace('%', '').replace(' sec', ''))
                effect_key = effect['key']
                # print(effect)
                for _effect_key in js_effect_key:
                    if _effect_key['key'] == effect_key:
                        desc = _effect_key['descriptions']['desc']
                        if ('$amount%' in desc) or ('$(amount)%' in desc):
                            unit = '%'
                        elif ('$amount seconds' in desc) or ('$(amount) seconds' in desc):
                            unit = ' sec'
                if effect_key == 'buff_upgrades':
                    if 'description' in loot['effects'][0]:
                        desc = loot['effects'][0]['description']
                ability_list = ''
                if not spec_1 == '':
                    ability_list += (spec_1 + ' and ')
                if not spec_2 == '':
                    ability_list += (spec_2 + ' and ')
                if not spec_3 == '':
                    ability_list += (spec_3 + ' and ')
                if not spec_4 == '':
                    ability_list += (spec_4 + ' and ')
                if not spec_5 == '':
                    ability_list += (spec_5 + ' and ')
                if not spec_6 == '':
                    ability_list += (spec_6 + ' and ')
                if not spec_7 == '':
                    ability_list += (spec_7 + ' and ')
                ability_list = ability_list[:-4]
                ability_list += 'abilities'
                desc = desc\
                    .replace('$target', name)\
                    .replace('$(upgrade_hero id)', name)\
                    .replace('$(upgrade_hero ids)', name)\
                    .replace('$(upgrade_name id)', effect['name'] if 'name' in effect else '')\
                    .replace('$(attack_names_and attack_ids)', 'Krond\'s Cantrip abilities')\
                    .replace(' $amount%', '')\
                    .replace(' $(amount)%', '')\
                    .replace(' $amount seconds', '')\
                    .replace(' $(amount) seconds', '')\
                    .replace('$(ability_list ids)', ability_list)\
                    .replace('Wild Shape', 'Wild Inspiration')  # Tyril
                # .replace(' $(upgrade_name id)', name)

                if desc[-1:] == '.':
                    desc = desc[:-1]
                eq_table[slot_id]['desc'] = desc
                # print(desc)
                eq_table[slot_id][str(rarity)] = str(effect_amt) + unit
                shiny_effect_amt = effect_amt * 1.5
                if shiny_effect_amt - int(shiny_effect_amt) == 0:
                    shiny_effect_amt = str(int(shiny_effect_amt))
                else:
                    shiny_effect_amt = str(float(shiny_effect_amt))
                golden_effect_amt = effect_amt * 2
                if golden_effect_amt - int(golden_effect_amt) == 0:
                    golden_effect_amt = str(int(golden_effect_amt))
                else:
                    golden_effect_amt = str(float(golden_effect_amt))
                eq_table[slot_id][str(rarity + 4)] = shiny_effect_amt + unit
                eq_table[slot_id][str(rarity + 8)] = golden_effect_amt + unit
        # pprint(eq_table)
        equipment = '''{| class="wikitable"
!Slot
!Description
!<span style="background:#202020; border: #bad6e8; border-style: solid; border-width: 0px; padding: inherit;"><span style="color: #ffffff>Common</span></span>
!<span style="background:#202020; border: #bad6e8; border-style: solid; border-width: 0px; padding: inherit;"><span style="color: #53e105>Uncommon</span></span>
!<span style="background:#202020; border: #bad6e8; border-style: solid; border-width: 0px; padding: inherit;"><span style="color: #2a8cfa>Rare</span></span>
!<span style="background:#202020; border: #bad6e8; border-style: solid; border-width: 0px; padding: inherit;"><span style="color: #a200ff>Epic</span></span>
!<span style="background:#202020; border: #bad6e8; border-style: solid; border-width: 1px; padding: inherit;"><span style="color: #bad6e8>Shiny</span> <span style="color: #ffffff>Common</span></span>
!<span style="background:#202020; border: #bad6e8; border-style: solid; border-width: 1px; padding: inherit;"><span style="color: #bad6e8>Shiny</span> <span style="color: #53e105>Uncommon</span></span>
!<span style="background:#202020; border: #bad6e8; border-style: solid; border-width: 1px; padding: inherit;"><span style="color: #bad6e8>Shiny</span> <span style="color: #2a8cfa>Rare</span></span>
!<span style="background:#202020; border: #bad6e8; border-style: solid; border-width: 1px; padding: inherit;"><span style="color: #bad6e8>Shiny</span> <span style="color: #a200ff>Epic</span></span>
!<span style="background:#202020; border: #fccc3b; border-style: solid; border-width: 1px; padding: inherit;"><span style="color: #fccc3b>Golden</span> <span style="color: #a200ff>Epic</span></span>
|-
|1
|''' + eq_table['slot1']['desc'] + '''
|''' + eq_table['slot1']['1'] + '''
|''' + eq_table['slot1']['2'] + '''
|''' + eq_table['slot1']['3'] + '''
|''' + eq_table['slot1']['4'] + '''
|''' + eq_table['slot1']['5'] + '''
|''' + eq_table['slot1']['6'] + '''
|''' + eq_table['slot1']['7'] + '''
|''' + eq_table['slot1']['8'] + '''
|''' + eq_table['slot1']['12'] + '''
|-
|2
|''' + eq_table['slot2']['desc'] + '''
|''' + eq_table['slot2']['1'] + '''
|''' + eq_table['slot2']['2'] + '''
|''' + eq_table['slot2']['3'] + '''
|''' + eq_table['slot2']['4'] + '''
|''' + eq_table['slot2']['5'] + '''
|''' + eq_table['slot2']['6'] + '''
|''' + eq_table['slot2']['7'] + '''
|''' + eq_table['slot2']['8'] + '''
|''' + eq_table['slot2']['12'] + '''
|-
|3
|''' + eq_table['slot3']['desc'] + '''
|''' + eq_table['slot3']['1'] + '''
|''' + eq_table['slot3']['2'] + '''
|''' + eq_table['slot3']['3'] + '''
|''' + eq_table['slot3']['4'] + '''
|''' + eq_table['slot3']['5'] + '''
|''' + eq_table['slot3']['6'] + '''
|''' + eq_table['slot3']['7'] + '''
|''' + eq_table['slot3']['8'] + '''
|''' + eq_table['slot3']['12'] + '''
|-
|4
|''' + eq_table['slot4']['desc'] + '''
|''' + eq_table['slot4']['1'] + '''
|''' + eq_table['slot4']['2'] + '''
|''' + eq_table['slot4']['3'] + '''
|''' + eq_table['slot4']['4'] + '''
|''' + eq_table['slot4']['5'] + '''
|''' + eq_table['slot4']['6'] + '''
|''' + eq_table['slot4']['7'] + '''
|''' + eq_table['slot4']['8'] + '''
|''' + eq_table['slot4']['12'] + '''
|-
|5
|''' + eq_table['slot5']['desc'] + '''
|''' + eq_table['slot5']['1'] + '''
|''' + eq_table['slot5']['2'] + '''
|''' + eq_table['slot5']['3'] + '''
|''' + eq_table['slot5']['4'] + '''
|''' + eq_table['slot5']['5'] + '''
|''' + eq_table['slot5']['6'] + '''
|''' + eq_table['slot5']['7'] + '''
|''' + eq_table['slot5']['8'] + '''
|''' + eq_table['slot5']['12'] + '''
|-
|6
|''' + eq_table['slot6']['desc'] + '''
|''' + eq_table['slot6']['1'] + '''
|''' + eq_table['slot6']['2'] + '''
|''' + eq_table['slot6']['3'] + '''
|''' + eq_table['slot6']['4'] + '''
|''' + eq_table['slot6']['5'] + '''
|''' + eq_table['slot6']['6'] + '''
|''' + eq_table['slot6']['7'] + '''
|''' + eq_table['slot6']['8'] + '''
|''' + eq_table['slot6']['12'] + '''
|}
'''
        if name == 'Bruenor':
            equipment += '''
===Golden Gear===
* Slot 1: Received from buying normal gold chests with real money the first time.
* Slot 2: Received from buying the [http://store.steampowered.com/app/714850/Idle_Champions_of_the_Forgotten_Realms__Bruenors_Starter_Pack/ Bruenor's Starter Pack].
'''
        elif name == 'Celeste':
            equipment += '''
===Golden Gear===
* Slot 1: Received from buying the [http://store.steampowered.com/app/714860/Idle_Champions_of_the_Forgotten_Realms__Celestes_Starter_Pack/ Celeste's Starter Pack].
'''
        elif name == 'Nayeli':
            equipment += '''
===Golden Gear===
* Slot 1: Received from buying the [http://store.steampowered.com/app/714861/Idle_Champions_of_the_Forgotten_Realms__Nayelis_Starter_Pack/ Nayeli's Starter Pack].
'''
        elif name == 'Nayeli':
            equipment += '''
===Golden Gear===
* Slot 1: Received from buying the [http://store.steampowered.com/app/714861/Idle_Champions_of_the_Forgotten_Realms__Nayelis_Starter_Pack/ Nayeli's Starter Pack].
'''
        elif name == 'Stoki':
            equipment += '''
===Golden Gear===
* Slot 2: Received from buying event chest's during the first [[Highharvestide]] Event.
'''
        elif name == 'Gromma':
            equipment += '''
===Golden Gear===
* Slot 4: Received from buying event chest's during the first [[Feast of the Moon]] Event.
'''
        elif name == 'Strix':
            equipment += '''
===Golden Gear===
* Slot 1: Received from buying Buff Weekend Chest
* Slot 3: Received from buying Festival of Fools gold chests with real money the first time.
'''
        elif name == 'Evelyn':
            equipment += '''
===Golden Gear===
* Slot 2: Received from buying [[The Great Modron March]] gold chests with real money the first time.
'''
        elif name == 'Donaar':
            equipment += '''
===Golden Gear===
* Slot 4: Gotten by buying multiple Gold Donaar Chests on the 2018 [[Liar's Night]] Event.
'''

        # Trivia
        trivia = ''
        if name == 'Minsc':
            trivia += '''
* Minsc (and Boo) was the first Champion to be revealed.
* Hovering over his Strength Stat will show "18/93". Older D&D rules interpret this as 18 strength, 93 percentile. This was because AD&D set 18 as the upper limit for all stats, with a percentile score representing strength higher than 18. In short, Minsc is very strong.
'''
        elif name == 'Tyril':
            trivia += '''
Created by Actor and Entrepreneur Dylan Sprouse.
'''
        elif name == 'Evelyn':
            trivia += '''
Evelyn's full name, according to creator Anna Prosser Robinson, is Evelyn Avalona Helvig Marthain.
'''
        elif name == 'Binwin':
            trivia += '''
Binwin is in the webcomic [http://tabletitans.com/binwins-minions Binwin's Minions], which is part of the [http://tabletitans.com/comics Table Titans] webcomic series.
'''
        elif name == 'Donaar':
            trivia += '''
Donaar is played by Ryan Hartman.
'''
        elif name == 'Spurt':
            trivia += '''
Spurt is based on Dungeons & Dragons designer Chris Perkins' guest character on the live-stream show [https://www.youtube.com/channel/UCpXBGqwsBkpvcYjsJBQ7LEQ Critical Role].
'''
        elif name == 'Vlahnya':
            trivia += '''
Vlahnya is based on [https://www.mazearcana.com/ Maze Arcana] dungeon master and former Community Manager for Dungeons & Dragons, Satine Phoenix.
'''

        # Media
        media = ''
        for num in range(1, 6):
            media += '{{{{#ifexist: File:{name}{num}.jpg | [[File:{name}{num}.jpg|350px|inline]] |}}}}\n'.format(
                name=name,
                num=f'{num:03}',
            )
            media += '{{{{#ifexist: File:{name}{num}.png | [[File:{name}{num}.png|350px|inline]] |}}}}\n'.format(
                name=name,
                num=f'{num:03}',
            )

        # Stubs
        # if name == 'Spurt':
        #     champ_str = '{{{{stub}}}}' + champ_str

        final_str = champ_str.format(
            id_=id_,
            name=name,
            skin=skin,
            class_=class_,
            race=race,
            age=age,
            alignment=alignment,
            str_=str_,
            dex=dex,
            con=con,
            int_=int_,
            wis=wis,
            cha=cha,
            fullname=fullname,
            backstory=backstory,
            extra_info=extra_info,
            group=group,
            b_cd=b_cd,
            u_cd=u_cd,
            swap1=swap1,
            swap2=swap2,
            swap3=swap3,
            swap4=swap4,
            abilities=abilities,
            wikitable=_wikitable,
            spec_1=spec_1,
            spec_2=spec_2,
            spec_desc_1=spec_desc_1,
            spec_desc_2=spec_desc_2,
            equipment=equipment,
            trivia=trivia,
            media=media,
        )

        with open('output/{filename}.txt'.format(filename=name), 'w') as f:
            f.write(html.unescape(final_str))

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
                print('{name}: Changes detected!'.format(name=name))
                if SHOW_CHANGES:
                    result = subprocess.run(['git', 'diff', '--no-index', posted_file, main_file])
                if POST:
                    if _summary is None:
                        _summary = input('Enter change summary: ')
                    EDIT_PARAMS = {
                        'action': 'edit',
                        'title': name,
                        'text': final_str,
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
                                g.write(final_str)
                        else:
                            print('{name}: FAIL! Error Message: {error}'.format(name=name, error=R2.json()['error']['info']))
                    # if R2.status_code == 200:
                    #     print('{name}: Success!'.format(name=name))
                    #     with open('output/posted/{filename}.txt'.format(filename=name), 'w') as g:
                    #         g.write(final_str)
                    else:
                        print('{name}: FAIL!'.format(name=name))

        if id_ == 32:
            exit()
        # break
