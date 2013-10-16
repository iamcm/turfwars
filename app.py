from gevent import monkey
monkey.patch_all()

import time
import random
import string
import json
import os 
import bottle
import settings
from Helpers import logger
from EntityManager import EntityManager
from Auth.auth import AuthService, User, AuthPlugin
from Auth.apps import auth_app
from models.Models import *
from Helpers.emailHelper import Email
from datetime import datetime
from BottlePlugins import ViewdataPlugin

import memcache
memcache_client = memcache.Client([settings.MEMCACHESERVER])

MESSAGECACHEKEY = '%s_messages' # usage: MESSAGECACHEKEY % (user_id)


#######################################################
# Plugins
#######################################################
def common_view_data():
    em = EntityManager()

    data = {
        'logged_in_user': em.find_one_by_id('User', bottle.request.session.user_id)
    }

    return data


viewdata_plugin = ViewdataPlugin(callback_function=common_view_data, bottle_app_reference=bottle)
auth_plugin = AuthPlugin(EntityManager())




#######################################################
# Static files
#######################################################
if settings.PROVIDE_STATIC_FILES:
    @bottle.route('/static/<filepath:path>', skip=[auth_plugin, viewdata_plugin])
    def index(filepath):
        return bottle.static_file(filepath, root=settings.ROOTPATH +'/static/')









#######################################################
# Main app routes
#######################################################

@bottle.route('/')
def index():
    em = EntityManager()

    userdata = em.find_one('UserData', {'user_id':bottle.request.session.user_id})
    users = []
    if userdata:
        users = em.geospatial_near('UserData', 'location.location', [float(userdata.location.lng), float(userdata.location.lat)], 10000)

        #regenerate health
        if userdata.health == 0:
            userdata.health = 100
            em.save('UserData', userdata)
    
    userIds = [u.user_id for u in users if str(u.user_id) != str(bottle.request.session.user_id)]

    users = em.find('User', {'_id':{'$in':userIds}})

    bottle.response.viewdata.update({'users':users})

    return bottle.template('index.tpl', vd=bottle.response.viewdata)



@bottle.route('/log/location', method="POST")
def log():
    lat = bottle.request.POST.get('lat')
    lng = bottle.request.POST.get('lng')

    l = Location()
    l.lat = lat
    l.lng = lng 

    em = EntityManager()

    userdata = em.find_one('UserData', {'user_id':bottle.request.session.user_id})
    if not userdata:
        userdata = UserData()
        userdata.user_id = bottle.request.session.user_id
        userdata.health = 100

    userdata.location = l

    em.save('UserData', userdata)

    return ''



@bottle.route('/challenge/:user_id')
def index(user_id):
    em = EntityManager()

    challenged_user = em.find_one_by_id('User', user_id)

    b = Battle()
    b.users.append(challenged_user)
    b.users.append(em.find_one_by_id('User', bottle.request.session.user_id))
    b.turn_of_user = challenged_user
    b.turn_of_user_index = 0
    b = em.save('Battle', b)

    m = Message()
    m.for_user_id = str(challenged_user._id)
    m.type = 'challenge'
    m.data = {'battle_id':str(b._id)}
    em.save('Message', m)

    return bottle.redirect('/battle/'+ str(b._id))



@bottle.route('/battle/:battle_id')
def index(battle_id):
    em = EntityManager()

    battle = em.find_one_by_id('Battle', battle_id)

    if bottle.request.session.user_id not in [u._id for u in battle.users]:
        battle.users.append(em.find_one_by_id('User', bottle.request.session.user_id))
        em.save('Battle', battle)

    for u in battle.users:
        u.userdata = em.find_one('UserData', {'user_id':u._id})

    bottle.response.viewdata.update({'battle':battle, 'current_session_user_id':bottle.request.session.user_id})

    return bottle.template('battle.tpl', vd=bottle.response.viewdata)



@bottle.route('/attack/:battle_id/:user_id')
def index(battle_id, user_id):
    em = EntityManager()

    attacking_user = em.find_one_by_id('User', bottle.request.session.user_id)

    battle = em.find_one_by_id('Battle', battle_id)

    if bottle.request.session.user_id == battle.turn_of_user._id and battle.ended is None:
        damage = random.sample(range(5), 1)[0] * 10

        attacked_user = em.find_one_by_id('User', user_id)
        attacked_user_data = em.find_one('UserData', {'user_id':attacked_user._id})

        attacked_user_data.health -= damage

        if attacked_user_data.health <= 0:
            attacked_user_data.health = 0
            battle.ended = datetime.now()
            battle.loser = attacked_user

        em.save('UserData', attacked_user_data)

        battle.latest_action = '%s attacked %s and reduced their health by %s!' % (attacking_user.email, attacked_user.email, damage)

        battle.turn_of_user_index += 1
        if battle.turn_of_user_index >= len(battle.users):
            battle.turn_of_user_index = 0

        battle.turn_of_user = battle.users[battle.turn_of_user_index]

        em.save('Battle', battle)

        for u in battle.users:
            if str(u._id) != str(bottle.request.session.user_id):
                m = Message()
                m.for_user_id = str(u._id)
                m.type = 'reload'
                em.save('Message', m)

    return bottle.redirect('/battle/'+ str(battle_id))
    



@bottle.route('/message/subscribe', skip=[viewdata_plugin])
def index():
    timeout_counter = 0

    if bottle.request.GET.getall('readIds[]'):
        delete_messages(bottle.request.GET.getall('readIds[]'), bottle.request.session.user_id)

    messages = get_messages(bottle.request.session.user_id)

    while not messages:
        timeout_counter += 1

        messages = get_messages(bottle.request.session.user_id)

        if timeout_counter > 100:
            return ''
        else:
            time.sleep(0.2)

    em = EntityManager()

    bottle.response.content_type = 'text/json'
    return json.dumps({'messages':[em.entity_to_json_safe_dict(m) for m in messages]})




@bottle.route('/message/read/:message_id', skip=[viewdata_plugin])
def index(message_id):
    delete_messages([message_id], bottle.request.session.user_id)
    return ''




def delete_messages(messageIds, deleted_by_user_id):
    if messageIds:
        em = EntityManager()

        for id in messageIds:
            m = em.find_one_by_id('Message', id)

            if m and str(m.for_user_id) == str(deleted_by_user_id):
                em.remove_one('Message', id)



def get_messages(user_id):    
    messages = memcache_client.get(MESSAGECACHEKEY % str(user_id))
    if messages:
        return messages
    else:
        return None





#######################################################



app = bottle.app()
app.install(auth_plugin)
app.install(viewdata_plugin)

app.mount('/auth/', auth_app)


if __name__ == '__main__':
    with open(settings.ROOTPATH +'/app.pid','w') as f:
        f.write(str(os.getpid()))

    if settings.DEBUG: 
        bottle.debug() 
    
    if settings.SERVER == 'gunicorn':    
        bottle.run(server=settings.SERVER, host=settings.APPHOST, port=settings.APPPORT, worker_class='gevent')
    else:
        bottle.run(app=app, server=settings.SERVER, reloader=settings.DEBUG, host=settings.APPHOST, port=settings.APPPORT, quiet=(settings.DEBUG==False) )
    
