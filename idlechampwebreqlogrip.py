import json
from pprint import pprint
import re
from collections import OrderedDict
import math
from decimal import Decimal
from idlechampaccount import ICAccount

webreqlog_path = '/home/txtsd/.local/share/Steam/steamapps/common/IdleChampions/IdleDragons_Data/StreamingAssets/downloaded_files/webRequestLog.txt'
# webreqlog_path = '/tmp/webRequestLog.txt'

with open(webreqlog_path) as f:
    webreqlog = f.read()

search = re.search('({"success":true,"details":{.*})', webreqlog)
# search = re.search('{"success":true,"graphic_defines":[.*', webreqlog)

js = json.loads(search.group())

js_adventure_defines = js['defines']['adventure_defines']
js_adventure_area_defines = js['defines']['adventure_area_defines']
js_background_defines = js['defines']['background_defines']
js_campaign_defines = js['defines']['campaign_defines']
js_location_defines = js['defines']['location_defines']
js_monster_defines = js['defines']['monster_defines']
js_quest_defines = js['defines']['quest_defines']
js_cinematics_defines = js['defines']['cinematics_defines']
js_distraction_defines = js['defines']['distraction_defines']
js_reset_currency_defines = js['defines']['reset_currency_defines']
js_reset_tier_defines = js['defines']['reset_tier_defines']
js_reset_upgrade_defines = js['defines']['reset_upgrade_defines']
if 'challenge_set_defines' in js['defines']:
    js_challenge_set_defines = js['defines']['challenge_set_defines']

js_time_gates = json.loads('[' + json.dumps(js['details']['time_gates']) + ']')
js_event_details = js['details']['event_details']
js_package_deals = js['details']['package_deals']
js_promotions = js['details']['promotions']


#  For single adventure files
per_adventure_adventure_defines = []
per_adventure_adventure_area_defines = []
per_adventure_background_defines = []
per_adventure_campaign_defines = []
per_adventure_location_defines = []
per_adventure_monster_defines = []
per_adventure_quest_defines = []
per_adventure_cinematics_defines = []
per_adventure_distraction_defines = []
per_adventure_reset_currency_defines = []
per_adventure_reset_tier_defines = []
per_adventure_reset_upgrade_defines = []
per_adventure_challenge_set_defines = []

per_adventure_time_gates = []
per_adventure_event_details = []
per_adventure_package_deals = []
per_adventure_promotions = []

# Read files and load data
adventure_defines = []
with open('json/{file}.json'.format(file='adventure_defines'), 'r') as f:
    adventure_defines = json.loads(f.read())
adventure_area_defines = []
with open('json/{file}.json'.format(file='adventure_area_defines'), 'r') as f:
    adventure_area_defines = json.loads(f.read())
background_defines = []
with open('json/{file}.json'.format(file='background_defines'), 'r') as f:
    background_defines = json.loads(f.read())
campaign_defines = []
with open('json/{file}.json'.format(file='campaign_defines'), 'r') as f:
    campaign_defines = json.loads(f.read())
location_defines = []
with open('json/{file}.json'.format(file='location_defines'), 'r') as f:
    location_defines = json.loads(f.read())
monster_defines = []
with open('json/{file}.json'.format(file='monster_defines'), 'r') as f:
    monster_defines = json.loads(f.read())
quest_defines = []
with open('json/{file}.json'.format(file='quest_defines'), 'r') as f:
    quest_defines = json.loads(f.read())
cinematics_defines = []
with open('json/{file}.json'.format(file='cinematics_defines'), 'r') as f:
    cinematics_defines = json.loads(f.read())
distraction_defines = []
with open('json/{file}.json'.format(file='distraction_defines'), 'r') as f:
    distraction_defines = json.loads(f.read())
reset_currency_defines = []
with open('json/{file}.json'.format(file='reset_currency_defines'), 'r') as f:
    reset_currency_defines = json.loads(f.read())
reset_tier_defines = []
with open('json/{file}.json'.format(file='reset_tier_defines'), 'r') as f:
    reset_tier_defines = json.loads(f.read())
reset_upgrade_defines = []
with open('json/{file}.json'.format(file='reset_upgrade_defines'), 'r') as f:
    reset_upgrade_defines = json.loads(f.read())
challenge_set_defines = []
if 'challenge_set_defines' in js['defines']:
    with open('json/{file}.json'.format(file='challenge_set_defines'), 'r') as f:
        challenge_set_defines = json.loads(f.read())

time_gates = []
with open('json/{file}.json'.format(file='time_gates'), 'r') as f:
    time_gates = json.loads(f.read())
event_details = []
with open('json/{file}.json'.format(file='event_details'), 'r') as f:
    event_details = json.loads(f.read())
package_deals = []
with open('json/{file}.json'.format(file='package_deals'), 'r') as f:
    package_deals = json.loads(f.read())
promotions = []
with open('json/{file}.json'.format(file='promotions'), 'r') as f:
    promotions = json.loads(f.read())


# Write old + new data to files
for item in js_adventure_defines:
    if item not in adventure_defines:
        adventure_defines.append(item)
    per_adventure_adventure_defines.append(item)
with open('json/{file}.json'.format(file='adventure_defines'), 'w+') as f:
    f.write(json.dumps(adventure_defines))

for item in js_adventure_area_defines:
    if item not in adventure_area_defines:
        adventure_area_defines.append(item)
    per_adventure_adventure_area_defines.append(item)
with open('json/{file}.json'.format(file='adventure_area_defines'), 'w+') as f:
    f.write(json.dumps(adventure_area_defines))

for item in js_background_defines:
    if item not in background_defines:
        background_defines.append(item)
    per_adventure_background_defines.append(item)
with open('json/{file}.json'.format(file='background_defines'), 'w+') as f:
    f.write(json.dumps(background_defines))

for item in js_campaign_defines:
    if item not in campaign_defines:
        campaign_defines.append(item)
    per_adventure_campaign_defines.append(item)
with open('json/{file}.json'.format(file='campaign_defines'), 'w+') as f:
    f.write(json.dumps(campaign_defines))

for item in js_location_defines:
    if item not in location_defines:
        location_defines.append(item)
    per_adventure_location_defines.append(item)
with open('json/{file}.json'.format(file='location_defines'), 'w+') as f:
    f.write(json.dumps(location_defines))

for item in js_monster_defines:
    if item not in monster_defines:
        monster_defines.append(item)
    per_adventure_monster_defines.append(item)
with open('json/{file}.json'.format(file='monster_defines'), 'w+') as f:
    f.write(json.dumps(monster_defines))

for item in js_quest_defines:
    if item not in quest_defines:
        quest_defines.append(item)
    per_adventure_quest_defines.append(item)
with open('json/{file}.json'.format(file='quest_defines'), 'w+') as f:
    f.write(json.dumps(quest_defines))

for item in js_cinematics_defines:
    if item not in cinematics_defines:
        cinematics_defines.append(item)
    per_adventure_cinematics_defines.append(item)
with open('json/{file}.json'.format(file='cinematics_defines'), 'w+') as f:
    f.write(json.dumps(cinematics_defines))

for item in js_distraction_defines:
    if item not in distraction_defines:
        distraction_defines.append(item)
    per_adventure_distraction_defines.append(item)
with open('json/{file}.json'.format(file='distraction_defines'), 'w+') as f:
    f.write(json.dumps(distraction_defines))

for item in js_reset_currency_defines:
    if item not in reset_currency_defines:
        reset_currency_defines.append(item)
    per_adventure_reset_currency_defines.append(item)
with open('json/{file}.json'.format(file='reset_currency_defines'), 'w+') as f:
    f.write(json.dumps(reset_currency_defines))

for item in js_reset_tier_defines:
    if item not in reset_tier_defines:
        reset_tier_defines.append(item)
    per_adventure_reset_tier_defines.append(item)
with open('json/{file}.json'.format(file='reset_tier_defines'), 'w+') as f:
    f.write(json.dumps(reset_tier_defines))

for item in js_reset_upgrade_defines:
    if item not in reset_upgrade_defines:
        reset_upgrade_defines.append(item)
    per_adventure_reset_upgrade_defines.append(item)
with open('json/{file}.json'.format(file='reset_upgrade_defines'), 'w+') as f:
    f.write(json.dumps(reset_upgrade_defines))

for item in js_challenge_set_defines:
    if item not in challenge_set_defines:
        challenge_set_defines.append(item)
    per_adventure_challenge_set_defines.append(item)
with open('json/{file}.json'.format(file='challenge_set_defines'), 'w+') as f:
    f.write(json.dumps(challenge_set_defines))


for item in js_time_gates:
    if item not in time_gates:
        time_gates.append(item)
    per_adventure_time_gates.append(item)
with open('json/{file}.json'.format(file='time_gates'), 'w+') as f:
    f.write(json.dumps(time_gates))

for item in js_event_details:
    if item not in event_details:
        event_details.append(item)
    per_adventure_event_details.append(item)
with open('json/{file}.json'.format(file='event_details'), 'w+') as f:
    f.write(json.dumps(event_details))

for item in js_package_deals:
    if item not in package_deals:
        package_deals.append(item)
    per_adventure_package_deals.append(item)
with open('json/{file}.json'.format(file='package_deals'), 'w+') as f:
    f.write(json.dumps(package_deals))

for item in js_promotions:
    if item not in promotions:
        promotions.append(item)
    per_adventure_promotions.append(item)
with open('json/{file}.json'.format(file='promotions'), 'w+') as f:
    f.write(json.dumps(promotions))


# Store all data in an adventure file separately
if js_adventure_defines[0]['name'] == 'Free Play':
    per_adventure_filename = js_adventure_defines[1]['name'] + ' ' + js_adventure_defines[0]['name'] + '.json'
else:
    per_adventure_filename = js_adventure_defines[0]['name'] + '.json'
per_adventure_json = []
per_adventure_json.append({'adventure_defines': per_adventure_adventure_defines})
per_adventure_json.append({'adventure_area_defines': per_adventure_adventure_area_defines})
per_adventure_json.append({'background_defines': per_adventure_background_defines})
per_adventure_json.append({'campaign_defines': per_adventure_campaign_defines})
per_adventure_json.append({'location_defines': per_adventure_location_defines})
per_adventure_json.append({'monster_defines': per_adventure_monster_defines})
per_adventure_json.append({'quest_defines': per_adventure_quest_defines})
per_adventure_json.append({'cinematics_defines': per_adventure_cinematics_defines})
per_adventure_json.append({'distraction_defines': per_adventure_distraction_defines})
per_adventure_json.append({'reset_currency_defines': per_adventure_reset_currency_defines})
per_adventure_json.append({'reset_tier_defines': per_adventure_reset_tier_defines})
per_adventure_json.append({'reset_upgrade_defines': per_adventure_reset_upgrade_defines})

per_adventure_json.append({'time_gates': per_adventure_time_gates})
per_adventure_json.append({'event_details': per_adventure_event_details})
per_adventure_json.append({'package_deals': per_adventure_package_deals})
per_adventure_json.append({'promotions': per_adventure_promotions})

with open('json/__{file}'.format(file=per_adventure_filename), 'w+') as f:
    f.write(json.dumps(per_adventure_json))
