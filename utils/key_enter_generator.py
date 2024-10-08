import json
import hashlib
import random


def key_generator():
    keys_generated = []
    for i in range(1, 30):
        key_str = 'keyBotSyperccaasmv12[][34]12,vc' + str(i) + str(random.randint(i, i**3))
        keys_generated.append(hashlib.sha512(key_str.encode()).hexdigest())

    with open("../cred/test_keys_inn_for_bot.json", "w") as outfile:
        json.dump(keys_generated, outfile)


def key_reader():
    with open('../cred/test_keys_inn_for_bot.json', 'r') as openfile:
        json_object = json.load(openfile)
    print(json_object)
    for obj in json_object:
        print(obj)
    print(type(json_object))
    print(len(json_object))

key_generator()
key_reader()