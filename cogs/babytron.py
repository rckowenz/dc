import discord
import os
import random


from discord.ext import commands


class babytron(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def babytron(self, ctx):
        allowed_ids = [1226427078560317542]
        if ctx.author.id in allowed_ids:
            responses = [
                "Triceps in my glasses, you would think it’s roids im off. — Out on bond",
                "King of the galaxy like come on, time to crown the Don. — Out on bond",
                "Point it at his toes turn his Yeezy’s into Foam Runners. — Paul bearer",
                "Undertaker, I don’t wrestle, I’m with Paul Bearer. — Paul bearer",
                "Finna use the CPN, bitch, I’m a credit booster. — 007",
                "Bougie bitch with me smoking za out a rose petal. — 007",
                "I’ma creep up on him with the stick, 007. — 007",
                "Three-five of, uh, I can’t say it, shit, I’m out of breath. — 007",
                "Trynna keep up with babytron? Yea keep trying. — 007",
                "Working magic with these Visa’s, Would’ve thought I cast a spell. — Half-Blood Prince",
                "Alright here bro hold the torch. — Half-Blood Prince",
                "Slytherin, the Sorting Hat sense the snake in your blood — Half-Blood Prince",
                "Spanish clerk and she cold hit her with the “Por Favor”. — Por Favor",
                "Fourty thousand on me, Finna get a Four-for-Four. — Por Favor",
                "Acting tough you get stomped out. — Just In Case",
                "Uh, hi, we need help, sir. BabyTron came to the ball with the fire BINs and left it scorching. We need you to send the fire department. ASAP, please. Please! — Human torch",
            ]
            await ctx.send(f"{random.choice(responses)}")

async def setup(bot):
    await bot.add_cog(babytron(bot))
