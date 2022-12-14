import pyrogram
from pyrogram import Client
from pyrogram import filters
import bypasser
import os
import ddl
import requests
import threading

# bot ENVs(required)
bot_token = os.environ.get("TOKEN", "")
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  

# Optional ENVs
GDTot_Crypt = os.environ.get("CRYPT","MVlCa3M1b2xrY1loaHpxUWxLWXBtS0dMZVA4b3ZSY2J0ZWJjOW1vV0c4UT0%3D")
Laravel_Session = os.environ.get("Laravel_Session","")
XSRF_TOKEN = os.environ.get("XSRF_TOKEN","")
KCRYPT = os.environ.get("KOLOP_CRYPT","")
DCRYPT = os.environ.get("DRIVEFIRE_CRYPT","")
HCRYPT = os.environ.get("HUBDRIVE_CRYPT","")
KATCRYPT = os.environ.get("KATDRIVE_CRYPT","")


# main thread
def mainthread(cmd,message):

    try:
        url = str(message.reply_to_message.text)
    except:
        try:
            url = str(message.text.split(f"{cmd} ")[1])
        except:
            app.send_message(message.chat.id, f"❌Invalid format\nEither **reply** to a __link__ or use inline command like this -> **{cmd} link**", reply_to_message_id=message.id)
            return

        
    # direct download link
    if cmd == "/dl":
        print("You Have Entered ddl:",url)
        msg = app.send_message(message.chat.id, "⚡ __generating...__", reply_to_message_id=message.id)
        link = ddl.direct_link_generator(url)
           
           
    # gdtot url
    elif cmd == "/gd":
        print("Entered gdtot Link:",url)
        msg = app.send_message(message.chat.id, "🔎Generating gdrive link for your **gdtot** URL...", reply_to_message_id=message.id)
        link = bypasser.gdtot(url,GDTot_Crypt)
        


    # appdrive look alike links
    elif cmd == "/app":
        print("Entered appdrive-look-alike link:",url)
        msg = app.send_message(message.chat.id, "🔎Generating gdrive link, please wait...", reply_to_message_id=message.id)
        link = bypasser.unified(url)

  
    # finnaly
    try:
        app.edit_message_text(message.chat.id, msg.id, f'**Original Link**- {url}\n\n**Gdrive link**- {link}')
    except:
        app.edit_message_text(message.chat.id, msg.id, "❌Failed to Bypass.")


AvailableCommands = ['dl','gd','app']
# commands
@app.on_message(filters.command(AvailableCommands))
def receive(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bypass = threading.Thread(target=lambda:mainthread(message.text.split(" ")[0],message),daemon=True)
    bypass.start()


# start command
@app.on_message(filters.command(["start"]))
def send_welcome(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, "🔗 **Available commands** \n\n  \
 /dl - __direct download link (/ddllist)__ \n  \
 /app - __appdrive look-alike links (/applist)__ \n  \
 /gd - __gdtot links__ \n\n\
reply to the link with command or use inline format /cmd link",
reply_to_message_id=message.id)


# app list
@app.on_message(filters.command(['applist']))
def gdlis(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    list = """**Supported sites**\n\n- appdrive.in \n\
- driveapp.in \n\
- drivehub.in \n\
- gdflix.pro \n\
- drivesharer.in \n\
- drivebit.in \n\
- drivelinks.in \n\
- driveace.in \n\
- drivepro.in \n\
"""
    app.send_message(message.chat.id, list, reply_to_message_id=message.id)


# others list
@app.on_message(filters.command(['otlist']))
def otlis(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    list="""__- exe.io/exey.io \n\
- sub2unlock.net/sub2unlock.com \n\
- rekonise.com \n\
- letsboost.net \n\
- ph.apps2app.com \n\
- mboost.me	\n\
- sub4unlock.com \n\
- ytsubme.com \n\
- bit.ly \n\
- social-unlock.com	\n\
- boost.ink	\n\
- goo.gl \n\
- shrto.ml \n\
- t.co \n\
- tinyurl.com
    __"""
    app.send_message(message.chat.id, list, reply_to_message_id=message.id)    


# ddl list
@app.on_message(filters.command(['ddllist']))
def ddllis(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    list="""__- disk.yandex.com \n\
- mediafire.com \n\
- uptobox.com \n\
- osdn.net \n\
- github.com \n\
- hxfile.co \n\
- anonfiles.com \n\
- letsupload.io \n\
- 1drv.ms(onedrive) \n\
- pixeldrain.com \n\
- antfiles.com \n\
- streamtape.com \n\
- bayfiles.com \n\
- racaty.net \n\
- 1fichier.com \n\
- solidfiles.com \n\
- krakenfiles.com \n\
- upload.ee \n\
- mdisk.me \n\
- wetransfer.com \n\
- gofile.io \n\
- dropbox.com \n\
- zippyshare.com \n\
- megaup.net \n\
- fembed.net, fembed.com, femax20.com, fcdn.stream, feurl.com, layarkacaxxi.icu, naniplay.nanime.in, naniplay.nanime.biz, naniplay.com, mm9842.com \n\
- sbembed.com, watchsb.com, streamsb.net, sbplay.org
    __"""
    app.send_message(message.chat.id, list, reply_to_message_id=message.id)     


# server loop
print("bot started")
app.run()
