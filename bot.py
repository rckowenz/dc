import discord
import os
import json
import asyncio

from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

prefixes = {} 

def load_prefixes():
    global prefixes
    if os.path.exists("prefixes.json"):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
    else:
        prefixes = {}

def save_prefixes():
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

def get_server_prefix(bot, message):
    return prefixes.get(str(message.guild.id), ";") 

bot = commands.Bot(command_prefix=get_server_prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user}")
    print(f"{round(bot.latency * 1000)}ms") 
    change_status.start()

@tasks.loop(seconds=60)
async def change_status():
    await bot.change_presence(activity=discord.Streaming(name="@anticastle", url="https://www.youtube.com/watch?v=xlX7NwTq9Zo"))

@bot.event
async def on_guild_join(guild):
    global prefixes
    prefixes[str(guild.id)] = ";" 
    save_prefixes()

@bot.event
async def on_guild_remove(guild):
    global prefixes
    prefixes.pop(str(guild.id), None)
    save_prefixes()

@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, *, newprefix: str):
    try:
        global prefixes
        prefixes[str(ctx.guild.id)] = newprefix
        save_prefixes() 

        embed = discord.Embed(
            title=" ",
            description=f"{ctx.author.mention}: changed the prefix for **{ctx.guild.name}** to **{newprefix}**",
            color=discord.Color.from_str("#ffffff")
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title=" ",
            description=f"{ctx.author.mention}: Opsie Dopsie :c Fuckie Wuckie >_< An error occurred ownic~chan ^_^ ~ {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@setprefix.error
async def setprefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title=" ",
            description=f"{ctx.author.mention}: you don't have perms to use this command. you need **administrator** perms.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def resetprefix(ctx):
    try:
        global prefixes
        default_prefix = ";" 
        prefixes[str(ctx.guild.id)] = default_prefix 
        save_prefixes()

        embed = discord.Embed(
            title=" ",
            description=f"{ctx.author.mention}: the prefix for **{ctx.guild.name}** has been reset to **{default_prefix}**",
            color=discord.Color.from_str("#ffffff")
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title=" ",
            description=f"{ctx.author.mention}: Opsie Dopsie :c Fuckie Wuckie >_< An error occurred ownic~chan ^_^ ~ {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.check
async def globally_block_ignored_users(ctx):
    cog = bot.get_cog("owner")
    if cog and ctx.author.id in getattr(cog, "ignored_users", set()):
        return False
    return True

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(os.getenv("TOKEN")) 
        
asyncio.run(main())
