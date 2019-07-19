from discord.ext import commands
import discord
import yaml
from .db import DataBase
from .embed import em

import os
from starbotutils import default_exts_names, raw_default_exts, p


class StarContext(commands.Context):
    """Context extention so we can add more stuff"""
    async def em(self, *args, **kwargs):
        return await self.send(**em(*args, **kwargs))

class StarHelp(commands.HelpCommand):
    """Help extention so we can have a better help command."""
    def __init__(self, **options):
        super().__init__(verify_checks=True, **options)

    def get_command_signature(self, command):
        return f"**{self.clean_prefix}{command.qualified_name} {command.signature}**\n"

    async def send_command_help(self, command):

        embed = em(command.description, command.name, type="info")["embed"]
        embed = discord.Embed(title=command.name, description=command.description, color=discord.Color.green())
        if len(command.aliases) > 0:
            embed.add_field(name="Aliases", value=', '.join(command.aliases))
        embed.add_field(name="Usage", value=self.get_command_signature(command))
        await self.context.send(embed=embed)

    async def send_bot_help(self, mapping):
        embed = em("A list of all commands", "Help", type="info")["embed"]
        for cog, cog_commands in mapping.items():
            if not cog:
                category = "No category"
            else:
                category = getattr(cog, 'qualified_name')
            command_signatures = '\n'.join([f"{self.get_command_signature(c)}{c.description}\n"  for c in cog_commands])
            if not command_signatures:
                continue

            embed.add_field(name=category, value=command_signatures, inline=False)

        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = em("Help for this Group", f"Help {group.qualified_name}", type="info")["embed"]
        for command in group.commands:
            embed.add_field(name=command.qualified_name, value=f"{self.get_command_signature(command)}{command.description}\n")

        await self.context.send(embed=embed)

class StarBot(commands.Bot):
    def __init__(self, command_prefix, **kwargs):
        self.config_file = kwargs.get("config_file", "config.yml")
        with open(self.config_file, 'r') as stream:
            self.config = yaml.safe_load(stream)
        self.db = DataBase()
        self.context = kwargs.get("context", StarContext)
        super().__init__(command_prefix, **kwargs)

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=self.context)
    
    """Helps (re/un)loading extentions"""

    def load_all(self):
        for cog in os.listdir("exts"):
            if cog.endswith(".py"):
                try:
                    self.load_extension(f"exts.{cog.replace(cog[-3:],'')}")
                    print(f"Loaded Cog {cog}")
                except Exception as e:
                    raise e
        for cog in default_exts_names:
            try:
                self.load_extension(cog)
                print(f"Loaded Cog {cog}")
            except Exception as e:
                raise e          


    def load(self, ext):
        if ext in os.listdir("exts"):
            try:
                self.load_extension(f"exts.{ext}")
                print(f"Loaded Cog {ext}")
            except Exception as e:
                raise e
        elif ext in raw_default_exts:
            try:
                self.load_extension(p+ext)
                print(f"Loaded Cog {ext}")
            except Exception as e:
                raise e
        else:
            try:
                self.load_extension(ext)
                print(f"Loaded Cog {ext}")
            except Exception as e:
                raise e

    def unload_all(self):
        for cog in os.listdir("exts"):
            if cog.endswith(".py"):
                try:
                    self.unload_extension(f"exts.{cog.replace(cog[-3:],'')}")
                    print(f"Unloaded Cog {cog}")
                except Exception as e:
                    raise e
        for cog in default_exts_names:
            try:
                self.unload_extension(cog)
                print(f"Unloaded Cog {cog}")
            except Exception as e:
                raise e          


    def unload(self, ext):
        if ext in os.listdir("exts"):
            try:
                self.unload_extension(f"exts.{ext}")
                print(f"Unloaded Cog {ext}")
            except Exception as e:
                raise e
        elif ext in raw_default_exts:
            try:
                self.unload_extension(p+ext)
                print(f"Unloaded Cog {ext}")
            except Exception as e:
                raise e
        else:
            try:
                self.unload_extension(ext)
                print(f"Unloaded Cog {ext}")
            except Exception as e:
                raise e


    def reload_all(self):
        for cog in os.listdir("exts"):
            if cog.endswith(".py"):
                try:
                    self.reload_extension(f"exts.{cog.replace(cog[-3:],'')}")
                    print(f"Reloaded Cog {cog}")
                except Exception as e:
                    raise e
        for cog in default_exts_names:
            try:
                self.reload_extension(cog)
                print(f"Reloaded Cog {cog}")
            except Exception as e:
                raise e          


    def reload(self, ext):
        if ext in os.listdir("exts"):
            try:
                self.reload_extension(f"exts.{ext}")
                print(f"Reloaded Cog {ext}")
            except Exception as e:
                raise e
        elif ext in raw_default_exts:
            try:
                self.reload_extension(p+ext)
                print(f"Reloaded Cog {ext}")
            except Exception as e:
                raise e
        else:
            try:
                self.reload_extension(ext)
                print(f"Reloaded Cog {ext}")
            except Exception as e:
                raise e