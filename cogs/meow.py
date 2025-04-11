import discord
import os
import random


from discord.ext import commands

OWNER_IDS = ["1226427078560317542" '255718877730832387']

class meow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ignored_users = set()

    @commands.command()
    async def meow(self, ctx):
        await ctx.send("meow")
    
    @commands.command(aliases=["owners"])
    async def owner(self, ctx):
        owners_mentions = [f"<@{owner_id}>" for owner_id in OWNER_IDS]
        await ctx.send(f"my owners are {', '.join(owners_mentions)} >_<")
    
    @commands.command()
    async def hi(self, ctx):
        if str(ctx.author.id) in OWNER_IDS:
            await ctx.send(f"hi master chan, {ctx.author.mention} >_<")
        else:
            await ctx.send("you are not my master >:c")

    @commands.command()
    async def charlie(self, ctx):
        folder_path = os.path.join(os.path.dirname(__file__), '..', 'dog')
        images = os.listdir(folder_path)
        if images:
            selected_image = random.choice(images)
            file = discord.File(os.path.join(folder_path, selected_image))
            await ctx.send(file=file)
        else:
            await ctx.send("meow")




    @commands.command()
    async def credits(self, ctx):

        embed = discord.Embed(title="credits", description="**[@anticastle](https://discord.com/users/1226427078560317542)**: **creator & dev**", color=0xFFFFFF)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1353819818926538841/1356657334826569938/f92b4563efe522919c02f1327e77d0f0.png?ex=67ed5d1a&is=67ec0b9a&hm=8740d23d5df3f149266fa658deed4f628be480f82a1494c7044d85cafabfb58e&")

        await ctx.send(embed=embed)


    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"{round(self.bot.latency * 1000)}ms")

    @commands.command(aliases=["inv"])
    async def invite(self, ctx):
        await ctx.send("https://discord.com/oauth2/authorize?client_id=1233617350922731642")    

    @commands.command(aliases=['setbotpfp', 'setavatar'])
    async def botpfp(self, ctx): 
        allowed_ids = [475046192179445780, 1226427078560317542]


        if ctx.author.id in allowed_ids:
            if len(ctx.message.attachments) == 0:
                await ctx.send("please upload an image file.")
                return


            attachment = ctx.message.attachments[0]


            if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                await ctx.send("please upload a valid image file (PNG, JPG, JPEG, GIF).")
                return


            try:
                await attachment.save(attachment.filename)


                with open(attachment.filename, 'rb') as file:
                    avatar_bytes = file.read()


                await self.bot.user.edit(avatar=avatar_bytes)


                os.remove(attachment.filename)


                await ctx.send("avatar updated.")
            except Exception as e:
                await ctx.send(f"Oopsie whoopsie ^_^ we made a fucky wucky Bingo Wingo :3333 Wawwww Wepowt! TypeError:{e} is not a function ~ Senpai chan >.<")

    @commands.command()
    async def kys(self, ctx):
        await ctx.send("-_-")

    @commands.command()
    async def close(self, ctx):
        if str(ctx.author.id) in OWNER_IDS:
            await ctx.send(":c")
            await self.bot.close()
        else:
            await ctx.send("erm")

async def setup(bot):
    await bot.add_cog(meow(bot))