import random

pack = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'


base = 'YYYYYYYYYYYY_XXXX'

def generate():
    token = ''
    for i in range(base.count('Y')):
        token += random.choice(pack)
    token += '_' + str(random.randint(1000, 9999))
    return token
