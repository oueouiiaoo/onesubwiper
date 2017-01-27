#!/usr/bin/python

import subprocess
import json
import sys
import time

def dump_user_comments(username):
    url = "https://pay.reddit.com/user/" + username + "/comments.json?t=all&limit=100&sort=new"
    while True:
        jsonresponse = json.loads(subprocess.check_output([
            "curl",
            "-s",
            url
        ]).decode("utf-8"))
        if "data" in jsonresponse:
            for child in jsonresponse["data"]["children"]:
                if child["data"]["subreddit"] == "FULLCOMMUNISM":
                    print("[ Subreddit ] " + child["data"]["subreddit"])
                    print("[ Fullname ] " + child["data"]["name"])
                    print("[ Comment ] " + child["data"]["body"] + "\n")
            if jsonresponse["data"]["after"] == None:
                break
            else:
                print("[ After ] " + jsonresponse["data"]["after"])
                url = "https://pay.reddit.com/user/" + username + "/comments.json?t=all&limit=100&sort=new"
                url = url + "&after=" + jsonresponse["data"]["after"]
        else:
            print(jsonresponse)
            time.sleep(2)

def main():
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

if __name__ == "__main__":
    dump_user_comments("trekman10")

