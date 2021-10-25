import requests
import re
import json
import time
import html
from io import BytesIO

# Get user info
print("Enter your username:")
username = input()

print("Enter your password:")
password = input()

print("Enter the studio ID:")
studio_id = input()

print("Enter the command studio ID:")
command_studio_id = input()

with requests.Session() as s:

    # https://github.com/CubeyTheCube/scratchclient/tree/main/scratchclient
    headers = {
        "x-csrftoken": "a",
        "x-requested-with": "XMLHttpRequest",
        "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
        "referer": "https://scratch.mit.edu",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
    }
    data = json.dumps({"username": username,"password": password,"useMessages": "true"})

    # Login with user info
    r = s.post("https://scratch.mit.edu/login/", data=data, headers=headers)
    print(r.status_code)
    session_id = re.search('"(.*)"', r.headers["Set-Cookie"]).group()
    token = r.json()[0]["token"]

    # Set headers
    headers = {
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchlanguage=en;permissions=%7B%7D;",
            "referer": "https://scratch.mit.edu"
    }

    # Get CSRF token
    r = s.get("https://scratch.mit.edu/csrf_token/", headers=headers)
    print(r.status_code)
    csrf_token = re.search(
            "scratchcsrftoken=(.*?);", r.headers["Set-Cookie"]
    ).group(1)

    # Update headers with the CSRF token, token, and cookies

    headers = {
        "x-csrftoken": csrf_token,
        "X-Token": token,
        "x-requested-with": "XMLHttpRequest",
        "Cookie": "scratchcsrftoken="
        + csrf_token
        + ";scratchlanguage=en;scratchsessionsid="
        + session_id
        + ";",
        "referer": "https://scratch.mit.edu",
    }

    print(csrf_token)

    # Get session data
    session = s.get("https://scratch.mit.edu/session/", headers=headers)
    print(session.status_code)
    print(session.text)

    def set_title(studio_id, content):
        data = json.dumps({"title": content})

        headers["referer"] = (
            "https://scratch.mit.edu/studios/" + studio_id + "/comments/"
        )

        r = s.put("https://scratch.mit.edu/site-api/galleries/all/" + studio_id + "/", data=data, headers=headers)
        print(r.status_code)

    def set_description(studio_id, content):
        data = json.dumps({"description": content})
        headers["referer"] = (
            "https://scratch.mit.edu/studios/" + studio_id + "/"
        )

        r = s.put("https://scratch.mit.edu/site-api/galleries/all/" + studio_id + "/", data=data, headers=headers)
        print(r.status_code)

    def set_thumbnail(src):
        r = requests.get(thumbnail_src)
        print(r.content)
        files = {"file": BytesIO(r.content)}
        headers["referer"] = (
            "https://scratch.mit.edu/studios/" + studio_id + "/"
        )

        r = s.post("https://scratch.mit.edu/site-api/galleries/all/" + studio_id + "/", files=files, headers=headers)
        print(r.status_code)

    def toggle_comments(studio_id):
        headers["referer"] = (
            "https://scratch.mit.edu/studios/" + studio_id + "/comments/"
        )

        r = s.post("https://scratch.mit.edu/site-api/comments/gallery/" + studio_id + "/toggle-comments/", headers=headers)
        print(r.status_code)

    # Get top comment ID to avoid excecuting commands before the program starts
    r = s.get("https://api.scratch.mit.edu/studios/" + studio_id + "/comments/")
    j = json.loads(r.text)
    top_comment_id = j[0]["id"]
    print(top_comment_id)

    # Get a list of managers
    r = s.get("https://api.scratch.mit.edu/studios/" + studio_id + "/managers/")
    j = json.loads(r.text)
    managers = []
    print(len(j))
    for x in range(len(j)):
        managers.append(j[x]["username"])
    print(managers)

    # Check for commands and excecute them every 5 minutes
    while(True):
        time.sleep(300) # Wait 300 seconds (5 minutes) between requests
        r = s.get("https://api.scratch.mit.edu/studios/" + command_studio_id + "/comments/") # Check the command studio for commands
        j = json.loads(r.text)
        print(json.dumps(j, indent=4))
        title = None
        description_id = None
        thumbnail_studio = None
        toggle_comments_num = 0

        for x in range(0, len(j)): # Check for commands in the comments
            if j[len(j)-1-x]["id"] > top_comment_id:
                c = j[len(j)-1-x]["content"].split(" ", 1)[0]
                u = j[len(j)-1-x]["author"]["username"]
                if c == "!t" and u in managers:
                    title = html.unescape(j[len(j)-1-x]["content"].split(" ", 1)[1])
                elif c == "!d" and u in managers:
                    description_id = j[len(j)-1-x]["content"].split(" ", 1)[1]
                elif c == "!b" and u in managers:
                    thumbnail_studio = j[len(j)-1-x]["content"].split(" ", 1)[1]
                elif c == "!c" and u in managers:
                    toggle_comments_num += 1

        # Excecute commands
        if title != None:
            set_title(studio_id, title)

        if description_id != None:
            r = s.get("https://api.scratch.mit.edu/studios/" + description_id + "/")
            description_content = json.loads(r.text)["description"]
            r = s.get("https://api.scratch.mit.edu/studios/" + studio_id + "/")
            print(json.loads(r.text)["description"])
            set_description(studio_id, description_content)

        if toggle_comments_num%2 == 1:
            toggle_comments(studio_id)

        if thumbnail_studio != None:
            thumbnail_src = "https://cdn2.scratch.mit.edu/get_image/gallery/" + thumbnail_studio + "_170x100.png";
            set_thumbnail(thumbnail_src)

        # Update top comment ID, to avoid excecuting the same command multiple times
        top_comment_id = j[0]["id"]
