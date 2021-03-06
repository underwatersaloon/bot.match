class ship:
    
    __slots__ = ['index', 'captain', 'crews', 'subject', 'ftime', 'waiting', 'reqc', 'maxc', 'state']
    _gIndex = 0
    sList=[]

    def __init__(self, nId, name):
        if ship.sList.count(nId):
            return
        self.index = ship._gIndex
        ship._gIndex += 1
        self.captain = nId
        self.crews = []
        self.subject = name + '\'s boat'
        self.reqc = 3
        self.maxc = 5
        self.state = 0
        ship.sList.append(self)

    def __eq__(self, other):
        if self.captain == other :
            return True
        else :
            return False

    @classmethod
    def findbycap(self, capId):
        for i in ship.sList :
            if i.captain == capId :
                return i.index
        return -1

    def findbycrew(self, crewId):
        for i in self.crews :
            if i == crewId :
                return self.index
        return -1

    @classmethod
    def findbyid(self, memId):
        for i in ship.sList :
            if i.captain == memId :
                return i.index
            elif tmp == i.findbycrew(memId) :
                return tmp
        return -1

    @classmethod
    def callbyindex(self, tar):
        """return ship"""
        for i in ship.sList :
            if i.index == tar :
                return i
        return None

    @classmethod
    def boom(self, tar):
        tmp = ship.callbyindex(tar)
        if tmp is None :
            return None
        else :
            ship.sList.remove(tmp)
            return tmp.crews

    def boarding(self, crewId):
        if len(self.crews) == (self.maxc - 1) | self.crews.count(crewId) :
            return False
        self.crews.append(crewId)
        return True
        
    def leaving(self, crewId):
        if self.crews.count(crewId) | len(self.crews) != 0 :
            self.crews.remove(crewId)
            return True
        else :
            return False

    def __setattr__(self, name, value):
        print('{} : {}'.format(name , value))
        return super().__setattr__(name, value)
    
