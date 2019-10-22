import json
from decimal import Decimal
from idlechampaccount import ICAccount
from pprint import pprint
import os
import filecmp


COMPARE = True
POST = False
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

page_text = '''
Familiars are small creatures that can be purchased with either real money, or gems, that allow the player to automate [[clicking]] and leveling up [[Champions]].

They get unlocked after having reached area 66 in any campaign.

==Clickrates==

\'\'\'Clicking Monsters - 5 clicks per second\'\'\'
*Up to six familiars can be assigned to clicking at a time.
*If 3 or more are assigned, they will automatically pickup gold, quest items, event items, and the contents of the gem bag.
*If 5 or more are assigned, they will automatically open the gem bag.
*If 6 are assigned, they will automatically click distractions.
*Familiars assigned to this task will always attack the frontmost enemy, as long as it is possible to deal damage to it via clicks (i.e. not log barricades or bosses with segmented health).

\'\'\'Leveling Champions - 1 click per second\'\'\'
*One familiar can be assigned per champion.
*As they click in the same way as a person clicking the green button, if the level up system is set to purchase upgrades, they will not level up a champion until the upgrade can be afforded.

\'\'\'Using Ultimates - 1 click per 30 seconds\'\'\'
*Up to four familiars can be assigned to the ultimates bar at once.

==List of Familiars==
{familiar_list}

{{{{Navbox-IdleChampions}}}}
[[Category:Game Mechanics]]'''

familiar_text = ''


for familiar in js_familiar:
    id_ = familiar['id']
    name = familiar['name']
    desc = familiar['description']
    cost = familiar['cost']
    prop = familiar['properties']

    fam = '''
\'\'\'{name}\'\'\'

{desc}

''Acquisition method: {cost}''

'''

    if 'soft_currency' in cost:
        real_cost = str(cost['soft_currency'])  + ' gems'
        # if (int(real_cost) / 1000) < 1:
        #     real_cost = ('{0:.2E}'.format(cost['soft_currency'])).replace('E+', 'e')
    elif 'premium_item' in cost:
        for prem in js_premium_item:
            if prem['id'] == cost['premium_item']:
                real_cost = '$' + str(int(prem['cost']) / 100)
    elif 'show_only_if_owned' in prop:
        if name == 'Gift-Wrapped Mimic':
            real_cost = 'Participate in the first anniversary event.'
        elif name == 'Iris':
            real_cost = 'Part of the Founder\'s Pack.'

    fam = fam.format(
        name=name,
        desc=desc,
        cost=real_cost,
    )

    familiar_text += fam

page_text = page_text.format(familiar_list=familiar_text)


with open('output/familiars.txt', 'w') as f:
    f.write(page_text)

if COMPARE:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isdir(os.path.join(dir_path, 'output')):
        os.makedirs(os.path.join(dir_path, 'output'))
    main_file = os.path.join(dir_path, 'output/familiars.txt')
    posted_file = os.path.join(dir_path, 'output/posted/familiars.txt')
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
            if POST:
                if _summary is None:
                    _summary = input('Enter change summary: ')
                EDIT_PARAMS = {
                    'action': 'edit',
                    'title': 'Familiars',
                    'text': page_text,
                    'bot': '1',
                    'nocreate': '1',
                    'summary': _summary
                }
                print('Posting...')
                R2 = instance.post(data=EDIT_PARAMS)
                if R2.status_code == 200:
                    print('Success!')
                    with open('output/posted/familiars.txt', 'w') as g:
                        g.write(page_text)
                else:
                    print('FAIL!')
