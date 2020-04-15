from __future__ import unicode_literals


import redis

# fill in the following.
# HOST = "redis-11363.c1.asia-northeast1-1.gce.cloud.redislabs.com"
# PWD = "1nOA0St0I7p9pQqu8HkQ18XqDfnoPeoL"
# PORT = "11363" 

HOST = "redis-15288.c16.us-east-1-3.ec2.cloud.redislabs.com"
PWD = "TE7ntZzxOTUByAsEbINMBAKVtBq8oROi"
PORT = "15288" 

r = redis.Redis(host = HOST, password = PWD, port = PORT)

user_id1 = "uu"
user_id2 = "tianxin"

query=['age?','hot?','weak?']
index = 0

while True:
    msg = input("Please enter your query (type 'quit' or 'exit' to end):").strip()
    if msg == 'quit' or msg == 'exit':
        break
    if msg == '':
        continue
        print("You have entered " + msg, end=' ')

    # Try hash
    if msg == 'test1':
        r.hset("user_id1", 'key1', 'value11')
        r.hset("user_id1", 'key2', 'value12')

    # create by one
    if msg == 'test2':
        r.hmset("hash2", {"k2": "v2", "k3": "v3"})
        print(type(user_id1))

    # existing str
    if msg == 'test3':
        r.hset(user_id1,'key1', 'value11')

    # create a lot
    if msg == 'start':
        for it in query:
            ans = input(it).strip()
            r.hset(user_id1,it,ans)
        print('you have done all of the question')

    if msg == 'check':
        temp = r.hgetall("hash1")
        print(temp)

    print ('else')





   
    # Add your code here

    '''
    value = redis1.get(msg)
    if value == None:
        print('for 1 times' )
        redis1.set(msg,2)
    else: 
        value_int=int(value)
        vt = value_int + 1
        get = redis1.getset(msg, vt)
        print('for '+ get.decode() + ' times' )
    '''


