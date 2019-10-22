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

__js_adv = sorted(js_adv, key=lambda x: x['id'])
__js_adv = sorted(__js_adv, key=lambda x: x['area_set_id'])
__js_adv = sorted(__js_adv, key=lambda x: x['location_id'])
__js_adv = sorted(__js_adv, key=lambda x: x['campaign_id'])

__js_area = sorted(js_area, key=lambda x: x['id'])
__js_area = sorted(__js_area, key=lambda x: x['area_id'])
__js_area = sorted(__js_area, key=lambda x: x['area_set_id'])
# pprint(__js_area)

__js_mon = sorted(js_mon, key=lambda x: x['id'])

# pprint(__js_adv)
set_advs = set()


def addtomonlist(dict_, m_id):
    for monster in __js_mon:
        if monster['id'] == m_id:
            if monster['name'] not in dict_:
                dict_[monster['name']] = []
            if sorted(set(monster['tags'])) not in dict_[monster['name']]:
                if dict_[monster['name']] == []:
                    dict_[monster['name']].append(sorted(set(monster['tags'])))
                else:
                    for tag in sorted(set(monster['tags'])):
                        if tag not in dict_[monster['name']][0]:
                            dict_[monster['name']][0].append(tag)
            # print(dict_)
            # print(monster, m_id, monster['name'])


footer = '''
{{Navbox-Adventures}}
{{Navbox-IdleChampions}}

[[Category:Adventures]]'''

footer_event = '''
{{Navbox-Adventures | event_state=expanded | locations_state = collapsed}}
{{Navbox-IdleChampions}}

[[Category:Events]] [[Category:Adventures]]'''


for adv in __js_adv:
    if adv['id'] not in set_advs:
        set_advs.add(adv['id'])
        # print(json.dumps(adv))
        page_text = ''
        adv_text = ''
        # print(adv['id'], adv['name'])
        # print(adv['campaign_id'], adv['location_id'], adv['area_set_id'])
        # print('Description:', adv['description'])
        # print('Requirements:', adv['requirements_text'])
        # print('Objectives:', adv['objectives_text'])
        # print('Restrictions:', adv['restrictions_text'])
        # if not adv['rewards'] == []:
        #     print('Rewards:', adv['rewards'])
        #     if 'amount' in adv['rewards'][0]:
        #         print('Rewards:', adv['rewards'][0]['reward'] + ': ' + str(adv['rewards'][0]['amount']))
        #     elif 'crusader_id' in adv['rewards'][0]:
        #         print('Rewards:', adv['rewards'][0]['reward'] + ': ' + str(adv['rewards'][0]['crusader_id']))
        # if not adv['costs'] == []:
        #     print('Costs:', adv['costs'])
        # print('\n')

        # if adv['name'] == 'Free Play'

        adv_text += ('<onlyinclude><!--\n-->')
        adv_text += ('{{AdventureNew' + '\n')
        name = adv['name']
        if name == 'Free Play':
            for _adv in __js_adv:
                if adv['variant_adventure_id'] == _adv['id']:
                    name = _adv['name'] + ' ' + name
                    adv_text += ('| icon = ' + _adv['name'] + '\n')
        elif 'Free Play (' in name:
            for _adv in __js_adv:
                if adv['variant_adventure_id'] == _adv['id']:
                    adv_text += ('| icon = ' + _adv['name'] + '\n')
        adv_text += ('| name = ' + name + '\n')
        adv_text += ('| description = ' + adv['description'] + '\n')
        requirements = adv['requirements_text']
        # print('1__', requirements)
        requirements = requirements.replace('\r\n', '\n')
        result1 = re.search('.*"(.*)"', requirements, re.MULTILINE | re.DOTALL)
        if result1:
            if result1.group(1) in [
                'A Brief Escort through the Realm',
                'A Brief Tour of the Realm',
            ]:
                replacement = '[[' + result1.group(1) + 's]]'
            else:
                replacement = '[[' + result1.group(1) + ']]'
            requirements = requirements.replace(result1.group(1), replacement)
            # print('2__', requirements)
        result2 = re.search('((Costs|Costs up to|Must have) \d+ (\w*.*)s to start)', requirements, re.MULTILINE | re.DOTALL)
        if result2:
            requirements = requirements.replace(result2.group(1), '')
            requirements = requirements[:-1]
        # requirements = requirements.replace('<br>', '\n')
        adv_text += ('| requirements = ' + requirements + '\n')
        if not adv['costs'] == []:
            if adv['costs'][0]['cost'] == 'event_tokens':
                adv_text += ('| cost = ' + str(adv['costs'][0]['amount']) + '\n')
                # if adv['costs'][0]['event_id'] == 18:
                #     adv_text += ('| cost_type = ' + result2.group(2) + '\n')
                # if adv['costs'][0]['event_id'] == 23:
                # print('__3', requirements)
                # print('__3', name)
                adv_text += ('| cost_type = ' + result2.group(3) + '\n')
        adv_text += ('| objectives = ' + adv['objectives_text'] + '\n')
        adv_text += ('| restrictions = ' + adv['restrictions_text'] + '\n')
        if not adv['rewards'] == []:
            for reward in adv['rewards']:
                if reward['reward'] == 'red_rubies':
                    adv_text += ('| gems = ' + str(reward['amount']) + '\n')
                elif reward['reward'] == 'claim_crusader':
                    for hero in js_hero:
                        if reward['crusader_id'] == hero['id']:
                            adv_text += ('| championreward = ' + hero['name'] + '\n')
                elif reward['reward'] == 'chest':
                    if 'chest_type_id' in reward:
                        for chest in js_chest_type:
                            if chest['id'] == reward['chest_type_id']:
                                adv_text += ('| chest = {{ChestNew|name=' +
                                             chest['name'] + '}}' + '\n')
                    elif 'chest_type_ids' in reward:
                        for enum, chest_choice in enumerate(reward['chest_type_ids']):
                            for chest in js_chest_type:
                                if chest['id'] == chest_choice:
                                    one_chest = chest['name']
                                    one_chance = str(reward['chest_odds'][enum]) + '%'
                                    adv_text += ('| chest' + str(enum + 1) +
                                                 '= {{ChestNew|name=' + one_chest + '|chance=' + one_chance + '}}' + '\n')
        if adv['campaign_id'] == 1:
            adv_text += ('| favor = ' + 'Torm' + '\n')
        elif adv['campaign_id'] == 2:
            adv_text += ('| favor = ' + 'Chauntea' + '\n')
        elif adv['campaign_id'] == 3:
            adv_text += ('| favor = ' + 'Kelemvor' + '\n')
        elif adv['campaign_id'] == 4:
            adv_text += ('| favor = ' + 'Leira' + '\n')
        elif adv['campaign_id'] == 5:
            adv_text += ('| favor = ' + 'Jergal' + '\n')
        elif adv['campaign_id'] == 6:
            adv_text += ('| favor = ' + 'Shar' + '\n')
        elif adv['campaign_id'] == 7:
            adv_text += ('| favor = ' + 'Oghma' + '\n')
        elif adv['campaign_id'] == 8:
            adv_text += ('| favor = ' + 'Auril' + '\n')
        elif adv['campaign_id'] == 9:
            adv_text += ('| favor = ' + 'Sune' + '\n')
        elif adv['campaign_id'] == 10:
            adv_text += ('| favor = ' + 'Umberlee' + '\n')
        elif adv['campaign_id'] == 11:
            adv_text += ('| favor = ' + 'Lliira' + '\n')
        elif adv['campaign_id'] == 12:
            adv_text += ('| favor = ' + 'Lathander' + '\n')
        elif adv['campaign_id'] == 13:
            adv_text += ('| favor = ' + 'Rillifane' + '\n')
        elif adv['campaign_id'] == 14:
            adv_text += ('| favor = ' + 'Gond' + '\n')
        elif adv['campaign_id'] == 15:
            adv_text += ('| favor = ' + 'Helm' + '\n')
        elif adv['campaign_id'] == 16:
            adv_text += ('| favor = ' + 'Waukeen' + '\n')
        elif adv['campaign_id'] == 17:
            adv_text += ('| favor = ' + 'Mystra' + '\n')
        elif adv['campaign_id'] == 18:
            adv_text += ('| favor = ' + 'Asmodeus' + '\n')
        elif adv['campaign_id'] == 19:
            adv_text += ('| favor = ' + 'Savra' + '\n')
        elif adv['campaign_id'] == 20:
            adv_text += ('| favor = ' + 'Azuth' + '\n')
        elif adv['campaign_id'] == 21:
            adv_text += ('| favor = ' + 'Tempus' + '\n')
        second_formation_logic = True
        if 'game_changes' in adv:
            check_for_formation_and_altered = set()
            for change in adv['game_changes']:
                check_for_formation_and_altered.add(change['type'])
                if 'name' in change:
                    formation = change['name'].replace(' formation', '').replace(' Formation', '')
            if any(
                y in check_for_formation_and_altered for y in [
                    'slot_escort',
                    'blocked_heroes_by_area',
                    'slot_escort_by_area',
                    'initial_formation',
                ]
            ):
                # print('Altered Formation')
                formation = name.replace(' formation', '').replace(' Formation', '')
                adv_text += ('| formation = ' + formation + '\n')
                second_formation_logic = False
            elif 'formation' in check_for_formation_and_altered:
                adv_text += ('| formation = ' + formation + '\n')
                second_formation_logic = False

        if second_formation_logic:
            for campaign in js_camp:
                # print(campaign['id'])
                # print(adv['campaign_id'])
                if campaign['id'] == int(adv['campaign_id']):
                    for change in campaign['game_changes']:
                        if change['type'] == 'formation':
                            if not change['name'] == 'Overwritten formation':
                                formation = change['name'].replace(
                                    ' formation', '').replace(' Formation', '')
                                adv_text += ('| formation = ' + formation + '\n')

        adv_text += '}}'
        adv_text += '<!--\n--></onlyinclude>'

        # print(adv_text)
        # print()

        intro = '\'\'\'{adv_name}\'\'\' is {adv_or_var} in the campaign [[{campaign}]].'
        for campaign in js_camp:
            if adv['campaign_id'] == campaign['id']:
                camp_name = campaign['name']
        if 'variant_adventure_id' in adv:
            for _adv in __js_adv:
                if adv['variant_adventure_id'] == _adv['id']:
                    _name = _adv['name']
            intro_text = intro.format(
                adv_name=name,
                adv_or_var='one of the [[Variant]] [[Adventures]] of [[{_name}]]'.format(
                    _name=_name),
                campaign=camp_name,
            )
        else:
            intro_text = intro.format(
                adv_name=name,
                adv_or_var='one of the [[Adventures]]',
                campaign=camp_name,
            )
        page_text = intro_text + page_text + '\n'

        page_text += adv_text

        variant_text = '<ul class="hlist">'
        _set_advs = set()
        for _adv in __js_adv:
            if _adv['id'] not in _set_advs:
                _set_advs.add(_adv['id'])
                if 'variant_adventure_id' in _adv:
                    if _adv['variant_adventure_id'] == adv['id']:
                        _name = _adv['name']
                        if _name == 'Free Play':
                            _name = adv['name'] + ' ' + _name
                        variant_text += ('\n' + '<li>' +
                                         '{{{{:{name}}}}}'.format(name=_name) + '</li>')
        variant_text += ('\n' + '</ul>')
        if not variant_text == '<ul class="hlist">\n</ul>':
            variant_text = '\n' + '{{clear}}' + '\n' + '==Variants==' + '\n' + variant_text
            page_text += variant_text

        # print(page_text)
        # print()

        ######

        mobtable = '''\n\n==Wave Information==
{| class="wikitable"
!Area
!Monsters
!Types'''

        set_areas = set()
        for area in __js_area:
            # print(set_areas)
            if area['area_set_id'] == adv['area_set_id']:
                if area['id'] not in set_areas:
                    set_areas.add(area['id'])
                    # print(area['id'])
                    if 'monsters' in area:
                        # print(area['monsters'])
                        if 'properties' in area:
                            if 'monster_spawners' in area['properties']:
                                # print(area['properties']['monster_spawners'])
                                if not area['properties']['monster_spawners'] == {}:
                                    for key in area['properties']['monster_spawners']:
                                        # temp = area['properties']['monster_spawners']
                                        # print(area['properties'])
                                        # spawner = temp.popitem()[0]
                                        # print('monster_spawners', spawner, end='')
                                        pass
                                        # print('monster_spawners', key, end='')
                                elif 'monster_generators' in area['properties']:
                                    if not area['properties']['monster_generators'] == {}:
                                        for key in area['properties']['monster_generators']:
                                            # temp = area['properties']['monster_generators']
                                            # print(area['properties'])
                                            # spawner = temp.popitem()[1]
                                            # print('monster_generators', spawner, end='')
                                            pass
                                            # print('monster_generators', key, end='')
                        monlist = {}
                        mobtable += ('\n' + '|-')
                        mobtable += ('\n' + '|' + str(area['area_id']))
                        static_boss = False
                        static_bosses = {}
                        for monster in area['monsters']:
                            for _monster in __js_mon:
                                if monster == _monster['id']:
                                    addtomonlist(monlist, _monster['id'])
                        if area['monsters'] == []:
                            # print('Detected unsuality', '<' + ('~'*100))
                            if 'properties' in area:
                                if 'include_monster_defs' in area['properties']:
                                    for mob_id in area['properties']['include_monster_defs']:
                                        for _monster in __js_mon:
                                            if (mob_id == _monster['id']) and (not mob_id == 1):
                                                addtomonlist(monlist, _monster['id'])
                                                # print(monlist)
                                if 'static_monsters' in area['properties']:
                                    for static_mon in area['properties']['static_monsters']:
                                        addtomonlist(
                                            static_bosses, area['properties']['static_monsters'][static_mon]['monster_id'])
                                        static_boss = True
                        elif not area['monsters'] == []:
                            if 'properties' in area:
                                if 'static_monsters' in area['properties']:
                                    for static_mon in area['properties']['static_monsters']:
                                        if 'boss' in area['properties']['static_monsters'][static_mon]:
                                            addtomonlist(
                                                static_bosses, area['properties']['static_monsters'][static_mon]['monster_id'])
                                            static_boss = True
                        monlist_text = ''
                        typelist = set()
                        for listitem in sorted(monlist):
                            monlist_text += ('[[' + listitem + ']]' + ', ')
                            for _type in monlist[listitem]:
                                for __type in _type:
                                    typelist.add(__type)
                        monlist_text = monlist_text[:-2]
                        mobtable += ('\n' + '|' + monlist_text)

                        # Types
                        for wave in sorted(monlist):
                            typestring = ''
                            for _type in sorted(typelist):
                                    # typestring += (_type.title() + ', ')
                                typestring += ('{{TypeTag|' + _type + '}}')
                            # typestring = typestring[:-2]
                        mobtable += ('\n' + '|' + typestring)

                        if static_boss == True:

                            # Boss
                            typelist = set()
                            mobtable += '\n' + '|-'
                            mobtable += ('\n' + '|' + '\'\'\'Boss\'\'\'')
                            mobtable += ('\n' + '|')
                            for boss in sorted(static_bosses):
                                # print(boss)
                                mobtable += ('\'\'\'[[' + boss + ']]\'\'\'' + ', ')
                                for _type in static_bosses[boss]:
                                    for __type in _type:
                                        # print(typelist)
                                        # print(boss, __type)
                                        typelist.add(__type)
                            mobtable = mobtable[:-2]

                            # Types
                            for boss in sorted(static_bosses):
                                typestring = ''
                                for _type in sorted(typelist):
                                    # typestring += (_type.title() + ', ')
                                    typestring += ('{{TypeTag|' + _type + '}}')
                                # typestring = typestring[:-2]
                                mobtable += ('\n' + '|' + typestring)
                    elif 'waves' in area:
                        wavelist_container = {}
                        wavelist_container_text = ''
                        for enum, wave in enumerate(area['waves']):
                            wavelist = {}
                            # wavelist = set()
                            for monster in sorted(wave):
                                for _monster in __js_mon:
                                    if monster == _monster['id']:
                                        addtomonlist(wavelist, _monster['id'])
                            wavelist_container[enum + 1] = wavelist
                        if len(wavelist_container) == 3:
                            if wavelist_container[1] == wavelist_container[2]:
                                wavelist_container_text = ''
                                typelist = set()
                                for listitem in sorted(wavelist_container[1]):
                                    wavelist_container_text += ('[[' + listitem + ']]' + ', ')
                                    for _type in wavelist_container[1][listitem]:
                                        for __type in _type:
                                            typelist.add(__type)
                                wavelist_container_text = wavelist_container_text[:-2]
                                mobtable += ('\n' + '|-')
                                mobtable += ('\n' + '|' + str(area['area_id']))
                                mobtable += ('\n' + '|')
                                mobtable += wavelist_container_text

                                # Types
                                for wave in sorted(wavelist_container[1]):
                                    typestring = ''
                                    for _type in sorted(typelist):
                                        # typestring += (_type.title() + ', ')
                                        typestring += ('{{TypeTag|' + _type + '}}')
                                    # typestring = typestring[:-2]
                                mobtable += ('\n' + '|' + typestring)

                            if wavelist_container[1] == wavelist_container[2]:
                                typelist = set()
                                wavelist_container_text = ''
                                mobtable += ('\n' + '|-')
                                mobtable += ('\n' + '|' + '\'\'\'Boss\'\'\'')
                                mobtable += ('\n' + '|')
                                for listitem in sorted(wavelist_container[3]):
                                    wavelist_container_text += (
                                        '\'\'\'[[' + listitem + ']]\'\'\'' + ', ')
                                    for _type in wavelist_container[3][listitem]:
                                        for __type in _type:
                                            typelist.add(__type)
                                wavelist_container_text = wavelist_container_text[:-2]
                                mobtable += wavelist_container_text

                                # Types
                                for wave in sorted(wavelist_container[3]):
                                    typestring = ''
                                    for _type in sorted(typelist):
                                        # typestring += (_type.title() + ', ')
                                        typestring += ('{{TypeTag|' + _type + '}}')
                                    # typestring = typestring[:-2]
                                mobtable += ('\n' + '|' + typestring)

                            else:
                                # If Wave1 != Wave2
                                mobtable += ('\n' + '|-')
                                mobtable += ('\n' + '|' + str(area['area_id']))

                                wave_subtable = ('\n' + '|')
                                wavelist_container = {}
                                # Monsters
                                for enum, wave in enumerate(area['waves']):
                                    wavelist = {}
                                    for monster in sorted(wave):
                                        for _monster in __js_mon:
                                            if monster == _monster['id']:
                                                addtomonlist(wavelist, _monster['id'])
                                    if enum in [0, 1]:
                                        wavelist_text = '\'\'Wave ' + str(enum + 1) + ':\'\' '
                                        typelist = set()
                                        for listitem in sorted(wavelist):
                                            wavelist_text += ('[[' + listitem + ']]' + ', ')
                                            for _type in wavelist[listitem]:
                                                for __type in _type:
                                                    typelist.add(__type)
                                        wavelist_text = wavelist_text[:-2]
                                        wave_subtable += (wavelist_text + '\n')
                                wave_subtable = wave_subtable[:-1]
                                mobtable += wave_subtable

                                # Types
                                for enum, wave in enumerate(area['waves']):
                                    if enum in [0, 1]:
                                        typestring = '<ul class="hlist">\'\'Wave ' + \
                                            str(enum + 1) + ':\'\' '
                                        for _type in sorted(typelist):
                                            # typestring += (_type.title() + ', ')
                                            typestring += ('<li>{{TypeTag|' + _type + '}}</li>')
                                        # typestring = typestring[:-2]
                                        if enum == 0:
                                            mobtable += ('\n' + '|' + typestring + '</ul>')
                                        elif enum == 1:
                                            mobtable += ('\n' + typestring + '</ul>')

                                # Bosses
                                wave_subtable = ''
                                wavelist_container = {}
                                for enum, wave in enumerate(area['waves']):
                                    wavelist = {}
                                    for monster in sorted(wave):
                                        for _monster in __js_mon:
                                            if monster == _monster['id']:
                                                addtomonlist(wavelist, _monster['id'])
                                    if enum not in [0, 1]:
                                        typelist = set()
                                        wavelist_text = '\n' + '|-'
                                        wavelist_text += ('\n' + '|' + '\'\'\'Boss\'\'\'')
                                        wavelist_text += ('\n' + '|')
                                        for listitem in sorted(wavelist):
                                            wavelist_text += ('\'\'\'[[' +
                                                              listitem + ']]\'\'\'' + ', ')
                                            for _type in wavelist[listitem]:
                                                for __type in _type:
                                                    typelist.add(__type)
                                        wavelist_text = wavelist_text[:-2]
                                        wave_subtable += (wavelist_text + '\n')
                                wave_subtable = wave_subtable[:-1]
                                mobtable += wave_subtable

                                # Types
                                for enum, wave in enumerate(area['waves']):
                                    if enum not in [0, 1]:
                                        typestring = ''
                                        for _type in sorted(typelist):
                                            # typestring += (_type.title() + ', ')
                                            typestring += ('{{TypeTag|' + _type + '}}')
                                        # typestring = typestring[:-2]
                                        mobtable += ('\n' + '|' + typestring)

                        # If only 2 waves
                        elif len(wavelist_container) == 2:
                            # If Wave1 == Wave2
                            # Monsters
                            if wavelist_container[1] == wavelist_container[2]:
                                wavelist_container_text = ''
                                typelist = set()
                                for listitem in sorted(wavelist_container[1]):
                                    wavelist_container_text += ('[[' + listitem + ']]' + ', ')
                                    for _type in wavelist_container[1][listitem]:
                                        for __type in _type:
                                            typelist.add(__type)
                                wavelist_container_text = wavelist_container_text[:-2]
                                mobtable += ('\n' + '|-')
                                mobtable += ('\n' + '|' + str(area['area_id']))
                                mobtable += ('\n' + '|')
                                mobtable += wavelist_container_text

                            # Types
                            for wave in sorted(wavelist_container[1]):
                                typestring = ''
                                for _type in sorted(wavelist_container[1][wave]):
                                    for __type in _type:
                                        # typestring += (__type.title() + ', ')
                                        typestring += ('{{TypeTag|' + __type + '}}')
                                # typestring = typestring[:-2]
                                mobtable += ('\n' + '|' + typestring)

                            # If Wave1 != Wave2
                            # And if Wave2 is a boss wave
                            if not wavelist_container[1] == wavelist_container[2]:
                                typelist = set()
                                wavelist_container_text = ''
                                if 'properties' in area:
                                    # If there is a boss in boss area
                                    if 'no_bosses_in_area' not in area['properties']:

                                        # Boss
                                        mobtable += ('\n' + '|-')
                                        mobtable += ('\n' + '|' + '\'\'\'Boss\'\'\'')
                                        mobtable += ('\n' + '|')
                                        for listitem in sorted(wavelist_container[2]):
                                            wavelist_container_text += (
                                                '\'\'\'[[' + listitem + ']]\'\'\'' + ', ')
                                            for _type in wavelist_container[2][listitem]:
                                                for __type in _type:
                                                    typelist.add(__type)
                                        mobtable += wavelist_container_text

                                        # Types
                                        for wave in sorted(wavelist_container[2]):
                                            typestring = ''
                                            for _type in sorted(wavelist_container[2][wave]):
                                                for __type in _type:
                                                    # typestring += (__type.title() + ', ')
                                                    typestring += ('{{TypeTag|' + __type + '}}')
                                            # typestring = typestring[:-2]
                                            mobtable += ('\n' + '|' + typestring)

                        elif len(wavelist_container) == 1:
                            # Boss mode
                            typelist = set()
                            wavelist_container_text = ''
                            mobtable += ('\n' + '|-')
                            mobtable += ('\n' + '|' + str(area['area_id']) + ' \'\'\'Boss\'\'\'')
                            mobtable += ('\n' + '|')
                            for listitem in sorted(wavelist_container[1]):
                                wavelist_container_text += (
                                    '\'\'\'[[' + listitem + ']]\'\'\'' + ', ')
                                for _type in wavelist_container[1][listitem]:
                                    for __type in _type:
                                        typelist.add(__type)
                            wavelist_container_text = wavelist_container_text[:-2]
                            mobtable += wavelist_container_text

                            # Types
                            for wave in sorted(wavelist_container[1]):
                                typestring = ''
                                for _type in sorted(wavelist_container[1][wave]):
                                    for __type in _type:
                                        # typestring += (__type.title() + ', ')
                                        typestring += ('{{TypeTag|' + __type + '}}')
                                # typestring = typestring[:-2]
                                mobtable += ('\n' + '|' + typestring)
                    else:
                        print('Check area id:', area['id'])

        if len(mobtable) > 66:
            mobtable += ('\n' + '|}')
            page_text += mobtable
        # else:
        #     print('AAAAAAHHHHHHHHHHHHHHHHH', adv['name'])
        # print(mobtable)

        ######

        # Stub status
        page_text = '{{stub}}' + '\n' + page_text
        # page_text = (page_text + '\n' + footer)
        if not adv['costs'] == []:
            for cost in adv['costs']:
                if 'cost' in cost:
                    if cost['cost'] == 'event_tokens':
                        page_text = (page_text + '\n' + footer_event)
        else:
            page_text = (page_text + '\n' + footer)
        # print(page_text)

        with open('output/{filename}.txt'.format(filename=name), 'w') as f:
            f.write(page_text)

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
