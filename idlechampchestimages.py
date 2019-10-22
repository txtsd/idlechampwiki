import json
from pprint import pprint
import re
from collections import OrderedDict
import math
from decimal import Decimal
import html
import glob
from idlechampaccount import ICAccount
import subprocess
import filecmp
import os
import hashlib
import requests
import zlib
import tempfile


COMPARE = True
POST = True
REDOWNLOAD = True
PROCESS = True
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

set_chests = set()

breakout = 0
LICENSE = '''
== Licensing ==
{{Copyright game}}'''

for chest in js_chest_type:
    if chest['id'] not in set_chests:
        set_chests.add(chest['id'])
        name = chest['name']
        if chest['id'] == 63:
            name += ' (Farideh)'
        if chest['id'] == 112:
            name += ' (Ishi)'
        print(chest['id'], chest['name'])
        if (not 'Gold E1' in name) and (not 'Silver E1' in name):
            imgid = chest['graphic_id']
            for gfx in js_graphic:
                if imgid == gfx['id']:
                    imgname = gfx['graphic']
                    imgname = imgname.replace('/', '__')
            fname_wiki = 'Icon_{name}.png'.format(name=name)
            fname_orig = '{imgname}.png'.format(imgname=imgname)
            fname_crop = '{imgname}_cropped.png'.format(imgname=imgname)
            fname_orig_path = 'images/' + fname_orig
            fname_crop_path = 'images/' + fname_crop
            # print(name)
            # print(imgname)
            # print()

            if PROCESS:
                if REDOWNLOAD or (not os.path.isfile(fname_orig_path)):
                    pathname = fname_orig.replace('__', '//').replace('.png', '')
                    file = requests.get(
                        'http://ps5.idlechampions.com/~idledragons/mobile_assets/{pathname}'.format(pathname=pathname))
                    with open('/tmp/IC_temp', 'wb') as t:
                        t.write(file.content)
                    with open('/tmp/IC_temp', 'rb') as t:
                        current_file = t.read()
                        # current_file = t.read()
                    res = re.search(b'(\\x89\\x50\\x4e\\x47\\x0d\\x0a\\x1a\\x0a.*)',
                                    current_file, re.MULTILINE | re.DOTALL)
                    if res is not None:
                        with open(fname_orig_path, 'wb') as g:
                            g.write(res.group())
                    else:
                        data = zlib.decompress(current_file)
                        res = re.search(b'(\\x89\\x50\\x4e\\x47\\x0d\\x0a\\x1a\\x0a.*)',
                                        data, re.MULTILINE | re.DOTALL)
                        with open(fname_orig_path, 'wb') as g:
                            g.write(res.group())

                result1 = subprocess.run(['convert', fname_orig_path, '-alpha', 'extract', '-auto-level', '-negate', '-threshold', '80%', '-negate', '-type', 'bilevel', '-define',
                                          'connected-components:area-threshold=1000', '-define', 'connected-components:verbose=true', '-connected-components', '4', 'null:'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # print(result1.stdout.decode())
                res = re.search(
                    b'((?P<width>\d+)x(?P<height>\d+)\+(?P<offset_x>\d+)\+(?P<offset_y>\d+)).*?gray\(255\)', result1.stdout)
                # print(res.groups())
                # print(res.group('width'))
                # print(res.group('height'))
                # print(res.group('offset_x'))
                # print(res.group('offset_y'))
                result2 = subprocess.run(
                    [
                        'convert',
                        fname_orig_path,
                        '-crop',
                        '{w}x{h}+{x}+{y}'.format(
                            w=res.group('width').decode(),
                            h=res.group('height').decode(),
                            x=res.group('offset_x').decode(),
                            y=res.group('offset_y').decode()
                        ),
                        fname_crop_path
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                if result2.stderr:
                    print(result2.stderr)
                result3 = subprocess.run(['pngcrush', '-brute', '-rem', 'alla', '-rem', 'allb', '-rem', 'text', '-reduce', '-check', '-q', '-s', '-ow', fname_crop_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if COMPARE:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                if not os.path.isdir(os.path.join(dir_path, 'output')):
                    os.makedirs(os.path.join(dir_path, 'output'))
                main_file = os.path.join(dir_path, 'images/' +
                                         '{filename}'.format(filename=fname_crop))
                posted_file = os.path.join(dir_path, 'images/' +
                                           'posted/{filename}'.format(filename=fname_wiki))
                try:
                    result = filecmp.cmp(main_file, posted_file, shallow=False)
                except FileNotFoundError as e:
                    print('{name}: No source found'.format(name=name))
                    if not main_file:
                        print('{name}: {main_file} does not exist'.format(
                            name=name, main_file=main_file))
                    result = None

                if (result is not None) and (result == True):
                    print('{name}: No changes'.format(name=name))
                else:
                    print('{name}: Changes detected!'.format(name=name))
                    # if SHOW_CHANGES:
                    #     result = subprocess.run(['git', 'diff', '--no-index', posted_file, main_file])
                    if POST:
                        if _summary is None:
                            _summary = input('Enter change summary: ')
                        EDIT_PARAMS = {
                            'action': 'upload',
                            'filename': fname_wiki,
                            'ignorewarnings': 1,
                            'text': LICENSE,
                            'format': 'json',
                            'bot': '1',
                            'summary': _summary,
                            # 'nocreate': '1',
                        }
                        FILE = {'file': (fname_wiki, open(
                            fname_crop_path, 'rb'), 'multipart/form-data')}
                        print('{name}: Posting...'.format(name=name))
                        R2 = instance.post(data=EDIT_PARAMS, files=FILE)
                        if R2.status_code == 200:
                            if 'error' not in R2.json():
                                print('{name}: Success!'.format(name=name))
                                result1 = subprocess.run(['cp', main_file, posted_file])
                            else:
                                print('{name}: FAIL! Error Message: {error}'.format(
                                    name=name, error=R2.json()['error']['info']))
                                # print(R2.json())
                                if R2.json()['error']['code'] == 'fileexists-no-change':
                                    result1 = subprocess.run(['cp', main_file, posted_file])
                        else:
                            print('{name}: FAIL!'.format(name=name))
            # break
