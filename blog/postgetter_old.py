import requests
import json
import time
#memes = [22751485]#, 132176157]
memes = [71114104, 132176157, 72340177, 88350989, 122162987, 139069603,
68232062, 29606875, 81671374, 91624558, 147286578] #22751485,  двач, слишком много постов беру  93082454,
anime = [93566453, 100867898, 111230293, 125372241, 100389805, 100892059, 126167642,
84054237, 104003829, 139383329, 135741815, 127473798 , 58110597, 130717387, 21044057,
33984260 ]

post_list = {}
etholone = []
token='6bca1415abf87ea3b901fa146a010209449123cf9020df5d9ced8569f61ee5ff920647e59fef2361fba6f'
my_gid = 119871717
my_uid = 303833699
gids = memes
sort_type = 'likes'

def now():
    return time.time()

def post(url, data):
    response = requests.post(url, data)
    return json.loads(response.text)

def sec_to_str(seconds, flag):
    if flag == 'a': #Wed May 31 11:39:24 2017
        return time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(seconds))
    elif flag == 'b': #151 11:40:04 2017
        return time.strftime("%j %H:%M:%S %Y", time.localtime(seconds))
    elif flag == 'c': #21:18:07 03 Jun 2017
        return time.strftime("%H:%M:%S %d %b %Y", time.localtime(seconds))

def str_to_sec(string, flag):
    if flag == 'a':
        return time.mktime(time.strptime(string, "%a %b %d %H:%M:%S %Y"))
    elif flag == 'b':
        return time.mktime(time.strptime(string, "%j %H:%M:%S %Y"))
    elif flag == 'c':
        return time.mktime(time.strptime(string, "%H:%M:%S %d %b %Y"))

def write(text):
    file = open('post_log.txt', 'a')
    file.write('\n' + text)
    file.close()

def sort(dic, sort_type):
    indic = 1
    while indic > 0:
        indic = 0
        for i in dic:
            if i - 1 >= 1 and i - 1 <= len(dic):
                if dic[i][sort_type] > dic[i-1][sort_type]:
                    dic['temp'] = dic[i-1]
                    dic[i-1] = dic[i]
                    dic[i] = dic['temp']
                    dic.pop('temp')
                    indic =1

            elif i + 1 <= len(dic):
                if dic[i][sort_type] < dic[i+1][sort_type]:
                    dic['temp'] = dic[i]
                    dic[i] = dic[i+1]
                    dic[i+1] = dic['temp']
                    dic.pop('temp')
                    indic =1
    return dic

def yesterday():
    yesterday_1 = int(sec_to_str(now(), 'b')[:4]) - 1
    yesterday = str(yesterday_1) + sec_to_str(now(), 'b')[3:]
    return sec_to_str(str_to_sec(yesterday, 'b'), 'a')

def tomorrow():
    tomorrow_1 = int(sec_to_str(now(), 'b')[:4]) + 1
    tomorrow = str(tomorrow_1) + sec_to_str(now(), 'b')[3:]
    return sec_to_str(str_to_sec(tomorrow, 'b'), 'c')

post_log = []

indic = 1
for gid in gids:
    time.sleep(0.3)
    wall_get = {'url': 'https://api.vk.com/method/wall.get?',
    'data': {'access_token': token, 'v': 5.71, 'owner_id': -gid, 'count': 50 }}
    wall = post(wall_get['url'], wall_get['data'])['response']
    users_get = {'url': 'https://api.vk.com/method/groups.getMembers?',
    'data': {'access_token': token, 'v': 5.71, 'group_id': gid, 'count': 50 }}
    users = post(users_get['url'], users_get['data'])['response']['count']
    for i in range(1, len(wall)):
        if sec_to_str(wall[i]['date'], 'a')[:10] == sec_to_str(now(), 'a')[:10]:
        #if sec_to_str(wall[i]['date'], 'a')[:10] == yesterday()[:10]:
            try:
                if wall[i]['marked_as_ads'] == 0 and wall[i]['text'] == '' and wall[i]['attachment']['type'] == 'photo':
                    if str(wall[i]['attachment']['photo']['pid']) not in post_log:
                        post_list[indic] = {}
                        post_list[indic]['text'] = wall[i]['text']
                        post_list[indic]['owner_id'] = wall[i]['attachment']['photo']['owner_id']
                        post_list[indic]['photo_id'] = wall[i]['attachment']['photo']['pid']
                        post_list[indic]['likes'] = wall[i]['likes']['count'] / int(users) * 1000
                        post_list[indic]['reposts'] = wall[i]['reposts']['count'] / int(users) * 1000
                        #post_list[indic]['full_link']= 'https://vk.com/photo' + str(post_list[indic]['owner_id'])+'_'+str(post_list[indic]['photo_id'])
                        post_list[indic]['full_link'] = wall[i]['attachment']['photo']['src_big']
                    #post_list[indic]['post_id'] = wall[i]['id']
                    #print ('\n', wall[i]['attachment']['photo']['pid'])
                    #print (post_list[indic]['photo_id'])
                    #post_list[indic]['pid_link'] = 'photo' +  str(post_list[indic]['owner_id']) + '_' + str(post_list[indic]['photo_id'])
                        indic +=1
            except KeyError:
                break
    #print (gid, 'wall loaded')
sl = sort(post_list, sort_type)
