from __future__ import unicode_literals


import redis

# fill in the following.
HOST = "redis-11363.c1.asia-northeast1-1.gce.cloud.redislabs.com"
PWD = "1nOA0St0I7p9pQqu8HkQ18XqDfnoPeoL"
PORT = "11363" 

redis1 = redis.Redis(host = HOST, password = PWD, port = PORT)

while True:
    msg = input("Please enter your query (type 'quit' or 'exit' to end):").strip()
    if msg == 'quit' or msg == 'exit':
        break
    if msg == '':
        continue
    print("You have entered " + msg, end=' ') 

   
    # Add your code here
    value = redis1.get(msg)
    if value == None:
        redis1.set(msg,1)
        get = redis1.get(msg)
    else: 
        value_int=int(value)
        vt = value_int + 1
        get = redis1.getset(msg, vt)

    print('for '+ get.decode() + ' times' ) 
