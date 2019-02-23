import discord
import asyncio
from ship import ship

client = discord.Client();
#command list
cmds = ['boat' , 'boom' , 'board' , 'leave' , 'recruit' , 'find']
#crew list
cList = []

Token = ''

def cmdParse(cmd):
    """cmd Parser 써보지 않아서 모름"""
    return cmd[1:].split(' ',1)

def argParse(argu,sep)
    """과연 쓸일이 있을까?"""
    pass

@client.event
async def on_ready():
    print('logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----bot ready-----')

@client.event
async def on_message(message):
    if message.content.startswith('!'):
        print('enter msgProc') #프로시저 진입 메시지 디버깅용
        cmd = cmdParse(message.content) #파싱 파-킹 이 아니라
        msgId=message.author.id #길어
        cIndex = -1 #index cursor
        
        if cmd[0] == cmds[0]:
            print('boat : ' + msgId)
            if ship.sList.count(msgId):
                await client.send_message(message.channel, 'he\'s already on his boat')
            else:
                ship(message.author)
                if ship.sList[-1] == msgId :
                    cList.append(msgId)
                    await client.send_message(message.channel, 'your boat is ready')
                else :
                    await client.send_message(message.channel, 'has a problem')
                print("succeed")
        elif cmd[0] == cmds[1]:
            print('boom')
            cIndex = ship.findbycap(msgId)
            if cIndex <0:
                await client.send_message(message.channel, 'there\'s no boat in this port')
            else :
                if len(ship.callbyindex(cIndex).crews) != 0 :
                    for i in ship.boom(cIndex):
                        cList.remove(i)
                else :
                    ship.boom(cIndex)
                cList.remove(msgId)
                await client.send_message(message.channel, 'boomed!')
                
        elif cmd[0]== cmds[2]:
            print('board')
            if cList.count(msgId):
                await client.send_message(message.channel, 'he\'s already on crewlist')
            else:
                if cmd[1].startswith('#') && cmd[1][1:].isnumeric() :
                    cIndex = int(mcd[1])
                    if ship.callbyindex(cIndex) is not None :
                        if ship.callbyindex(cIndex).boarding(msgId) :
                            cList.attend(msgId)
                            await client.send_message(message.channel, 'you just boarded')
                        else :
                            await client.send_message(message.channel, 'you failed to get on the boat')
                    else :
                        await client.send_message(message.channel, 'there\'s no such boat')
                else :
                    await client.send_message(message.channel, 'wrong number')
        elif cmd[0] == cmds[3]:
            print('leave')
            if cList.count(msgId):
                if ship.sList.findbycap(msgId) > 0 :
                    await client.send_message(message.channel, 'you can\'t leave your boat')
                else :
                    cIndex = ship.findbyId(msgId)
                    if cIndex > 0:
                        ship.callbyindex(cIndex).leaving(msgId)
                    cList.remove(msgId)
                    await client.send_message(message.channel, 'you just left a boat')
            else:
                await client.send_message(message.channel, 'you\'re not unemployeed')
        elif cmd[0] == cmds[4]:
            print('recruit')
            if len(ship.sList) > 0 :
                for i in ship.sList :
                    await client.send_message(message.channel, i.subject + '(captain ' + i.captain + ')')

                    
client.run(Token)
