from BaseModel import BaseModel
import datetime
from Auth.auth import User

class Location(BaseModel):    
    def __init__(self):
        self.lat = None
        self.lng = None
        self.location = []
        self.added = datetime.datetime.now()

    def _presave(self, entityManager):
        self.location  = {'type': 'Point', 'coordinates': [float(self.lng), float(self.lat)]}



class UserData(BaseModel):
    def __init__(self):
        self.user_id = None
        self.location = None
        self.health = 100



class Battle(BaseModel):
    def __init__(self):
        self.users = []
        self.turn_of_user_index = None
        self.turn_of_user = None
        self.latest_action = None
        self.ended = None
        self.loser = None



class Message(BaseModel):
    def __init__(self):
        self.from_user_id = None
        self.for_user_id = None
        self.type = None
        self.data = None
        self.read = False