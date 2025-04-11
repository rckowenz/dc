import json
import os
import discord

from discord.ext import commands

OWNER_IDS = ["1226427078560317542", '255718877730832387']


class owner(commands.Cog):
    
    def load_ignored_users(self):
        if not os.path.exists("ignored_users.json"):
            return set()
        with open("ignored_users.json", "r") as f:
            return set(json.load(f))

    def save_ignored_users(self):
        with open("ignored_users.json", "w") as f:
            json.dump(list(self.ignored_users), f)

    def __init__(self, bot):
        self.bot = bot
        self.ignored_users = self.load_ignored_users()

    @commands.command()
    async def ignore(self, ctx, member: discord.Member):
        if str(ctx.author.id) in OWNER_IDS:
            self.ignored_users.add(member.id)
            self.save_ignored_users()
            await ctx.send(f"ignorwng {member.display_name} >:c")

    @commands.command()
    async def unignore(self, ctx, member: discord.Member):
        if str(ctx.author.id) in OWNER_IDS:
            if member.id in self.ignored_users:
                self.ignored_users.remove(member.id)
                self.save_ignored_users()
                await ctx.send(f"oki :3 .")
            else:
                await ctx.send(f"{member.display_name} isn't being ignored")


async def setup(bot):
    await bot.add_cog(owner(bot))

