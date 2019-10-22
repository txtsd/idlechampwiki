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
POST = False
PROCESS = True
REDOWNLOAD = False
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

image_dir = '/home/txtsd/.local/share/Steam/steamapps/common/IdleChampions/IdleDragons_Data/StreamingAssets/downloaded_files/'

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

breakout = 0
LICENSE = '''
== Licensing ==
{{Copyright game}}'''

for hero in js_hero:
    if not re.search('^E\d', hero['name']):
        for skin in js_hero_skin:
            if hero['id'] == skin['hero_id']:
                imgid = skin['details']['portrait_graphic_id']
                for gfx in js_graphic:
                    if imgid == gfx['id']:
                        imgname = gfx['graphic']
                        imgname = imgname.replace('/', '__')
                name = skin['name']
                fname_wiki = 'Icon_{name}.png'.format(name=name)
                # fname_orig = 'images/Portraits__Portrait_{name}.png'.format(name=name)
                fname_orig = '{imgname}.png'.format(imgname=imgname)
                # fname_crop = 'images/Portraits__Portrait_{name}_cropped.png'.format(name=name)
                fname_crop = '{imgname}_cropped.png'.format(imgname=imgname)
                fname_orig_path = 'images/' + fname_orig
                fname_crop_path = 'images/' + fname_crop

                # print(fname_wiki)
                # print(fname_orig_path)
                # print(fname_crop_path)
                # print('os.path.isfile(fname_orig_path)', os.path.isfile(fname_orig_path))

                if PROCESS:
                    if REDOWNLOAD or (not os.path.isfile(fname_orig_path)):
                        pathname = fname_orig.replace('__', '//').replace('.png', '')
                        file = requests.get('http://ps5.idlechampions.com/~idledragons/mobile_assets/{pathname}'.format(pathname=pathname))
                        with open('/tmp/IC_temp', 'wb') as t:
                            t.write(file.content)
                        with open('/tmp/IC_temp', 'rb') as t:
                            current_file = t.read()
                            # current_file = t.read()
                        res = re.search(b'(\\x89\\x50\\x4e\\x47\\x0d\\x0a\\x1a\\x0a.*)', current_file, re.MULTILINE|re.DOTALL)
                        if res is not None:
                            with open(fname_orig_path, 'wb') as g:
                                g.write(res.group())
                        else:
                            data = zlib.decompress(current_file)
                            res = re.search(b'(\\x89\\x50\\x4e\\x47\\x0d\\x0a\\x1a\\x0a.*)', data, re.MULTILINE|re.DOTALL)
                            with open(fname_orig_path, 'wb') as g:
                                g.write(res.group())
                    result1 = subprocess.run(['convert', fname_orig_path, '-trim', fname_crop_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if result1.stderr:
                        print(result1.stderr)
                    result2 = subprocess.run(['pngcrush', '-brute', '-rem', 'alla', '-rem', 'allb', '-rem', 'text', '-reduce', '-check', '-q', '-s', '-ow', fname_crop_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if COMPARE:
                    dir_path = os.path.dirname(os.path.realpath(__file__))
                    if not os.path.isdir(os.path.join(dir_path, 'output')):
                        os.makedirs(os.path.join(dir_path, 'output'))
                    main_file = os.path.join(dir_path, 'images/' + '{filename}'.format(filename=fname_crop))
                    posted_file = os.path.join(dir_path, 'images/' + 'posted/{filename}'.format(filename=fname_wiki))
                    try:
                        result = filecmp.cmp(main_file, posted_file, shallow=False)
                    except FileNotFoundError as e:
                        print('{name}: No source found'.format(name=name))
                        if not main_file:
                            print('{name}: {main_file} does not exist'.format(name=name, main_file=main_file))
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
                            FILE = {'file': (fname_wiki, open(fname_crop_path, 'rb'), 'multipart/form-data')}
                            print('{name}: Posting...'.format(name=name))
                            R2 = instance.post(data=EDIT_PARAMS, files=FILE)
                            if R2.status_code == 200:
                                if 'error' not in R2.json():
                                    print('{name}: Success!'.format(name=name))
                                    result1 = subprocess.run(['cp', main_file, posted_file])
                                else:
                                    print('{name}: FAIL! Error Message: {error}'.format(name=name, error=R2.json()['error']['info']))
                            else:
                                print('{name}: FAIL!'.format(name=name))
                # break
