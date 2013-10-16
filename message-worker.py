from EntityManager import EntityManager
from models.Models import *
import settings
import time
import memcache

MESSAGECACHEKEY = '%s_messages' # usage: MESSAGECACHEKEY % (user_id)

CACHEDURATION = (60 * 60) * 24 # 1 day

memcache_client = memcache.Client([settings.MEMCACHESERVER])

while True:

    em = EntityManager()

    messages = em.find('Message', {'read':False})

    object_to_cache = {}
    message_ids_to_cache= []
    user_ids_to_cache = []

    for m in messages:
        message_ids_to_cache.append(str(m._id))
        user_ids_to_cache.append(str(m.for_user_id))

        if str(m.for_user_id) in object_to_cache:
            object_to_cache[str(m.for_user_id)].append(m)
        else:
            object_to_cache[(m.for_user_id)] = [m]

    current_cached_message_ids = memcache_client.get('current_cached_message_ids')

    #print '----------------------------------'
    #print '----------------------------------'
    #print '----------------------------------'
    #print ('current_cached_message_ids', current_cached_message_ids)
    #print ('message_ids_to_cache', message_ids_to_cache)

    if current_cached_message_ids != message_ids_to_cache:

        for user_id, message_list in object_to_cache.iteritems():
            memcache_client.set(MESSAGECACHEKEY % str(user_id), message_list, time=CACHEDURATION)
            #print ('SET', (MESSAGECACHEKEY % str(user_id), message_list))


        memcache_client.set('current_cached_message_ids', message_ids_to_cache)




    current_cached_user_ids = memcache_client.get('current_cached_user_ids')
    #print ('current_cached_user_ids', current_cached_user_ids)
    #print ('user_ids_to_cache', user_ids_to_cache)

    if not current_cached_user_ids:
        current_cached_user_ids = []

    if current_cached_user_ids != user_ids_to_cache:
        a = set(current_cached_user_ids)
        b = set(user_ids_to_cache)

        for user_id in a.difference(b):
            memcache_client.delete(MESSAGECACHEKEY % str(user_id))
            #print('DELETE', MESSAGECACHEKEY % str(user_id))

        memcache_client.set('current_cached_user_ids', user_ids_to_cache)


    time.sleep(1)
