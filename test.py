import requests
import time
import webbrowser

cookiesFile = open("cookies.txt", "r")
lnumber = 1

groupsWithFunds = []

for cookie in cookiesFile:
    r = requests.Session()
    r.cookies[".ROBLOSECURITY"] = cookie.rstrip("\n")

    getUserInfo = r.get("https://users.roblox.com/v1/users/authenticated")
    if getUserInfo.status_code == 401:
        print("Invalid cookie in line number:", lnumber)
        lnumber += 1
    else:
        lnumber += 1
        userName, userID = getUserInfo.json()['name'], getUserInfo.json()['id']
        print("Username:", userName, "User ID:", userID); print("")
        groupsTbl = r.get(f"https://groups.roblox.com/v1/users/{userID}/groups/roles").json()
        print("Funds \t Group ID \t Group Name"); print("-------------------------------------")

        robuxTotal = 0

        rateLimited = []
        for i in groupsTbl['data']:
            groupID, groupName = i['group']['id'], i['group']['name']
            if i['role']['rank'] == 255:
                checkFunds = r.get(f"https://economy.roblox.com/v1/groups/{groupID}/currency")
                if checkFunds.status_code == 200:
                    robux = checkFunds.json().get('robux', 0)
                    print(f"{robux:<9}{groupID}\t {groupName.encode('utf-8')}")
                    robuxTotal += robux
                    if robux > 0:
                        groupsWithFunds.append(groupID)
                    time.sleep(0) 
                elif checkFunds.status_code == 429:
                    print(f"{'WAIT':<9}{'RATELIMITED':<9}\t WAIT")
                    rateLimited.append({"id": groupID, "name": groupName})
                    time.sleep(30)
 
        for i in rateLimited:
            checkFunds = r.get(f"https://economy.roblox.com/v1/groups/{i['id']}/currency")
            if checkFunds.status_code == 200:
                robux = checkFunds.json().get('robux', 0)
                print(f"{robux:<9}{i['id']}\t {i['name'].encode('utf-8')}")
                robuxTotal += robux
                if robux > 0:
                    groupsWithFunds.append(i['id'])
                rateLimited.remove(i)
            elif checkFunds.status_code == 429:
                print(f"{'0':<9}{'0':<9}\t RATELIMITED")
                rateLimited.append(i)
                time.sleep(30)

        print(f"Total amount of Robux is: {robuxTotal}")

for groupID in groupsWithFunds:
    webbrowser.open(f"https://www.roblox.com/groups/{groupID}/groupName#!/about")
