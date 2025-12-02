try:
    from random import choice
    import requests
    from PIL import Image
    from io import BytesIO
    import os, sys
except Exception as e:
    print(f"1 or more modules not found\nInstall the module using 'pip install [module]'\n{e}")

def play_audio(content):
    # Save audio to a temporary file
    tmp_file = "temp_audio.ogg"
    with open(tmp_file, "wb") as f:
        f.write(content)
    
    # Play depending on OS
    if sys.platform.startswith("win"):  # Windows
        os.system(f"start {tmp_file}")  # Opens default audio player
    elif sys.platform.startswith("darwin"):  # macOS
        os.system(f"afplay {tmp_file}")
    else:  # Linux
        os.system(f"ffplay -nodisp -autoexit {tmp_file}")  # Requires ffplay

def show_image(content):
    img = Image.open(BytesIO(content))
    img.show()

def get_cat_err_img(errcode: int):
    url = f"https://http.cat/{errcode}"
    r = requests.get(url)
    if r.status_code == 200:
        show_image(r.content)
    return f"Errorcode: {errcode}"

def cinput(prompt):
    """Custom input"""
    data = input(prompt).strip().lower()
    return data

def preview_list(lst):
    """Preview a list for the user, showing index and brief description."""
    for i, item in enumerate(lst[:10]):  # show only first 10 for readability
        if isinstance(item, dict):
            keys = ", ".join(item.keys())
            print(f"{i}: dict with keys [{keys}]")
        elif isinstance(item, list):
            print(f"{i}: list of length {len(item)}")
        else:
            print(f"{i}: {item}")
    if len(lst) > 10:
        print(f"...and {len(lst)-10} more items")

def drill(data, path="root"):
    """Recursively let the user select keys/items from dicts or lists."""
    while isinstance(data, (dict, list)):
        if isinstance(data, dict):
            keys = list(data.keys())
            print(f"\nCurrent path: {path}")
            choice = cinput(f"Choose a key ({', '.join(keys)}): ")
            if choice not in data:
                print("Invalid key. Try again.")
                continue
            data = data[choice]
            path += f"->{choice}"
        elif isinstance(data, list):
            print(f"\nCurrent path: {path}")
            preview_list(data)
            idx = cinput(f"Choose an index (0-{len(data)-1}): ")
            try:
                idx = int(idx)
                data = data[idx]
                path += f"[{idx}]"
            except (ValueError, IndexError):
                print("Invalid index. Try again.")
                continue
    return data

class APIS:
    @staticmethod
    def get_ip():
        """
        Returns current IP address
        """
        url = "https://api.ipify.org?format=json"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            ip = data["ip"]
        else:
            return get_cat_err_img(r.status_code)
        
        url = f"http://ip-api.com/json/{ip}?"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            country = data["country"]
            city = data["city"]
            zipcode = data["zip"]
            lat = data["lat"]
            lon = data["lon"]
            organisation = data["org"]


            return (f"Your IP address is {ip}.\nExtra info:\nLocation: {city}, {country} with ZIP-code {zipcode}.\nCoordinates: {lat}, {lon}.\nThe WiFi is owned by {organisation}")
        else:
            return get_cat_err_img(r.status_code)

    @staticmethod
    def get_random_user():
        """
        Returns a dict with 
        - Gender
        - Name
        - Date of birth
        - Age
        - Location
        """
        url = "https://randomuser.me/api/"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            results = data["results"][0]
            return {
                "Gender" : f"{results["gender"]}",
                "Name" : f"{results["name"]["first"]} {results["name"]["last"]}",
                "Date of birth" : f"{results["registered"]["date"].split("T")[0]}",
                "Age" : f"{results["registered"]["age"]}",
                "Location" : f"{results["location"]["city"]}, {results["location"]["country"]}"
            }
            #print(results) print for full API response
        else:
            return get_cat_err_img(r.status_code)
    
    @staticmethod
    def get_dog_img():
        url = "https://dog.ceo/api/breeds/image/random"
        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()
            image_url = data["message"]
            img_data = requests.get(image_url).content
            return show_image(img_data)
        else:
            return get_cat_err_img(r.status_code)
        
    @staticmethod
    def get_fox_img():
        url = "https://randomfox.ca/floof/"
        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()
            image_url = data["image"]
            img_data = requests.get(image_url).content
            return show_image(img_data)
        else:
            return get_cat_err_img(r.status_code)
        
    @staticmethod
    def get_noise_img(rgb:tuple=(255,255,255), nrtiles:int=50, tileSize:int=7, borderWidth:int=0):
        """
        - (Red, Green, Blue), default: (255, 255, 255)
        - Number of tiles (1-50), default: 50
        - Tilesize in px (1-20), default: 7
        - Borderwidth (grid) in px (0-15), default: 0
        """
        url = f"https://php-noise.com/noise.php?r={rgb[0]}&g={rgb[1]}&b={rgb[2]}&tiles={nrtiles}&tileSize={tileSize}&borderWidth={borderWidth}&json"
        r = requests.get(url)

        if r.status_code == 200:
            return show_image(r.content)
        else:
            return get_cat_err_img(r.status_code)
        
    @staticmethod
    def get_robot_img(prompt):
        url = f"https://robohash.org/{prompt}"
        r = requests.get(url)

        if r.status_code == 200:
            return show_image(r.content)
        else:
            return get_cat_err_img(r.status_code)
        
    @staticmethod
    def get_minecraft_skin(username, skinpart, overlay=False):
        skinparts = ["head", "head3d", "body", "body3d"]

        if skinpart in skinparts:
            mojang_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
            r = requests.get(mojang_url)
            if r.status_code == 200:
                data = r.json()
                uuid = data["id"]
                if skinpart == "uuid":
                    return uuid
            else:
                return get_cat_err_img(r.status_code)

            if skinpart == "head":
                crafatar_url = f"https://crafatar.com/avatars/{uuid}?{"overlay" if overlay else ""}"
            elif skinpart == "head3d":
                crafatar_url = f"https://crafatar.com/renders/head/{uuid}?{"overlay" if overlay else ""}"
            elif skinpart == "body3d":
                crafatar_url = f"https://crafatar.com/renders/body/{uuid}?{"overlay" if overlay else ""}"
            elif skinpart == "body":
                crafatar_url = f"https://crafatar.com/skins/{uuid}"
            r = requests.get(crafatar_url)
            if r.status_code == 200:
                return show_image(r.content)
            else:
                return get_cat_err_img(r.status_code)
        else:
            return f"Skin parts: {', '.join(skinparts)}"
        
    @staticmethod
    def get_minecraft_block(block):
        url = f"https://assets.mcasset.cloud/1.21.10/assets/minecraft/textures/block/{block}.png"
        r = requests.get(url)
        if r.status_code == 200:
            return show_image(r.content)
        else:
            return get_cat_err_img(r.status_code)
    
    @staticmethod
    def get_f2p_games(get_all: bool = False, get_random: bool = False, game_id = None, category: str = "", platform: str = ""):
        categories = [
            "mmorpg", "shooter", "strategy", "moba", "racing",
            "sports", "social", "sandbox", "open-world", "survival",
            "pvp", "pve", "pixel", "voxel", "zombie",
            "turn-based", "first-person", "third-person", "top-down", "tank",
            "space", "sailing", "side-scroller", "superhero", "permadeath",
            "card", "battle-royale", "mmo", "mmofps", "mmotps",
            "3d", "2d", "anime", "fantasy", "sci-fi",
            "fighting", "action-rpg", "action", "military", "martial-arts",
            "flight", "low-spec", "tower-defense", "horror"
        ]
        platforms = [
            "pc", "browser", "all"
        ]

        base_url = "https://www.freetogame.com/api/games"

        # Handle specific game by ID
        if game_id is not None:
            url = f"https://www.freetogame.com/api/game?id={game_id}"
            r = requests.get(url)
            if r.status_code == 200:
                return r.json()["game_url"]
            else:
                return get_cat_err_img(r.status_code)

        # Build query parameters
        params = {}
        if category:
            if category not in categories:
                return ["Category not allowed", f"Allowed categories: {', '.join(categories)}"]
            params["category"] = category
        if platform:
            if platform not in platforms:
                return ["Platform not allowed", f"Allowed platforms: {', '.join(platforms)}"]
            params["platform"] = platform

        # Fetch games
        r = requests.get(base_url, params=params)
        if r.status_code != 200:
            return get_cat_err_img(r.status_code)

        data = r.json()
        game_urls = [game["game_url"] for game in data]

        if get_all:
            return game_urls
        if get_random:
            return choice(game_urls)
        return game_urls
    
    @staticmethod
    def get_qr(mode:str, qr_data:str):
        if mode == "create":
            url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={qr_data}"
            r = requests.get(url)
            if r.status_code == 200:
                return show_image(r.content)
            else:
                return get_cat_err_img(r.status_code)
        elif mode == "read":
            return "Read mode is not supported yet"
        else:
            return "Mode can be either create or read"
        
    @staticmethod
    def get_pokemon(name):
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        if name:
            r = requests.get(url)
        else:
            r = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")
        if r.status_code == 200:
            data = r.json()
            choice = cinput(f"Choose a key ({', '.join(data.keys())}): ")
            if choice != "cries" and choice != "sprites":
                if choice == "abilities":
                    result = [data[choice][index]["ability"]["name"] for index in range(len(data[choice]))]
                elif choice == "base_experience":
                    result = int(data["base_experience"])
                elif choice == "forms":
                    result = [data[choice][index]["name"] for index in range(len(data[choice]))]
                elif choice == "game_indecies" or choice == "location_area_encounters" or choice == "past_types":
                    result = f"{choice} is just too much data."
                elif choice == "height":
                    result = f"{data[choice]*10} cm"
                elif choice == "weight":
                    result = f"{data[choice]/10} kg"
                elif choice == "held_items":
                    result = [data[choice][index]["item"]["name"] for index in range(len(data[choice]))]
                elif choice == "id" or choice == "is_default" or choice == "name" or choice == "order":
                    result = data[choice]
                elif choice == "moves":
                    result = [data[choice][index]["move"]["name"] for index in range(len(data[choice]))]
                elif choice == "past_abilities":
                    result = []
                    for i in range(len(data[choice])):
                        for j in range(len(data[choice][i]["abilities"])):
                            result.append(data[choice][i]["abilities"][j]["ability"])
                elif choice == "species":
                    result = data[choice]["name"]
                else:
                    result = drill(data)
                return result
            elif choice == "cries":
                url = data[choice]["latest"]
                r = requests.get(url)
                if r.status_code == 200:
                    return play_audio(r.content)
                else:
                    return get_cat_err_img(r.status_code)
            elif choice == "sprites":
                sprite = cinput(f"Enter sprite ({", ".join(data[choice].keys())}: ")
                if sprite in ["other", "versions"]:
                    sprite2 = cinput(f"Enter sprite ({", ".join(data[choice][sprite].keys())}): ")
                    sprite3 = cinput(f"Enter sprite ({", ".join(data[choice][sprite][sprite2].keys())}): ")
                    url = data[choice][sprite][sprite2][sprite3]
                else:
                    url = data[choice][sprite]
                r = requests.get(url)
                if r.status_code == 200:
                    return show_image(r.content)
                else:
                    return get_cat_err_img(r.status_code)
        else:
            return get_cat_err_img(r.status_code)
        
    @staticmethod
    def get_advice():
        url = "https://api.adviceslip.com/advice"
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()["slip"]["advice"]

    @staticmethod
    def get_bored():
        url = "https://bored-api.appbrewery.com/random"
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()["activity"]
        
    @staticmethod
    def translate(text, source, target):
        # Example endpoint; you’d need a working public instance:
        url = "https://apertium.org/apy/translate"

        params = {
            "q": text,
            "langpair": f"{source}|{target}"
        }

        r = requests.get(url, params=params)

        if r.status_code == 200:
            data = r.json()
            translation = data["responseData"]["translatedText"]
            return translation
        else:
            return get_cat_err_img(r.status_code)
        
    @staticmethod
    def sudoku():
        # Example endpoint; you’d need a working public instance:
        url = "https://sudoku.freeapi.me/"
        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()
            r2 = requests.get(data["puzzle_url"])
            if r.status_code == 200:
                data = r2.content
                return show_image(data)
            else:
                return get_cat_err_img(r2.status_code)
        else:
            return get_cat_err_img(r.status_code)
    
def error():
    http_error_codes = [
        # 4xx Client Errors
        400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410,
        411, 412, 413, 414, 415, 416, 417, 418, 421, 422, 423,
        424, 425, 426, 428, 429, 431, 451,

        # 5xx Server Errors
        500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511
    ]
    return (get_cat_err_img(choice(http_error_codes)))

def ip():
    return APIS.get_ip()

def random_user():
    data = APIS.get_random_user()
    if isinstance(data, dict):
        return f"Gender: {data["Gender"]}\nName: {data["Name"]}\nDate of birth: {data["Date of birth"]}\nAge: {data["Age"]}\nLocation: {data["Location"]}"
    else:
        return data

def dog():
    return APIS.get_dog_img()

def fox():
    return APIS.get_fox_img()

def noise():
    print("Leave any value empty for default")
    rgb_input = cinput("RGB (e.g., 255,128,0) [default 255,255,255]: ")
    try:
        rgb = tuple(int(x) for x in rgb_input.split(",")) if rgb_input else (255, 255, 255)
    except:
        print("Invalid value. RGB set to 255,255,255")
        rgb = (255, 255, 255)

    nrtiles_input = cinput("Number of tiles (1-50) [default 50]: ")
    try:
        nrtiles = int(nrtiles_input) if nrtiles_input else 50
    except:
        print("Invalid value. Number of tiles set to 50")
        nrtiles = 50

    tileSize_input = cinput("Size of tiles in px (1-20) [default 7]: ")
    try:
        tileSize = int(tileSize_input) if tileSize_input else 7
    except:
        print("Invalid value. Tile size set to 7")
        tileSize = 7

    borderWidth_input = cinput("Borderwidth (0-15) [default 0]: ")
    try:
        borderWidth = int(borderWidth_input) if borderWidth_input else 0
    except:
        print("Invalid value. Border width set to 0")
        borderWidth = 0
    return (APIS.get_noise_img(rgb, nrtiles, tileSize, borderWidth))

def robot():
    return APIS.get_robot_img(cinput("Enter prompt: "))

def minecraft():
    skinblock = cinput("Skin or block: ")
    if skinblock == "skin":
        username = cinput("Enter username: ")
        skinpart = cinput("Enter part of skin: ")
        overlay = cinput("With overlay (y/n): ")
        overlay = overlay == "y"
        return (APIS.get_minecraft_skin(username, skinpart, overlay))
    elif skinblock == "block":
        block = cinput("Enter block: ")
        return (APIS.get_minecraft_block(block))

def f2p():
    option = cinput("Enter option (all (default), random, id, category, platform): ")
    option = option if option else "all"
    get_all = False
    get_random = False
    game_id = None
    category = ""
    platform = ""
    if option == "all" or option == "category" or option == "platform":
        if option == "all":
            get_all = True
        elif option == "category":
            category = cinput("Enter category (default shooter): ")
            category = category if category else "shooter"
        elif option == "platform":
            platform = cinput("Enter platform (default pc): ")
            platform = platform if platform else "pc"
        data = APIS.get_f2p_games(get_all=get_all, category=category, platform=platform)
        try:
            games = []
            for game in data:
                games.append(game)
            return games
        except:
            return data
    else:
        if option == "random":
            get_random = True
        elif option == "id":
            game_id = cinput("Enter game id (default 1): ")
            game_id = int(game_id) if game_id else 1
        return APIS.get_f2p_games(get_random=get_random, game_id=game_id)

def qr():
    return APIS.get_qr("create", cinput("Enter QR code data: "))

def pokemon():
    return APIS.get_pokemon(cinput("Enter Pokemon name (default Pikachu): "))

def advice():
    return APIS.get_advice()

def bored():
    return APIS.get_bored()

def translate():
    text = cinput("Enter text: ").lower()
    source = cinput("Enter source language: ").lower()
    target = cinput("Enter target language: ").lower()
    if target == "random":
        pass
    return (APIS.translate(text, source, target))

def sudoku():
    return APIS.sudoku()

apis = ["error", "ip", "random user", "dog", "fox", "noise", "robot", "minecraft", "f2p", "qr", "pokemon", "advice", "bored",\
        "translate", "sudoku"]

def main():
    api = cinput(f"\nChoose API ({", ".join(apis)}): ")

    if api == "quit" or api == "break":
        print("\n\033[0;32mThank you for using APIs by SayA\033[0m\n")
        return False

    elif api == "get ip" or api == "ip":
        print(ip())

    elif api == "random user":
        print(random_user())

    elif api == "dog":
        print(dog())

    elif api == "fox":
        print(fox())

    elif api == "noise":
        print(noise())

    elif api == "robot":
        print(robot())

    elif api == "minecraft":
        print(minecraft())

    elif api == "f2p":
        print(f2p())

    elif api == "qr":
        print(qr())

    elif api == "pokemon":
        print(pokemon())

    elif api == "advice":
        print(advice())

    elif api == "bored":
        print(bored())

    elif api == "translate":
        print(translate())

    elif api == "sudoku":
        print(sudoku())

    elif api == "error":
        print(error())

    else:
        print("Invalid API")

    return True

if __name__ == "__main__":
    while True:
        if not main():
            break
