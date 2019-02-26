import discord
import asyncio
from ship import ship

client = discord.Client();
#chan #활동 채널
#admin #관리자
#control character
ctrlch='$'
#command list
help = '도움!' 
cmds = ['모집' , '침몰' , '참가' , '탈주' , '목록', '정보', '호출', '설정' , '출항']
guides = [ '모집 [배 이름] : 새로운 배를 만든다. 배를 만든 사람은 선장이 된다. \n 배 이름을 입력하면 이름을 가진 배를 만들수 있다.' # 만들기 명령어에 대한 도움말
          ,'침몰 : (선장 전용) 배를 버린다.' # 수장 명령어에 대한 도움말
          ,'타기 #(배 번호) : 배에 탄다. 이미 배를 가지고 있거나, 배에 탔다면 탈수 없다.' # 타기 명령어
          ,'탈주 : 배에서 내린다. 선장은 배에서 내릴 수 없다. 플라잉 더치맨에겐 선장이 필요하다.' # 내리기
          ,'목록 : 현재 선원을 모집하는 배를 확인한다.' # 모집중
          ,'정보 : 현재 타고 있는 배를 확인한다.' # 정보
          ,'호출 : (선장 전용) 선장은 선원을 호출할 수 있다. 바다로 나갈 시간이다!' # 호출
          ,'설정 (항목) : (변경 내용) , ... : (선장 전용) 선장은 자신의 배를 변경할 수 있다. \n 변경 가능 항목은 "배 이름" , "필요 인원" , "최대 인원", "출발 시간" 이다. '] # 설정
#cmds.extend = ['출항', '선원 등록', '명령어', '관리자']
#crew list
cList = []
wcList = []


Token = ''

def cmdParse(cmd, start = 1):
    """cmd Parser 써보지 않아서 모름"""
    return cmd[start:].split(' ', 1)

def argParse(argu):
    """ : 로 구분? !중망호 세팅 이름:블라블라 블라숑, 블라블라 속성:하 시발 담배가 맵다, 아니시발 존나 싫엏 ㅠㅠ: 머라머라 머라
    딕셔너리 이용 함. k[attr]=val 방식인듯"""
    tmp = argu.split(",")
    argv = {}
    for i in tmp:
        tmp2 = i.split(':', 1)
        if len(tmp2) == 2 :
            argv[tmp2[0].strip()]=tmp2[1].strip()
    return argv

async def boat(message, cmd):
    msgId=message.author.id
    cIndex = -1
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

async def boom(message, cmd):
    msgId=message.author.id
    cIndex = -1
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

async def leave(message, cmd):
    msgId=message.author.id
    cIndex = -1
    print('leave')
    if cList.count(msgId):
        cIndex = ship.findbycap(msgId)
        if cIndex == -1 :
            cIndex = ship.findbyid(msgId)
            if cIndex > -1:
                ship.callbyindex(cIndex).leaving(msgId)
            cList.remove(msgId)
            await client.send_message(message.channel, 'you just left a boat')
        else :
            if ship.callbyindex(cIndex).captain == msgId:
                await client.send_message(message.channel, 'you can\'t leave your boat')
            else :
                await client.send_message(message.channel, 'you\'re a captain of another boat')
    else:
        await client.send_message(message.channel, 'you\'re not unemployeed')

async def board(message, cmd):
    msgId=message.author.id
    cIndex = -1
    print('board')
    if cList.count(msgId):
        await client.send_message(message.channel, 'he\'s already on crewlist')
    else:
        if cmd[1].startswith('#') and cmd[1][1:].isnumeric() :
            cIndex = int(cmd[1][1:])
            tmpB = ship.callbyindex(cIndex)
            if tmpB is not None :
                if tmpB.boarding(msgId) :
                    cList.append(msgId)
                    await client.send_message(message.channel, 'you just boarded')
                    if tmpB.maxc == len(tmpB.crews) + 1 :
                        await client.send_message(message.server.get_member(tmpB.captain),'당신의 선원이 다 모였습니다. 출항 대기중')
                        pass
                else :
                    await client.send_message(message.channel, 'you failed to get on the boat')
            else :
                await client.send_message(message.channel, 'there\'s no such boat')
        else :
            await client.send_message(message.channel, 'wrong boat number')

async def recruit(message, cmd):
    msgId=message.author.id
    cIndex = -1
    print('recruit')
    if len(ship.sList) > 0 :
        embed=discord.Embed(title="제 1부두",description="뽀트는 중붕이를 태우고-")
        for i in ship.sList :
            bInfo=i.infor()
            if i.state == 0 :
               embed.add_field(name = bInfo[0], value = bInfo[1], inline=True)
        await client.send_message(message.channel,embed=embed)
    pass

async def boatInform(message, cmd):
    msgId=message.author.id
    cIndex = -1
    print("check Information : {} - {}".format(message.author.name, msgId))
    cIndex = ship.findbyid(msgId)
    if cIndex >= 0 :
        msgS = message.server
        tmpS = ship.callbyindex(cIndex)
        await client.send_message(message.channel, '#{}-{} : {} 선장(처녀, 임신가능) ({}/{}-{})'.format(cIndex, tmpS.subject, msgS. get_member(tmpS.captain).name,len(tmpS.crews) +1,tmpS.reqc, tmpS.maxc))
        pass
    else :
        await client.send_message(message.channel, "당신의 배는 없는 거샤아악")
        pass
    pass

async def callMem(message, cmd):
    msgId = message.author.id
    cIndex = -1
    cIndex = ship.findbycap(msgId)
    if cIndex > -1 :
        boat = ship.callbyindex(cIndex)
        #await client.send_message(message.server.get_member(boat.captain),"너는 선장인테치 선원을 부를수 있는테치") 테스트용 선장 호출메시지
        if len(boat.crews) > 0 :
            for c in boat.crews:
                await client.send_message(message.server.get_member(c),'중망호({})의 선장이 선원들을 호출했다.'.format(boat.subject))
                pass
            pass
        else :
            client.send_message()
        pass
    else :
        await client.send_message(message.channel,"너는 선장이 아닌테치!")
        pass
    pass

async def setBoat(message, cmd):
    msgId = message.author.id
    cIndex = -1
    #has attr, get attr, set attr을 사용해서 적절하게 짠다.
    cIndex = ship.findbycap(msgId)
    if cIndex != -1 :
        argv = argParse(cmd[1])
        if len(argv.items()) > 0 :
            boat = ship.callbyindex(cIndex)
            for k,v in argv.items() :
                #print('{} : {}'.format(k,v))
                if boat.has(str(k)) : #has 메서드는 hasattr의 클래스 래핑 함수다.
                    boat.set(str(k),v) #set 메서드도 그렇다
                    pass
            #await client.send_message(message.channel,'변경 완료')
        else :
            print('no args')
        pass
    pass

async def depart(message, cmd) :
    msgId=message.author.id
    cIndex = ship.findbycap(msgId)
    if cIndex != -1 :
        tmpS = ship.callbyindex(cIndex)
        if tmpS.state == 1 :
            await client.send_message(message.channel,"이미 바다에 나가버린 배입니다.")
        elif (len(tmpS.crews) + 1) >= tmpS.reqc :
            tmpS.state = 1 #수정 필요
            await client.send_message(message.channel,"요오시 출항이다!")
        else :
            await client.send_message(message.channel,"바다는 위험하단다. 어서 선원들을 더 모아오렴 (필요 노예 수:{})".format(tmpS.reqc - len(tmpS.crews) -1))
    else :
        await client.send_message(message.channel,"유령선은 출발하지 않는다.")
    pass

async def helpMsg(message, cmd):
    msgId = message.author.id
    embed = discord.Embed(title = '도움!', description = "모든 명령어는 '{}' 으로 시작한다.".format(ctrlch) )
    hDict = dict(zip(cmds,guides))

    for k , v in hDict.items():
        embed.add_field(name = k, value = v , inline = False)
    await client.send_message(message.server.get_member(msgId),embed= embed)

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
        #msgId=message.author.id #길어 함수 내부로 이동
        #cIndex = -1 #index cursor 함수 내부로 이동
        print('ent_msgProc : {}'.format(cmd[0])) #프로시저 진입 메시지 디버깅용

        #딕셔너리 개체 생성후 명령어 목록과 함수 연결시켜서 호출한다.

        if cmd[0] == cmds[0]:
            await boat(message,cmd)
        elif cmd[0] == cmds[1] :
            await boom(message,cmd)
        elif cmd[0] == cmds[2] :
            await board(message,cmd)
        elif cmd[0] == cmds[3] :
            await leave(message,cmd)
        elif cmd[0] == cmds[4] :
            await recruit(message,cmd)
        elif cmd[0] == cmds[5] :
            await boatInform(message,cmd)
        elif cmd[0] == cmds[6] :
            await callMem(message,cmd)
        elif cmd[0] == cmds[7] :
            await setBoat(message,cmd)
        elif cmd[0] == cmds[8] :
            await depart(message,cmd)
        elif cmd[0] == help :
            await helpMsg(message,cmd)
            pass
    return

client.run(Token)
