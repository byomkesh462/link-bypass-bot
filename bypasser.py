import re
import requests
import base64
from urllib.parse import unquote, urlparse, parse_qs
import time
import cloudscraper
from bs4 import BeautifulSoup
from lxml import etree
import hashlib
import json
from dotenv import load_dotenv
load_dotenv()


#################################################################
# gdtot

def gdtot(url,GDTot_Crypt):
    client = cloudscraper.create_scraper(allow_brotli=False)
    match = re.findall(r"https?://(.+)\.gdtot\.(.+)\/\S+\/\S+", url)[0]
    client.cookies.update({ "crypt": GDTot_Crypt })
    res = client.get(url)
    res = client.get(f"https://{match[0]}.gdtot.{match[1]}/dld?id={url.split('/')[-1]}")
    url = re.findall(r'URL=(.*?)"', res.text)[0]
    info = {}
    info["error"] = False
    params = parse_qs(urlparse(url).query)
    if "gd" not in params or not params["gd"] or params["gd"][0] == "false":
        info["error"] = True
        if "msgx" in params:
            info["message"] = params["msgx"][0]
        else:
            info["message"] = "Invalid link"
    else:
        decoded_id = base64.b64decode(str(params["gd"][0])).decode("utf-8")
        drive_link = f"https://drive.google.com/open?id={decoded_id}"
        info["gdrive_link"] = drive_link
    if not info["error"]:
        return info["gdrive_link"]
    else:
        return "Could not generate GDrive URL for your GDTot Link :("


##################################################################################################################        
# AppDrive or DriveApp etc. Look-Alike Link and as well as the Account Details (Required for Login Required Links only)

def unified(url):

    try:

        Email = "OPTIONAL"
        Password = "OPTIONAL"

        account = {"email": Email, "passwd": Password}
        client = cloudscraper.create_scraper(allow_brotli=False)
        client.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
            }
        )
        data = {"email": account["email"], "password": account["passwd"]}
        client.post(f"https://{urlparse(url).netloc}/login", data=data)
        res = client.get(url)
        key = re.findall('"key",\s+"(.*?)"', res.text)[0]
        ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")
        info = re.findall(">(.*?)<\/li>", res.text)
        info_parsed = {}
        for item in info:
            kv = [s.strip() for s in item.split(":", maxsplit=1)]
            info_parsed[kv[0].lower()] = kv[1]
        info_parsed = info_parsed
        info_parsed["error"] = False
        info_parsed["link_type"] = "login"
        headers = {
            "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
        }
        data = {"type": 1, "key": key, "action": "original"}
        if len(ddl_btn):
            info_parsed["link_type"] = "direct"
            data["action"] = "direct"
        while data["type"] <= 3:
            boundary = f'{"-"*6}_'
            data_string = ""
            for item in data:
                data_string += f"{boundary}\r\n"
                data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
            data_string += f"{boundary}--\r\n"
            gen_payload = data_string
            try:
                response = client.post(url, data=gen_payload, headers=headers).json()
                break
            except BaseException:
                data["type"] += 1
        if "url" in response:
            info_parsed["gdrive_link"] = response["url"]
        elif "error" in response and response["error"]:
            info_parsed["error"] = True
            info_parsed["error_message"] = response["message"]
        else:
            info_parsed["error"] = True
            info_parsed["error_message"] = "Something went wrong :("
        if info_parsed["error"]:
            return info_parsed
        if urlparse(url).netloc == "driveapp.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        info_parsed["src_url"] = url
        if urlparse(url).netloc == "drivehub.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if urlparse(url).netloc == "gdflix.pro" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link

        if urlparse(url).netloc == "drivesharer.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if urlparse(url).netloc == "drivebit.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if urlparse(url).netloc == "drivelinks.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if urlparse(url).netloc == "driveace.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if urlparse(url).netloc == "drivepro.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if info_parsed["error"]:
            return "Faced an Unknown Error!"
        return info_parsed["gdrive_link"]
    except BaseException:
        return "Unable to Extract GDrive Link"


#####################################################################################################        
