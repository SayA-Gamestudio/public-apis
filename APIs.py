import requests
from random import choice
from PIL import Image
from io import BytesIO

def show_image(content):
    img = Image.open(BytesIO(content))
    img.show()

def get_cat_err_img(errcode):
    url = f"https://http.cat/{errcode}"
    r = requests.get(url)
    if r.status_code == 200:
        show_image(r.content)

apis = ["error", "ip", "random user", "dog", "fox", "noise", "robot", "minecraft", "f2p"]

class APIS():
    @staticmethod
    def test():
        url = f""
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            return (f"Data: {data}")
        else:
            get_cat_err_img(r.status_code)
            return r.status_code

    @staticmethod
    def get_ip():
        """
        Returns current IP address
        """
        url = "https://api.ipify.org?format=json"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            return (f"Your IP address is {data["ip"]}")
        else:
            get_cat_err_img(r.status_code)
            return r.status_code

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
            get_cat_err_img(r.status_code)
            return r.status_code
    
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
            get_cat_err_img(r.status_code)
            return r.status_code
        
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
            get_cat_err_img(r.status_code)
            return r.status_code
        
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
            get_cat_err_img(r.status_code)
            return r.status_code
        
    @staticmethod
    def get_robot_img(prompt):
        url = f"https://robohash.org/{prompt}"
        r = requests.get(url)

        if r.status_code == 200:
            return show_image(r.content)
        else:
            get_cat_err_img(r.status_code)
            return r.status_code
        
    @staticmethod
    def get_amiibo_data(name):
        url = f"https://www.amiiboapi.com/api/amiibo/?name={name}"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            return (f"Returned data: {data["amiibo"][0]}")
        else:
            get_cat_err_img(r.status_code)
            return r.status_code
        
    @staticmethod
    def get_minecraft_skin(username, skinpart):
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
                get_cat_err_img(r.status_code)
                return r.status_code

            if skinpart == "head":
                crafatar_url = f"https://crafatar.com/avatars/{uuid}"
            elif skinpart == "head3d":
                crafatar_url = f"https://crafatar.com/renders/head/{uuid}"
            elif skinpart == "body3d":
                crafatar_url = f"https://crafatar.com/renders/body/{uuid}"
            elif skinpart == "body":
                crafatar_url = f"https://crafatar.com/skins/{uuid}"
            r = requests.get(crafatar_url)
            if r.status_code == 200:
                return show_image(r.content)
            else:
                get_cat_err_img(r.status_code)
                return r.status_code
        else:
            return f"Skin parts: {', '.join(skinparts)}"
    
    @staticmethod
    def get_f2p_games(get_all: bool = False, get_random: bool = False, game_id: int = None, category: str = "", platform: str = ""):
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
                get_cat_err_img(r.status_code)
                return r.status_code

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
            get_cat_err_img(r.status_code)
            return r.status_code

        data = r.json()
        game_urls = [game["game_url"] for game in data]

        if get_all:
            return game_urls
        if get_random:
            return choice(game_urls)
        return game_urls

def main():
    while True:
        api = input(f"\nChoose API ({", ".join(apis)}): ").lower().strip()

        if api == "quit":
            break

        if api == "test":
            print(APIS.test())

        elif api == "get ip" or api == "ip":
            print(APIS.get_ip())

        elif api == "random user":
            data = APIS.get_random_user()
            print(data["Gender"])
            print(data["Name"])
            print(data["Date of birth"])
            print(data["Age"])
            print(data["Location"])

        elif api == "dog":
            print(APIS.get_dog_img())

        elif api == "fox":
            print(APIS.get_fox_img())

        elif api == "noise":
            print("Leave any value empty for default")
            rgb_input = input("RGB (e.g., 255,128,0) [default 255,255,255]: ").strip()
            rgb = tuple(int(x) for x in rgb_input.split(",")) if rgb_input else (255, 255, 255)

            nrtiles_input = input("Number of tiles (1-50) [default 50]: ").strip()
            nrtiles = int(nrtiles_input) if nrtiles_input else 50

            tileSize_input = input("Size of tiles in px (1-20) [default 7]: ").strip()
            tileSize = int(tileSize_input) if tileSize_input else 7

            borderWidth_input = input("Borderwidth (0-15) [default 0]: ").strip()
            borderWidth = int(borderWidth_input) if borderWidth_input else 0
            print(APIS.get_noise_img(rgb, nrtiles, tileSize, borderWidth))

        elif api == "robot":
            print(APIS.get_robot_img(input("Enter prompt: ")))

        elif api == "amiibo":
            print(APIS.get_amiibo_data(input("Enter Amiibo name: ")))

        elif api == "minecraft":
            username = input("Enter username: ")
            skinpart = input("Enter part of skin: ")
            print(APIS.get_minecraft_skin(username, skinpart))

        elif api == "f2p":
            option = input("Enter option (all (default), random, game_id, category, platform): ").strip()
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
                    category = input("Enter category (default shooter): ")
                    category = category if category else "shooter"
                elif option == "platform":
                    platform = input("Enter platform (default pc): ")
                    platform = platform if platform else "pc"
                data = APIS.get_f2p_games(get_all=get_all, category=category, platform=platform)
                try:
                    for game in data:
                        print(game)
                except:
                    print(data)
            else:
                if option == "random":
                    get_random = True
                elif option == "game_id":
                    game_id = int(input("Enter game id (default 1): "))
                    game_id = game_id if game_id else 1
                print(APIS.get_f2p_games(get_random=get_random, game_id=game_id))

        elif api == "error":
            http_error_codes = [
                # 4xx Client Errors
                400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410,
                411, 412, 413, 414, 415, 416, 417, 418, 421, 422, 423,
                424, 425, 426, 428, 429, 431, 451,

                # 5xx Server Errors
                500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511
            ]
            get_cat_err_img(str(choice(http_error_codes)))
            break

        else:
            print("Invalid API")

main()