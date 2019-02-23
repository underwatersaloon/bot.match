import discord
import asyncio
from ship import ship

client = discord.Client();
#chan #활동 채널
#admin #관리자
#control character
ctrlch='!중망호 '
#command list
cmds = ['만들기' , '수장' , '타기' , '내리기' , '모집중']
#cmds.extend = ['설정', '출항', '선원 등록', '명령어', '관리자']
#crew list
cList = []

Token = ''

def cmdParse(cmd, start = 1):
    """cmd Parser 써보지 않아서 모름"""
    return cmd[start:].split(' ')

def argParse(argu,sep):
    """과연 쓸일이 있을까?"""
    pass

async def boat(message, cmd, msgId):
    print('boat : ' + msgId) 
    if cList.count(msgId):
        await client.send_message(message.channel, 'he\'s already on his boat')
    else:
        ship(message.author)
        if ship.sList[-1] == msgId :
            cList.append(msgId)
            if len(cmd) > 1 :
                ship.sList[-1].subject = cmd[1]
            await client.send_message(message.channel, 'your boat is ready')
        else :
            await client.send_message(message.channel, 'has a problem')
                #print("succeed")

async def boom(message, cmd, msgId):
    print('boom')
    cIndex = ship.findbycap(msgId)
    if cIndex < 0 :
        await client.send_message(message.channel, 'there\'s no boat in this port')
    else :
        if len(ship.callbyindex(cIndex).crews) != 0 :
            for i in ship.boom(cIndex):
                cList.remove(i)
        else :
            ship.boom(cIndex)
        cList.remove(msgId)
        await client.send_message(message.channel, 'boomed!')

async def leave(message, cmd, msgId):
    print('leave')
    if cList.count(msgId):
        if ship.findbycap(msgId) == -1 :
            await client.send_message(message.channel, 'you can\'t leave your boat')
        else :
            cIndex = ship.findbyid(msgId)
            if cIndex > 0:
                ship.callbyindex(cIndex).leaving(msgId)
            cList.remove(msgId)
            await client.send_message(message.channel, 'you just left a boat')
    else:
        await client.send_message(message.channel, 'you\'re not unemployeed')

async def board(message, cmd, msgId):
    print('board')
    if cList.count(msgId):
        await client.send_message(message.channel, 'he\'s already on crewlist')
    else:
        if cmd[1].startswith('#') & cmd[1][1:].isnumeric() :
            cIndex = int(cmd[1][1:])
            if ship.callbyindex(cIndex) is not None :
                if ship.callbyindex(cIndex).boarding(msgId) :
                    cList.append(msgId)
                    await client.send_message(message.channel, 'you just boarded')
                else :
                    await client.send_message(message.channel, 'you failed to get on the boat')
            else :
                await client.send_message(message.channel, 'there\'s no such boat')
        else :
            await client.send_message(message.channel, 'wrong boat number')

async def recruit(message, cmd, msgId):
    print('recruit')
    if len(ship.sList) > 0 :
        embed=discord.Embed(title="제 1부두",description="뽀트는 중붕이를 태우고-")
        for i in ship.sList :
            bInfo=i.infor()
            embed.add_field(name = bInfo[0], value = bInfo[1], inline=True)
        await client.send_message(message.channel,embed=embed)
    return None
        
@client.event
async def on_ready():
    print('logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----bot ready-----')

@client.event
async def on_message(message):
    if message.content.startswith(ctrlch):
        cmd = cmdParse(message.content, len(ctrlch)) #파싱 파-킹 이 아니라
        msgId=message.author.id #길어
        cIndex = -1 #index cursor
        print('ent_msgProc : {}'.format(cmd[0])) #프로시저 진입 메시지 디버깅용

        if cmd[0] == cmds[0]:
            await boat(message,cmd,msgId)
        elif cmd[0] == cmds[1] :
            await boom(message,cmd,msgId)
        elif cmd[0] == cmds[2] :
            await board(message,cmd,msgId)
        elif cmd[0] == cmds[3] :
            await leave(message,cmd,msgId)
        elif cmd[0] == cmds[4]:
            await recruit(message,cmd,msgId)
    
    return

client.run(Token)
