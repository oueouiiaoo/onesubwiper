#!/usr/bin/python

import subprocess
import json
import sys

if __name__ == "__main__":
    print("oueouiiaoo.github.io/onesubwiper/")
    print("- enter the code from the website to authorize onesubwiper")
    print("  copying and pasting really helps if you can")
    print("- a list of the subreddits you have comments on will appear")
    print("- copy out the name of the subreddit who's comments you")
    print("  want to replace and press enter")
    print("- enter the text you wish to have replace those comments")
    print("- repeat for all desired subs")
    print("- when you're done you can exit by pressing enter without")
    print("- typing in the name of a sub")
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
        jsonres = json.loads(subprocess.check_output([
            "curl", "-s", "-A", useragent,
            "-H", "Authorization: bearer " + access_token,
            "https://oauth.reddit.com/api/v1/me"
        ]).decode("utf-8"))
        if "name" in jsonres:
            username = jsonres["name"]
    print(username)
    comments = {}
    commenturl = "https://pay.reddit.com/user/" + username + "/comments.json?t=all&limit=100&sort=new"
    while True:
        jsonres = json.loads(subprocess.check_output(["curl", "-s", "-A", useragent, commenturl]).decode("utf-8"))
        if "data" in jsonres:
            for child in jsonres["data"]["children"]:
                if child["data"]["subreddit"] in comments:
                    comments[child["data"]["subreddit"]].append(child["data"]["name"])
                else:
                    comments[child["data"]["subreddit"]] = []
                    comments[child["data"]["subreddit"]].append(child["data"]["name"])
            if jsonres["data"]["after"] == None:
                break
            else:
                commenturl = "https://pay.reddit.com/user/" + username + "/comments.json?t=all&limit=100&sort=new"
                commenturl = commenturl + "&after=" + jsonres["data"]["after"]
    while True:
        totalcomments = 0
        for sub in comments:
            totalcomments += len(comments[sub])
            print(sub + " " + str(len(comments[sub])) + " " + str(totalcomments) + "+")
        sys.stdout.write("(subreddit) ")
        sys.stdout.flush()
        subreddit = sys.stdin.readline().splitlines()[0]
        if subreddit == "":
            quit()
        sys.stdout.write("(replacement) ")
        sys.stdout.flush()
        replacement = sys.stdin.readline().splitlines()[0]
        if subreddit in comments:
            for fullname in comments[subreddit]:
                subprocess.check_output(["curl", "-s", "-A", useragent, "-X", "POST",
                    "-H", "Authorization: bearer " + access_token,
                    "-d", "api_type=json&text=" + replacement + "&thing_id=" + fullname,
                    "https://oauth.reddit.com/api/editusertext"])
            comments.pop(subreddit)

