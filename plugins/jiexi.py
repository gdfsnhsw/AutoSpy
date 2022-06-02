## 京东口令解析

PandaToken = ''
Version = "0.0.1"
try:
    import requests
    import yaml
    import json
    import asyncio
    from auto_spy import client, chat_id, sendmsg_deledit, sendmsg_del, msg_add_del
    from telethon import events
    import re
    import os
    import traceback
    import sys

except:
    import os
    os.system("pip3 install requests")
    os.system('pip3 install pyyaml')
    os.system("pip3 install lxml beautifulsoup4")
    os.system("pip install lxml beautifulsoup4")
    import asyncio
    import re
    from auto_spy import client, chat_id, get_ck, sendmsg_del, sendmsg_deledit, sendmsg_del, msg_add_del
    from telethon import events
    import yaml
    import requests
    import json
    import traceback
    import sys
    pass

cfg = {}
cfgpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "jiexi.yaml")

if not os.path.exists(cfgpath):
    with open(cfgpath, "w") as f:
        cfg["token"] = ''
        yaml.dump(cfg, f, allow_unicode=True)
        pass

with open(cfgpath, 'r') as f:
    cfg = yaml.safe_load(f)


@client.on(events.NewMessage(pattern=r'^jx'))
async def jx(event):
    if event.message.sender_id not in chat_id:
        return

    # await msg_add_del(event.chat_id, event.message, 0)

    args = event.text.split(" ")

    if args[0] != 'jx':
        return

    if len(args) > 1:
        if args[0] == 'jx' and args[1] == 'token' and len(args) == 2:
            await sendmsg_del(event.chat_id, cfg['token'])
            return
        if len(args) == 3:
            cfg['token'] = args[2]
            with open(cfgpath, 'w') as f:
                yaml.dump(cfg, f, allow_unicode=True)
            await sendmsg_del(event.chat_id, "token保存成功")
        return


    if cfg["token"] == '':
        await sendmsg_del(event.chat_id, "token 没有设置哦~\njx token <token>")
        return
    try:
        replymsg = await event.get_reply_message()
        replytext=replymsg.text
    except ValueError:
        return await sendmsg_del(event.chat_id, "获取回复信息失败")
        
    msg = await sendmsg_deledit(event.chat_id, f"正在解析......", event.message)
    
    try:
        token = cfg['token']
        header = {"Authorization": "Bearer " + token}
        res = requests.post("https://api.zhezhe.cf/jd/jcommand", headers=header, json={"code": replytext}, timeout=20)
        data = res.json()

    except:
        return await sendmsg_deledit(event.chat_id, "[解析] 网络错误！", msg)
        
    if data["code"] != 200:
        return await sendmsg_deledit(event.chat_id, "[jx] 未找到 JD 口令！", msg)
    else:
        tstr = f'[活动详情]:{data["data"]["title"]}\n' \
               f'[口令创建人]:{data["data"]["userName"]}\n' \
               f'[活动地址]:{data["data"]["jumpUrl"]}'
        await sendmsg_deledit(event.chat_id, tstr, msg)
        try:
            data = data["data"]["jumpUrl"]
            if "pool" in data :
                url = re.findall(r"(.+?)/pool", data) 
            #组队    
            elif "wxTeam" in data :
                url = re.findall(r"(.+?)/wxTeam", data) 
                url = re.sub('\[\'|\'\]', '', f"{url}")
                id1 = re.findall(r"activityId=(.+?)&signUuid", data)
                id1 = re.sub('\[\'|\'\]', '',f"{id1}")
                if "lzkjdz" in url :
                    await sendmsg_del(event.chat_id, f'组队瓜分变量：\nexport jd_zdjr_activityId="{id1}"')
                elif "cjhydz" in url :
                    await sendmsg_del(event.chat_id, f'CJ组队瓜分变量：\nexport jd_cjhy_activityId="{id1}"')
                else:
                    await sendmsg_del(event.chat_id, '未检测到相关变量信息')
            #集卡     
            elif "wxCollectCard" in data :
                url2 = re.findall(r"(.+?)&shareUuid", data) 
                url2 = re.sub('\[\'|\'\]', '', f"{url2}")
                id2 = re.findall(r"(.+?)&shareUuid", data)
                id2 = re.sub('\[\'|\'\]', '',f"{id2}")
                if "wxCollectCard" in url2 :
                    await sendmsg_del(event.chat_id, f'集卡变量：\nM_WX_COLLECT_CARD_UR={id2}')
                else:
                    await sendmsg_del(event.chat_id,'未检测到相关变量信息')
           #开卡     
            elif "wxInviteActivity" in data :
                url3= re.findall(r"(.+?)&invite", data) 
                url3 = re.sub('\[\'|\'\]', '', f"{url3}")
                id3 = re.findall(r"venderId=(.+?)&activityId", data)
                id3 = re.sub('\[\'|\'\]', '',f"{id3}")
                if "venderId=" in url3 :
                    await sendmsg_del(event.chat_id, f'监听并解析到开卡入会变量：\nexport VENDER_ID={id3}')
                else:
                    await sendmsg_del(event.chat_id,'未检测到相关变量信息')
           #微订制     
            elif "microDz" in data :
                url4 = re.findall(r"(.+?)/index", data) 
                url4 = re.sub('\[\'|\'\]', '', f"{url4}")
                id4 = re.findall(r"activityId=(.+?)&inviter=", data)
                id4 = re.sub('\[\'|\'\]', '',f"{id4}")
                if "/wx/view" in url4 :
                    await sendmsg_del(event.chat_id, f'微定制变量：\nexport jd_cjhy_activityId60={id4}')
                else:
                    await sendmsg_del('未检测到相关变量信息')

           #分享有礼     
            elif "wxShareActivity" in data :
                url5 = re.findall(r"(.+?)&friendUuid", data) 
                url5 = re.sub('\[\'|\'\]', '', f"{url5}")
                id5 = re.findall(r"activityId=(.+?)&friendUuid=", data)
                id5 = re.sub('\[\'|\'\]', '',f"{id5}")
                if "wxShareActivity" in url5 :
                    await sendmsg_del(event.chat_id, f'分享有礼变量：\nexport jd_fxyl_activityId={id5}')
                else:
                    await sendmsg_del(event.chat_id, '未检测到相关变量信息')
           #M幸运抽奖     
            elif "lzclient" in data :
                url6 = re.findall(r"(.+?)&shareuserid", data) 
                url6 = re.sub('\[\'|\'\]', '', f"{url6}")
                id6 = re.findall(r"activityId=(.+?)&shareuserid", data)
                id6 = re.sub('\[\'|\'\]', '',f"{id6}")
                if "lzclient" in url6 :
                    await sendmsg_del(event.chat_id, f'M幸运抽奖变量：\nexport  M_WX_LUCK_DRAW_URL={url6}')
                else:
                    await sendmsg_del(event.chat_id,'未检测到相关变量信息')
            #转盘抽奖     
            # elif "gameType" in data :
                # url7 = re.findall(r"(.+?)&gameType=", data) 
                # url7 = re.sub('\[\'|\'\]', '', f"{url7}")
                # id7 = re.findall(r"activityId=(.+?)&gameType", data)
                # id7 = re.sub('\[\'|\'\]', '',f"{id7}")
                # if "activityId" in url7 :
                    # await event. sendmsg_deledit(f'监听并解析到转盘抽奖变量：\nexport M_WX_LUCK_DRAW_URL="{url7}"\n解析大师祝您薅豆愉快！！')
                # else:
                    # await event. sendmsg_deledit('未检测到相关变量信息')           
            else:
                await sendmsg_del(event.chat_id,'未检测到相关变量信息')
                
                
            # uri = data.split("=")[1].split("&")[0]
            # await event. sendmsg_deledit(f'【jdjx】export jd_zdjr_activityId = "{uri}"')
        except KeyError:
            return await sendmsg_del(event.chat_id, "解析错误")
    