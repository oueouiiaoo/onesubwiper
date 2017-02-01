#!/usr/bin/python

import subprocess
import json
import sys
import time

def dump_user_comments(username, subreddits):
    url = "https://pay.reddit.com/user/" + username + "/comments.json?t=all&limit=100&sort=new"
    commentcount = 0
    commentsprinted = 0
    while True:
        jsonresponse = json.loads(subprocess.check_output([
            "curl",
            "-s",
            url
        ]).decode("utf-8"))
        if "data" in jsonresponse:
            for child in jsonresponse["data"]["children"]:
                if child["data"]["subreddit"] in subreddits:
                    print(child["data"]["subreddit"] + ":: " + child["data"]["link_title"])
                    # print("[ Fullname ] " + child["data"]["name"])
                    print(child["data"]["body"] + "\n\n\n")
                    commentsprinted += 1
                commentcount += 1
            if jsonresponse["data"]["after"] == None:
                # print("[ Downloaded " + str(commentcount) + " comments ]")
                # print("[ Printed " + str(commentsprinted) + " comments ]")
                break
            else:
                # print("[ After ] " + jsonresponse["data"]["after"])
                url = "https://pay.reddit.com/user/" + username + "/comments.json?t=all&limit=100&sort=new"
                url = url + "&after=" + jsonresponse["data"]["after"]
        else:
            pass
            # print(jsonresponse)
            # time.sleep(1)

def dump_user_comment_fullnames(username, subreddits):
    url = "https://pay.reddit.com/user/" + username + "/comments.json?t=all&limit=100&sort=new"
    commentcount = 0
    commentsprinted = 0
    while True:
        jsonresponse = json.loads(subprocess.check_output([
            "curl",
            "-s",
            url
        ]).decode("utf-8"))
        if "data" in jsonresponse:
            for child in jsonresponse["data"]["children"]:
                if child["data"]["subreddit"] in subreddits:
                    print(child["data"]["name"])
                    commentsprinted += 1
                commentcount += 1
            if jsonresponse["data"]["after"] == None:
                print(str(commentsprinted) + " total")
                break
            else:
                url = "https://pay.reddit.com/user/" + username + "/comments.json?t=all&limit=100&sort=new"
                url = url + "&after=" + jsonresponse["data"]["after"]
        else:
            pass
            # print(jsonresponse)
            # time.sleep(1)

def get_user_comment_fullnames(username, subreddits):
    url = "https://pay.reddit.com/user/" + username + "/comments.json?t=all&limit=100&sort=new"
    fullnames = []
    while True:
        jsonresponse = json.loads(subprocess.check_output([
            "curl",
            "-s",
            url
        ]).decode("utf-8"))
        if "data" in jsonresponse:
            for child in jsonresponse["data"]["children"]:
                if child["data"]["subreddit"] in subreddits:
                    fullnames.append(child["data"]["name"])
            if jsonresponse["data"]["after"] == None:
                break
            else:
                url = "https://pay.reddit.com/user/" + username + "/comments.json?t=all&limit=100&sort=new"
                url = url + "&after=" + jsonresponse["data"]["after"]
    return fullnames

def old_main():
    clientid = ""
    secret = ""
    username = sys.argv[1]
    password = sys.argv[2]
    jsonresponse = json.loads(subprocess.check_output([
        "curl",
        "-X",
        "POST",
        "-d",
        "grant_type=password&username=" + username + "&password=" + password,
        "-s",
        "--user",
        clientid + ":" + secret,
        "https://www.reddit.com/api/v1/access_token"]).decode("utf-8"))
    if "access_token" in jsonresponse:
        access_token = jsonresponse["access_token"]
        print(json.loads(subprocess.check_output([
            "curl",
            "-s",
            "-H",
            "Authorization: bearer " + access_token,
            "https://oauth.reddit.com/api/v1/me/karma"]).decode("utf-8")))
    else:
        print("The response did not include an access token")

def edit_comments(clientid, secret, username, password, fullnames, note):
    access_token = None
    while True:
        jsonresponse = json.loads(subprocess.check_output([
            "curl",
            "-s",
            "-X",
            "POST",
            "-d",
            "grant_type=password&username=" + username + "&password=" + password,
            "--user",
            clientid + ":" + secret,
            "https://www.reddit.com/api/v1/access_token"
        ]).decode("utf-8"))
        if "access_token" in jsonresponse:
            access_token = jsonresponse["access_token"]
            print(access_token)
            break
        else:
            print("We did not get an access token.")
    for name in fullnames:
        print(subprocess.check_output([
            "curl",
            "-s",
            "-X",
            "POST",
            "-H",
            "Authorization: bearer " + access_token,
            "-d",
            "api_type=json&text=" + note + "&thing_id=" + name,
            "https://oauth.reddit.com/api/editusertext"
        ]).decode("utf-8"))

if __name__ == "__main__":
    useragent = "onesubwiper 1.0"
    access_token = None
    while access_token == None:
        sys.stdout.write("(code) ")
        sys.stdout.flush()
        code = sys.stdin.readline()
        while access_token == None:
            jsonres = json.loads(subprocess.check_output([
                "curl", "-s", "-A", useragent, "-X", "POST", "-d",
                "grant_type=authorization_code&code=" + code.splitlines()[0] + "&redirect_uri=https://oueouiiaoo.github.io/onesubwiper/index.html",
                "--user", "VScq0j6VBmWeig:", "https://www.reddit.com/api/v1/access_token"
            ]).decode("utf-8"))
            if "access_token" in jsonres:
                access_token = jsonres["access_token"]
            if "error" in jsonres:
                if jsonres["error"] == "invalid_grant":
                    break
    username = None
    while username == None:
        print(subprocess.check_output([
            "curl", "-s", "-A", useragent,
            "-H", "Authorization: bearer " + access_token,
            "https://oauth.reddit.com/api/v1/me"
        ]).decode("utf-8"))
    
