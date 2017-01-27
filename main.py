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
    dump_user_comments("trekman10", [
        "FULLCOMMUNISM",
        "COMPLETENANARCHY",
        "socialism",
        "LateStageCapitalism",
        "Trotskyism",
        "anarchy"
    ])

