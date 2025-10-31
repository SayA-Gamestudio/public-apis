import requests
from io import BytesIO
try:
    from PIL import Image
except:
    print("-"*10+"Install PIL using 'pip install pillow'"+"-"*10)

def show_image(content):
    img = Image.open(BytesIO(content))
    img.show()

def get_cat_err_img(errcode):
    url = f"https://http.cat/{errcode}"
    r = requests.get(url)
    if r.status_code == 200:
        show_image(r.content)

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
    
def minecraft():
    username = input("Enter username: ")
    skinpart = input("Enter part of skin: ")
    print(get_minecraft_skin(username, skinpart))

def main():
    while True:
        minecraft()

main()