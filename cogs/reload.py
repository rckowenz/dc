import discord

from discord.ext import commands

OWNER_IDS = ["475046192179445780", "255718877730832387", "1226427078560317542"]

class reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx, *, cog: str):
        try:
            if str(ctx.author.id) in OWNER_IDS:
                await self.bot.unload_extension(f"cogs.{cog}")
                await self.bot.load_extension(f"cogs.{cog}")
                await ctx.send(f"master i rwloaded: {cog} :3")
            else:
                await ctx.send("...")
        except Exception as e:
            await ctx.send(f"Oopsie whoopsie ^_^ we made a fucky wucky Bingo Wingo :3333 Wawwww Wepowt! TypeError:{e} is not a function ~ Senpai chan >.<")


async def setup(bot):
    await bot.add_cog(reload(bot))