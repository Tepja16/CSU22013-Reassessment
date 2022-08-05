#!/usr/bin/python3

import requests, json   

from datetime import date

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"


# Some example users to test.
USER_LIST = [
    "Ser Amantio di Nicolao", 
    "BrownHairedGirl",
    "Koavf", 
    "BD2412",
    "Tom.Reding", 
    "Rich Farmbrough", 
    "Jevansen", 
    "Lugnuts", 
    "Materialscientist", 
    "Waacstats",
]


def check_user_existence(user):

    if user == "":
        return False

    PARAMS = {
    "action": "query",
    "format": "json",
    "list": "users",
    "ususers": user,
    "usprop": "blockinfo|groups|editcount|registration|emailable|gender"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    user = DATA["query"]["users"]

    if list(user[0].keys())[1] == 'missing':
        return False
    else:
       
       return True

def get_edits(user):

    PARAMS = {
        "format": "json",
        "rcprop": "title|ids|sizes|flags|user",
        "list": "recentchanges",
        "action": "query",
        "rclimit": "100",
        "rcuser": user
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    RECENTCHANGES = DATA['query']['recentchanges']

    for rc in RECENTCHANGES:
        print()
        for key, val in rc.items():
            #print(str(key) + " : " + str(val))
            if str(key) == "title":
                print("\t" + str(val))

    print()

def get_editcount(user):

    PARAMS = {
    "action": "query",
    "format": "json",
    "list": "users",
    "ususers": user,
    "usprop": "editcount"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    USERS = DATA["query"]["users"]
    user_info = USERS[0]
 
    print()
    print("\t" + user + " has made " + str(user_info['editcount']) + " total edits.")
    print()
    
def get_major_contributions(user):
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "ucuser": user
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    USERCONTRIBS = DATA["query"]["usercontribs"]

    print()
    for uc in USERCONTRIBS:
        keys = uc.keys()
        if 'minor' not in keys:
             print("\t" + "major contribution to: " + str(uc["title"]))
    print()                

def get_minor_contributions(user):
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "ucuser": user
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    USERCONTRIBS = DATA["query"]["usercontribs"]

    print()
    for uc in USERCONTRIBS:
        keys = uc.keys()
        if 'minor' in keys:
            print("\t" + "minor contribution to: " + str(uc["title"]))
    print()
        
def get_original(user):

    PARAMS = {
        "format": "json",
        "rcprop": "title|ids|sizes|flags|user",
        "list": "recentchanges",
        "action": "query",
        "rclimit": "1000000",
        "rcuser": user
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    RECENTCHANGES = DATA['query']['recentchanges']

    print()
    for rc in RECENTCHANGES:
        for key, val in rc.items():
            if str(key) == "type" and str(val) == "new":
                print("\t" + "title: " + rc["title"])
                print("\t" + "page id: " + str(rc["pageid"]))
                print()

def get_page_views(user):

    current_year = date.today().year
    initial_date = str(current_year) + "0101"
    final_date = str(current_year) + "1231"

    PARAMS = {
        "format": "json",
        "rcprop": "title|ids|sizes|flags|user",
        "list": "recentchanges",
        "action": "query",
        "rclimit": "100",
        "rcuser": user
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    RECENTCHANGES = DATA['query']['recentchanges']

    for rc in RECENTCHANGES:
        print()
        for key, val in rc.items():
            #print(str(key) + " : " + str(val))
            if str(key) == "title":
                site_string = str(val).replace(" ", "_")
                headers = {
                "Authority" : "wikimedia.org",
                "User-Agent" : "curl/7.84.0",
                "Accept" : "*/*"
                }
                R = S.get(
                    "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/" + site_string + "/daily/" + initial_date + "00/" + final_date + "00",
                    headers=headers
                )

                R.json()
                DATA = eval(R.text)
                if 'items' in DATA: 
                    views = DATA['items'][0]["views"]
                    print("\tviews for " + str(val) + ":\t " + str(views))
    print()

def get_info():

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": "Albert Einstein",
        "prop": "info",
        "inprop" : "visitingwatchers"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    PAGES = DATA["query"]["pages"]

    print(PAGES)
    
banner = """
                                                                                        _..._     
                                                                                     .-'_..._''.  
             .--.    .    .--.__  __   ___        __.....__                   .--. .' .'      '.\ 
       _     |__|  .'|    |__|  |/  `.'   `.  .-''         '.                 |__|/ .'            
 /\    \\   /.--..'  |    .--|   .-.  .-.   '/     .-''"'-.  `.     .| .-,.--..--. '              
 `\\  //\\ //|  <    |    |  |  |  |  |  |  /     /________\   \  .' |_|  .-. |  | |              
   \`//  \'/ |  ||   | ___|  |  |  |  |  |  |                  |.'     | |  | |  | |              
    \|   |/  |  ||   | \ .|  |  |  |  |  |  \    .-------------'--.  .-| |  | |  . '              
     '       |  ||   |/  .|  |  |  |  |  |  |\    '-.____...---.  |  | | |  '-|  |\ '.          . 
             |__||    /\  |__|__|  |__|  |__| `.             .'   |  | | |    |__| '. `._____.-'/ 
                 |   |  \  \                    `''-...... -'     |  '.| |           `-.______ /  
                 '    \  \  \                                     |   /|_|                    `   
                '------'  '---'                                   `'-'                            
"""

info = """
    Type help for a list of commands and exit to quit.
"""

if __name__ == "__main__":
    print(banner)
    print(info)

    
    u_input = ""
    while u_input != "exit":
        
        u_input = input(":> ")
        l_input = u_input.split()
        u_command = l_input[0]
        u_name = " ".join(l_input[1:])

        if u_command == "quit":
            print()
            print("Goodbye!")
            
            break
        
        elif  u_command == "help":
            print ("""
                check <NAME>    -   Check if the entity is apart of the Wiki collaborative process.

                edits <NAME>    -   Return the last bunch of edits made by the user.

                count <NAME>    -   Return the total number of edits made by the user.

                major <NAME>    -   Return Additive contributions made by the user.

                minor <NAME>    -   Return Maintenance contributions made by the user.

                new <NAME>      -   Return a list of pages initially created by the user.

                views <NAME>    -   Return the number of total views of the 10 pages edited by the user. 

                quit            -   Close the REPL.

            """)
        elif u_command == "check":
            if check_user_existence(u_name):
                print(f'User {u_name} is in database.')
            else:
                print(f'User {u_name} is not in database.')

        elif u_command == "edits":
            if check_user_existence(u_name):
                get_edits(u_name)
            else:
                print(f'User {u_name} is not in database.')

        elif u_command == "count":
            if check_user_existence(u_name):
                get_editcount(u_name)
            else:
                print(f'User {u_name} is not in database.')  

        elif u_command == "major":
            if check_user_existence(u_name):
                get_major_contributions(u_name)
            else:
                print(f'User {u_name} is not in database.')

        elif u_command == "minor":
            if check_user_existence(u_name):
                get_minor_contributions(u_name)
            else:
                print(f'User {u_name} is not in database.')

        elif u_command == "new":
            if check_user_existence(u_name):
                get_original(u_name)
            else:
                print(f'User {u_name} is not in database.')

        elif u_command ==    "views":
            if check_user_existence(u_name):
                get_page_views(u_name)
            else:
                print(f'User {u_name} is not in database.')
        else:
            print("ERROR: please enter in a valid command.")

    



