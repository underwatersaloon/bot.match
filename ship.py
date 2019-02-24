import discord

class ship:

    __slots__ = ['index', 'captain', 'crews', 'subject', 'ftime', 'waiting', 'reqc', 'maxc', 'state', 'dest']
    _gIndex = 0
    sList=[]
    _slotKor = ['index', '선장', '선원', '이름', '건조 시간', '대기 시간', '필요 인원', '최대 인원', '상태', '목적지']
    _attTrans = dict(zip(_slotKor,__slots__))
    _attSet = dict(zip(__slots__,[None, None, None, 'str', None, 'num', 'num', 'num', None, 'str']))

    def __init__(self, member):
        if ship.sList.count(member.id):
            return
        self.index = ship._gIndex
        ship._gIndex += 1
        self.captain = member.id
        self.crews = []
        self.subject = member.name+'\'s boat'
        #self.ftime = time.time()
        self.waiting = 60
        self.reqc = 3
        self.maxc = 5
        self.state = 0
        ship.sList.append(self)
        return

    def __eq__(self, other):
        if self.captain == other :
            return True
        else :
            return False

    @classmethod
    def findbycap(self, capId):
        "return cls.index 선장의 Id로 배를 찾는다."
        for i in ship.sList :
            if i.captain == capId :
                return i.index
        return -1

    def findbycrew(self, crewId):
        """내부용 메소드. 외부에서 부르면 안된다."""
        for i in self.crews :
            if i == crewId :
                return True
        return False

    @classmethod
    def findbyid(self, memId):
        "return cls.index 멤버의 Id로 배를 찾는다"
        for i in ship.sList :
            if i.captain == memId :
                return i.index
            elif i.findbycrew(memId) :
                return i.index
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
    
    def infor(self):
        tmp = []
        tmp.append('#{} - {}'.format(self.index,self.subject))
        tmp.append('{} / {} ({})'.format(len(self.crews)+1,self.maxc,self.reqc))
        return tmp

    def set(self, name, value):
        tmp = ship._attTrans[name]
        if ship._attSet[tmp] == 'num' :
            if str(value).isnumeric() & int(value) >=0 :
                if tmp == 'waiting' :
                    if 1440 >= int(value):
                        return super().__setattr__(tmp, value)
                    else :
                        return None
                elif tmp == 'reqc' :
                    if self.maxc >= int(value) :
                        return super().__setattr__(tmp, value)
                    else :
                        return None
                elif tmp == 'maxc' :
                    if 16 >= int (value) & (int(value) >= self.reqc & int(value) >= len(self.crews)) :
                        return super().__setattr__(tmp, value)
                    else :
                        return None
                else :
                    return super().__setattr__(tmp, value)
        elif ship._attSet[tmp] == 'str':
            return super().__setattr__(tmp, value)
        return None

    def has(self, name):
        if name in ship._attTrans :
            tmp = ship._attTrans[name]
            print("{} : {}".format(name, tmp))
            return hasattr(self,tmp)
        else :
            return False