import discord
import random
#icons from https://flaticon.com/ we dont own these

formating = {
    None : ("", "{d}", 0xffffff, None),
    "done": (random.choice(["Done!", "Finished!", "Completed!"]), "{d}", 0x00ff00, "https://i.imgur.com/78vuV0Q.png"),
    "error": ("Error", "{d}\n\n**Please join our [support](https://discord.gg/BRtS3CJ) server for help!**", 0xff0000, "https://i.imgur.com/boHCCTy.png"),
    "unknown": ("Error", "An unknown error has occured ```{d}```\n\n**Please join our [support](https://discord.gg/BRtS3CJ) server for help!**", 0xff0000, "https://i.imgur.com/boHCCTy.png"),
    "info" : ("Info", "{d}", 0x52e0ff, "https://i.imgur.com/NKkqwUR.png")
}


def em(description, title=None, type=None, **kwargs):
    t, desc, colour, icon = formating.get(type) or formating.get(None)
    title = title or t
    colour = kwargs.get("colour", colour)
    icon = kwargs.get("icon", icon)
    thumbnail = kwargs.get("image", None)
    description = desc.format(d=description)
    if icon == "null":
        icon = None
    if thumbnail is None:
        if not icon is None:
            embed=discord.Embed(description=description, colour=colour).set_author(name=title, icon_url=icon)
        else:
            embed=discord.Embed(description=description, colour=colour).set_author(name=title)
    else:
        if not icon is None:
            embed=discord.Embed(description=description, colour=colour).set_author(name=title, icon_url=icon).set_thumbnail(url=thumbnail)
        else:
            embed=discord.Embed(description=description, colour=colour).set_author(name=title).set_thumbnail(url=thumbnail)
    
    for field in kwargs.get("fields", []):
        embed.add_field(name=field["name"], value=field["value"])
    
    return {"embed" : embed}
