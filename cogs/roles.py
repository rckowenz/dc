import discord
from discord.ext import commands
import asyncio 

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='role', invoke_without_command=True)
    async def role_group(self, ctx):
        await ctx.send("ssss")

    @role_group.command(name='create')
    @commands.has_permissions(manage_roles=True)
    async def role_create(self, ctx, *, name):
        try:
            name = name.replace('_', ' ')
            role = await ctx.guild.create_role(name=name)
            embed = discord.Embed(
                title=" ",
                description=f"{ctx.author.mention}: role <@&{role.id}> has been created.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title=" ",
                description=f"{ctx.author.mention}: i don't have permission to create roles.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Oppsie Dopsie :c Something went wrong! >_< An error occurred: {str(e)}")

    @role_group.command(name='edit')
    @commands.has_permissions(manage_roles=True)
    async def role_edit(self, ctx, role: discord.Role, *, name):
        try:
            name = name.replace('_', ' ')
            
            await role.edit(name=name)
            embed = discord.Embed(
                description=f"{ctx.author.mention}: changed <@&{role.id}> name to **{name}**.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Oopsie whoopsie ^_^ we made a fucky wucky Bingo Wingo :3333 Wawwww Wepowt! TypeError:{e} is not a function ~ Senpai chan >.<")
    @role_group.command(name='delete')
    @commands.has_permissions(manage_roles=True)
    async def role_delete(self, ctx, *, name):
        try:
            name = name.replace('_', ' ')
            role = discord.utils.get(ctx.guild.roles, name=name)

            if role is None:
                embed = discord.Embed(
                    title=" ",
                    description=f"{ctx.author.mention}: role **{name}** was not found.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            await role.delete()

            embed = discord.Embed(
                title=" ",
                description=f"{ctx.author.mention}: **{name}** has been deleted.",
                color=discord.Color.from_str("#ffffff")
            )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Opsie Dopsie :c Something went wrong! >_< An error occurred: {str(e)}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def r(self, ctx, member: discord.Member, *, name):
        try:
            name = name.replace('_', ' ')
            role = discord.utils.get(ctx.guild.roles, name=name)

            if role is None:
                embed = discord.Embed(
                    title=" ",
                    description=f"{ctx.author.mention}: role **{name}** was not found.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            if role in member.roles:
                await member.remove_roles(role)
                embed = discord.Embed(
                    title=" ",
                    description=f"{ctx.author.mention}: removed <@&{role.id}> from {member.mention}",
                    color=discord.Color.from_str("#ffffff")
                )
            else:
                await member.add_roles(role)
                embed = discord.Embed(
                    title=" ",
                    description=f"{ctx.author.mention}: gave {member.mention} <@&{role.id}>",
                    color=discord.Color.from_str("#ffffff")
                )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Oopsie whoopsie ^_^ we made a fucky wucky Bingo Wingo :3333 Wawwww Wepowt! TypeError:{e} is not a function ~ Senpai chan >.<")
            
    @role_group.command(name='list')
    @commands.has_permissions(manage_roles=True)
    async def roles_list(self, ctx):
        try:
            roles = [role for role in ctx.guild.roles if role.name != "@everyone"]
            role_mentions = [f"<@&{role.id}>" for role in roles]

            embed = discord.Embed(
                title=f"roles in {ctx.guild.name}",
                description="\n".join(role_mentions) if role_mentions else "no roles found.",
                color=discord.Color.from_str("#ffffff")
            )

            await ctx.send(f"{ctx.author.mention}", embed=embed)
        except Exception as e:
            await ctx.send(f"Oopsie whoopsie ^_^ we made a fucky wucky Bingo Wingo :3333 Wawwww Wepowt! TypeError:{e} is not a function ~ Senpai chan >.<")
    @role_group.command(name='color')
    @commands.has_permissions(manage_roles=True)
    async def role_color(self, ctx, name: str, color: str):
        try:
            name = name.replace('_', ' ')
            role = discord.utils.get(ctx.guild.roles, name=name)
            if role is None:
                embed = discord.Embed(
                    description=f"{ctx.author.mention}: role **{name}** not found.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            new_color = discord.Color(int(color.strip("#"), 16))
            await role.edit(color=new_color)
            embed = discord.Embed(
                description=f"{ctx.author.mention}: changed **{name}** role color to {color}.",
                color=new_color
            )
            await ctx.send(embed=embed)
        except ValueError:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: invalid color format. Use HEX format, e.g., #ff5733",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Oopsie whoopsie ^_^ we made a fucky wucky Bingo Wingo :3333 Wawwww Wepowt! TypeError:{e} is not a function ~ Senpai chan >.<")
            
    @role_group.command(name='removeall')
    @commands.has_permissions(manage_roles=True)
    async def remove_all_roles(self, ctx, *, name):
        try:
            name = name.replace('_', ' ')
            role = discord.utils.get(ctx.guild.roles, name=name)
            if role is None:
                embed = discord.Embed(
                    description=f"{ctx.author.mention}: role **{name}** not found.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            embed = discord.Embed(
                description=f"{ctx.author.mention}: Are you sure you want to remove <@&{role.id}> role from all members? (y/n)",
                color=discord.Color.from_str("#ffffff")
            )
            confirmation_message = await ctx.send(embed=embed)

            def check(msg):
                return msg.author == ctx.author and msg.content.lower() in ['yes', 'y']
            
            try:
                user_response = await self.bot.wait_for('message', timeout=30.0, check=check)
                if user_response:
                    for member in ctx.guild.members:
                        if role in member.roles:
                            await member.remove_roles(role)

                    success_embed = discord.Embed(
                        description=f"{ctx.author.mention}: removed <@&{role.id}> role from all members.",
                        color=discord.Color.from_str("#ffffff")
                    )
                    await ctx.send(embed=success_embed)

            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(
                    description=f"{ctx.author.mention}: I take that as a no..",
                    color=discord.Color.red()
                )
                await ctx.send(embed=timeout_embed)

        except Exception as e:
            await ctx.send(f"Oopsie whoopsie ^_^ we made a fucky wucky Bingo Wingo :3333 Wawwww Wepowt! TypeError:{e} is not a function ~ Senpai chan >.<")
async def setup(bot):
    await bot.add_cog(Roles(bot))