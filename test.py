from ship_test import ship

def prShip(lst):
    for i in lst:
        print('capID : {}, boat Index : {}, boat name : {}'.format(i.captain,i.index,i.subject))

def main():
    capIds=[i+1000 for i in range(10)]
    capNames=['captain no.' + str(capIds[i]) for i in range(10)]
    crewIds=[i+10 for i in range(40)]
    
    for i in range(10):
        ship(capIds[i],capNames[i])

    prShip(ship.sList)
