import random
from fake_useragent import UserAgent


def log_produce(cnt=2000):
    albet_upper = list(map(chr, range(ord('A'), ord('Z') + 1)))
    albet_lower = list(map(chr, range(ord('a'), ord('z') + 1)))
    albet_num = list(map(str, range(10)))
    topic_arry = ['Ad', 'Volvo', 'Wrangler', '']

    random_uln = albet_lower + albet_upper + albet_num
    random_ln = albet_lower + albet_num
    ua = UserAgent(use_cache_server=False)

    for num in range(0, cnt):
        cookie = ''.join(random.sample(random_uln, 8))
        uid = 'u' + random.choice(albet_num[1:])
        user_agent = ua.random
        ip3 = random.randint(0, 256)
        ip4 = random.randint(0, 256)
        ip = '192.168.%s.%s' % (ip3, ip4)
        video_id = ''.join(random.sample(albet_num, 7))
        topic = 'apple'
        orger_id = '0'
        log_type = str(random.randint(1, 8))
        # log_type  1.点击;2.播放;3.点赞;4.收藏;5.付费观看;6.站外分享;7.评论
        cookie_list = [cookie, uid, user_agent, ip, video_id, topic, orger_id, log_type]
        final = '&'.join(cookie_list)

        yield final


log_file = log_produce(cnt=5000)
click_action = {}
for lg in log_file:
    lg_list = lg.split('&')
    if lg_list[-1] == '1':
        if lg_list[1] not in click_action.keys():
            click_action[lg_list[1]] = []
        click_action[lg_list[1]].append(lg_list[4])
print(click_action)
