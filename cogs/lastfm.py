import discord
import requests
import json
import os
import asyncio
import random
import requests
import re

from datetime import datetime
from discord.ext import commands

API_KEY = "da70c3416fe974b1846594be6a15d56c"
SHARED_SECRET = "c5efc281242cba4f913d93e2b5ac1578"

DATA_FILE = "users.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        user_data = json.load(f)
else:
    user_data = {}

class lastfm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#############################################################################################################################################################


    @commands.group(name='lf', invoke_without_command=True)
    async def lf(self, ctx, username: str):
        embed= discord.Embed(
            title=" ",
            description=f"{ctx.author.mention}: you currently don't have an account connected. try ;connect <uysername>, then try a command again.",
            color=discord.Color.from_str("#ffffff"),
        )
        await ctx.send(embed=embed)


#############################################################################################################################################################


    @commands.command(aliases=['con', 'login'])
    async def connect(self, ctx, username: str):
        user_data[str(ctx.author.id)] = username

        with open(DATA_FILE, "w") as f:
            json.dump(user_data, f, indent=4)

        embed = discord.Embed(
            title=" ",
            description=f"{ctx.author.mention}: connected Last.fm to the user **{username}**",
            color=discord.Color.from_str("#ffffff"),
        )
        await ctx.send(embed=embed)

#############################################################################################################################################################

    @commands.command(aliases=['discon', 'logout'])
    async def disconnect(self, ctx):
        user_id = str(ctx.author.id)

        if user_id not in user_data:
            embed = discord.Embed(
                title=" ",
                description=f"{ctx.author.mention}: you don't have an account connected.",
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)
            return

        del user_data[user_id]

        with open(DATA_FILE, "w") as f:
            json.dump(user_data, f, indent=4)

        embed = discord.Embed(
            title=" ",
            description=f"{ctx.author.mention}: disconnected your Last.fm account.",
            color=discord.Color.from_str("#ffffff"),
        )
        await ctx.send(embed=embed)

#############################################################################################################################################################

    @lf.command(name='recent', aliases=['recenttracks'], invoke_without_command=True)
    async def recent(self, ctx):
        user_id = str(ctx.author.id)
        
        if user_id not in user_data:

            embed = discord.Embed(
                title=" ",
                description=f"{ctx.author.mention}: you don't have an account connected. try ;connect <username>, then try the command again.",
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)
            return

        username = user_data[user_id]

        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "user.getrecenttracks",
            "user": username,
            "api_key": API_KEY,
            "format": "json",
            "limit": 5
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "recenttracks" not in data:
            await ctx.send("could not retrieve data. make sure your Last.fm username is correct.")
            return

        tracks = data["recenttracks"]["track"]
        track_list = [f"🎵  **{t['artist']['#text']}** - *{t['name']}*" for t in tracks]

        embed = discord.Embed(title=f"{username}'s recent tracks", description="\n".join(track_list), color=discord.Color.from_str("#ffffff"))
        await ctx.send(embed=embed)

#############################################################################################################################################################


    @commands.command(aliases=['np', 'fm'])
    async def nowplaying(self, ctx):
        user_id = str(ctx.author.id)

        if user_id not in user_data:
            embed = discord.Embed(
                title=" ",
                description=f"{ctx.author.mention}: you don't have an account connected. try ;connect <username>, then try the command again.",
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)
            return

        username = user_data[user_id]
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "user.getrecenttracks",
            "user": username,
            "api_key": API_KEY,
            "format": "json",
            "limit": 1
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if "recenttracks" not in data or "track" not in data["recenttracks"]:
                embed = discord.Embed(
                    title=" ",
                    description=f"{ctx.author.mention}: could not retrieve data. make sure your Last.fm username is correct.",
                    color=discord.Color.from_str("#ffffff"),
                )
                await ctx.send(embed=embed)
                return

            tracks = data["recenttracks"]["track"]

            if len(tracks) == 0:
                await ctx.send(f"{username} is not listening to anything right now.")
                return

            track = tracks[0]
            image_url = track['image'][-1]['#text'] if track['image'] else None

            is_now_playing = "@attr" in track and "nowplaying" in track["@attr"]

            embed_color = discord.Color.from_str("#ffffff") if is_now_playing else discord.Color.from_str("#ffffff")
            embed_description = f"**[{track['name']}]({track['url']})**\n**{track['artist']['#text']}** | *{track['album']['#text']}*"

            embed = discord.Embed(
                description=embed_description,
                color=embed_color,
            )

            if image_url:
                user_info_url = "http://ws.audioscrobbler.com/2.0/"
                user_params = {
                    "method": "user.getinfo",
                    "user": username,
                    "api_key": API_KEY,
                    "format": "json"
                }
                user_response = requests.get(user_info_url, params=user_params).json()

                total_scrobbles = user_response.get("user", {}).get("playcount", "N/A")

                embed.set_thumbnail(url=image_url)
                embed.set_author(
                    name=f"now playing | {username}",
                    icon_url=ctx.author.avatar.url
                )
                embed.set_footer(text=f"{total_scrobbles} scrobbles")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Oopsie whoopsie ^_^ we made a fucky wucky Bingo Wingo :3333 Wawwww Wepowt! TypeError:{e} is not a function ~ Senpai chan >.<")


#############################################################################################################################################################

    @commands.command(aliases=['s'])
    async def spotify(self, ctx):
        try:
            member = ctx.author

            for activity in member.activities:
                if isinstance(activity, discord.Spotify):
                    track_url = f"https://open.spotify.com/track/{activity.track_id}"
                    await ctx.send(f"{track_url}")
                    return

            await ctx.send("You're not listening to Spotify right now, owo~")

        except Exception as e:
            await ctx.send(f"Oopsie whoopsie ^_^ we made a fucky wucky Bingo Wingo :3333 Wawwww Wepowt! `{type(e).__name__}: {e}` ~ Senpai chan >.<")

#############################################################################################################################################################


    @commands.command(aliases=['itunes, tidal, youtube, applemusic, sc'])
    async def soundcloud(self, ctx):
        await ctx.send("these sources have not been set up yet.. give some time and it would be added to the bot :3!")


#############################################################################################################################################################

    @lf.command(name="lyrics", invoke_without_command=True)
    async def lyrics(self, ctx):
        user_id = str(ctx.author.id)

        if user_id not in user_data:
            embed = discord.Embed(
                title=" ",
                description=f"{ctx.author.mention}: you don't have an account connected. try ;connect <username>, then try the command again.",
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)
            return

        username = user_data[user_id]

        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "user.getrecenttracks",
            "user": username,
            "api_key": API_KEY,
            "format": "json",
            "limit": 1
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            track = data["recenttracks"]["track"][0]
            title = track["name"]
            artist = track["artist"]["#text"]

            lyrics_url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
            lyrics_response = requests.get(lyrics_url)
            lyrics_response.raise_for_status()
            lyrics_data = lyrics_response.json()

            if 'lyrics' in lyrics_data and lyrics_data['lyrics'].strip():
                lyrics = lyrics_data['lyrics']
                for chunk in [lyrics[i:i+2000] for i in range(0, len(lyrics), 2000)]:
                    embed = discord.Embed(
                        title=f"{title} by {artist}",
                        description=chunk,
                        color=discord.Color.from_str("#ffffff"),
                    )
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=" ",
                    description=f"could not find any lyrics for.. **{title} by {artist}**.",
                    color=discord.Color.from_str("#ffffff"),
                )
                await ctx.send(embed=embed)


        except Exception as e:
            error_message = f"{ctx.author.mention}: could not find lyrics for"
            if title and artist:
                error_message += f" **{title} by {artist}**"

            embed = discord.Embed(
                title=" ",
                description=error_message,
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)

#############################################################################################################################################################


    @lf.command(aliases=["wkt"])
    async def whoknowstrack(self, ctx):
        user_id = str(ctx.author.id)

        if user_id not in user_data:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: you don't have an account connected. try ;connect <username>, then try the command again.",
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)
            return        

        username = user_data[user_id]
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "user.getrecenttracks",
            "user": username,
            "api_key": API_KEY,
            "format": "json",
            "limit": 1
        }

        response = requests.get(url, params=params)
        data = response.json()
        track = data.get("recenttracks", {}).get("track", [])[0]

        if not track:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: no track found.. try again",
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)
            return

        track_name = track['name']
        artist_name = track['artist']['#text']
        
        known_users = []

        for uid, uname in user_data.items():
            track_info_url = "http://ws.audioscrobbler.com/2.0/"
            track_params = {
                "method": "track.getinfo",
                "user": uname,
                "api_key": API_KEY,
                "artist": artist_name,
                "track": track_name,
                "format": "json"
            }

            track_info = requests.get(track_info_url, params=track_params).json()
            user_playcount = track_info.get("track", {}).get("userplaycount", 0)

            if user_playcount and int(user_playcount) > 0:
                try:
                    member = await ctx.guild.fetch_member(int(uid))
                    known_users.append((member.display_name, user_playcount, uname))
                except:
                    continue

        if not known_users:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: no one in this server has listened to *{track_name}* by **{artist_name}**",
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)
            return

        known_users.sort(key=lambda x: int(x[1]), reverse=True)

        description = "\n".join([
            f"{i+1}. **[{name}](https://www.last.fm/user/{uname})** - **{count}** plays"
            for i, (name, count, uname) in enumerate(known_users)
        ])

        embed = discord.Embed(
            title=f"{track_name} by {artist_name} in {ctx.guild.name}",
            url=f"https://www.last.fm/music/{artist_name.replace(' ', '+')}/{track_name.replace(' ', '+')}",
            description=description,
            color=discord.Color.from_str("#ffffff")
        )

        album_image = None
        if "image" in track and track["image"]:
            album_image = track["image"][-1].get("#text")
        if album_image:
            embed.set_thumbnail(url=album_image)

        await ctx.send(embed=embed)

#############################################################################################################################################################


    @lf.command(aliases=["gwkt"], invoke_without_command=True)
    async def globalwhoknowstrack(self, ctx):
        user_id = str(ctx.author.id)

        if user_id not in user_data:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: you don't have an account connected. try `;connect <username>`, then try again.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        username = user_data[user_id]
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "user.getrecenttracks",
            "user": username,
            "api_key": API_KEY,
            "format": "json",
            "limit": 1
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
        except requests.exceptions.RequestException as e:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: there was an error fetching track data. please try again later.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        track = data.get("recenttracks", {}).get("track", [])[0]

        if not track:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: no track found. try again later.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        track_name = track['name']
        artist_name = track['artist']['#text']
        album_art = track['image'][-1]['#text'] if "image" in track and track["image"] else None

        known_users = []

        for uid, uname in user_data.items():
            track_info_url = "http://ws.audioscrobbler.com/2.0/"
            track_params = {
                "method": "track.getinfo",
                "user": uname,
                "api_key": API_KEY,
                "artist": artist_name,
                "track": track_name,
                "format": "json"
            }

            try:
                track_info = requests.get(track_info_url, params=track_params).json()
                user_playcount = track_info.get("track", {}).get("userplaycount", 0)
            except Exception as e:
                print(f"Error fetching track info for {uname}: {e}")
                continue

            if user_playcount and int(user_playcount) > 0:
                try:
                    member = await ctx.bot.fetch_user(int(uid))
                    known_users.append((member.display_name, user_playcount, uname))
                except discord.NotFound:
                    pass 

        if not known_users:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: no one has listened to **{track_name}** by **{artist_name}**.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        known_users.sort(key=lambda x: int(x[1]), reverse=True)

        description = "\n".join([
            f"{i+1}. **[{name}](https://www.last.fm/user/{uname})** - **{count}** plays"
            for i, (name, count, uname) in enumerate(known_users)
        ])

        embed = discord.Embed(
            title=f"{track_name} by {artist_name} globally",
            url=f"https://www.last.fm/music/{artist_name.replace(' ', '+')}/{track_name.replace(' ', '+')}",
            description=description,
            color=discord.Color.from_str("#ffffff")
        )

        if album_art:
            embed.set_thumbnail(url=album_art)

        await ctx.send(embed=embed)


#############################################################################################################################################################

    @commands.command()
    async def no(self, ctx):
        await ctx.send("yes")

#############################################################################################################################################################

    @lf.command(name='wka', aliases=['whoknowsalbum'])
    async def wka(self, ctx):
        user_id = str(ctx.author.id)

        if user_id not in user_data:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: you don't have an account connected. try `;connect <username>`, then try again.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        username = user_data[user_id]
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "user.getrecenttracks",
            "user": username,
            "api_key": API_KEY,
            "format": "json",
            "limit": 1
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
        except requests.exceptions.RequestException:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: there was an error fetching album data. please try again later.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        tracks = data.get("recenttracks", {}).get("track", [])
        if not tracks:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: no recent track found. try again later.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        track = tracks[0]
        album_name = track.get('album', {}).get('#text', 'Unknown Album')
        artist_name = track.get('artist', {}).get('#text', 'Unknown Artist')

        album_art = (
            track.get('image', [{}])[-1].get('#text')
            if track.get('image') else None
        )

        known_users = []

        for member in ctx.guild.members:
            uid = str(member.id)
            if uid not in user_data:
                continue

            uname = user_data[uid]

            album_info_url = "http://ws.audioscrobbler.com/2.0/"
            album_params = {
                "method": "album.getinfo",
                "user": uname,
                "api_key": API_KEY,
                "artist": artist_name,
                "album": album_name,
                "format": "json"
            }

            try:
                album_info = requests.get(album_info_url, params=album_params).json()
                user_playcount = album_info.get("album", {}).get("userplaycount", 0)
            except Exception as e:
                print(f"error fetching album info for {uname}: {e}")
                continue

            if user_playcount and int(user_playcount) > 0:
                known_users.append((member.display_name, user_playcount, uname))

        if not known_users:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: no one in this server has listened to **{album_name}** by **{artist_name}**.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        known_users.sort(key=lambda x: int(x[1]), reverse=True)

        description = "\n".join([
            f"{i+1}. **[{name}](https://www.last.fm/user/{uname})** - **{count}** plays"
            for i, (name, count, uname) in enumerate(known_users)
        ])

        embed = discord.Embed(
            title=f"{album_name} by {artist_name} in {ctx.guild.name}",
            url=f"https://www.last.fm/music/{artist_name.replace(' ', '+')}/{album_name.replace(' ', '+')}",
            description=description,
            color=discord.Color.from_str("#ffffff")
        )

        if album_art:
            embed.set_thumbnail(url=album_art)

        await ctx.send(embed=embed)


#############################################################################################################################################################

    @lf.command(name='gwka', aliases=['globalwhoknowsalbum'])
    async def gwka(self, ctx):
        user_id = str(ctx.author.id)

        if user_id not in user_data:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: you don't have an account connected. try `;connect <username>`, then try again.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        username = user_data[user_id]
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "user.getrecenttracks",
            "user": username,
            "api_key": API_KEY,
            "format": "json",
            "limit": 1
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
        except requests.exceptions.RequestException as e:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: there was an error fetching album data. please try again later.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        tracks = data.get("recenttracks", {}).get("track", [])
        if not tracks:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: no recent track found. try again later.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        track = tracks[0]
        album_name = track.get('album', {}).get('#text', 'Unknown Album')
        artist_name = track.get('artist', {}).get('#text', 'Unknown Artist')

        album_art = (
            track.get('image', [{}])[-1].get('#text')
            if track.get('image') else None
        )

        known_users = []

        for uid, uname in user_data.items():
            album_info_url = "http://ws.audioscrobbler.com/2.0/"
            album_params = {
                "method": "album.getinfo",
                "user": uname,
                "api_key": API_KEY,
                "artist": artist_name,
                "album": album_name,
                "format": "json"
            }

            try:
                album_info = requests.get(album_info_url, params=album_params).json()
                user_playcount = album_info.get("album", {}).get("userplaycount", 0)
            except Exception as e:
                print(f"error fetching album info for {uname}: {e}")
                continue

            if user_playcount and int(user_playcount) > 0:
                try:
                    member = await ctx.bot.fetch_user(int(uid))
                    known_users.append((member.display_name, user_playcount, uname))
                except discord.NotFound:
                    pass 

        if not known_users:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: no one has listened to **{album_name}** by **{artist_name}**.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        known_users.sort(key=lambda x: int(x[1]), reverse=True)

        description = "\n".join([
            f"{i+1}. **[{name}](https://www.last.fm/user/{uname})** - **{count}** plays"
            for i, (name, count, uname) in enumerate(known_users)
        ])

        embed = discord.Embed(
            title=f"{album_name} by {artist_name} globally",
            url=f"https://www.last.fm/music/{artist_name.replace(' ', '+')}/{album_name.replace(' ', '+')}",
            description=description,
            color=discord.Color.from_str("#ffffff")
        )

        if album_art:
            embed.set_thumbnail(url=album_art)

        await ctx.send(embed=embed)

#############################################################################################################################################################

    @lf.command(name='wk', aliases=['whoknows'])
    async def wk(self, ctx, *, artist_name=None):
        user_id = str(ctx.author.id)

        if user_id not in user_data:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: you don't have an account connected. try ;connect <username>, then try the command again.",
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)
            return        

        username = user_data[user_id]

        if not artist_name:
            recent_url = "http://ws.audioscrobbler.com/2.0/"
            recent_params = {
                "method": "user.getrecenttracks",
                "user": username,
                "api_key": API_KEY,
                "format": "json",
                "limit": 1
            }

            recent_response = requests.get(recent_url, params=recent_params)
            recent_data = recent_response.json()

            try:
                artist_name = recent_data["recenttracks"]["track"][0]["artist"]["#text"]
            except (KeyError, IndexError):
                embed = discord.Embed(
                    description=f"{ctx.author.mention}: couldn't get the currently playing artist.. try again?",
                    color=discord.Color.from_str("#ffffff"),
                )
                await ctx.send(embed=embed)
                return

        known_users = []

        for member in ctx.guild.members:
            uid = str(member.id)
            if uid not in user_data:
                continue

            uname = user_data[uid]

            info_url = "http://ws.audioscrobbler.com/2.0/"
            info_params = {
                "method": "artist.getinfo",
                "artist": artist_name,
                "username": uname,
                "api_key": API_KEY,
                "format": "json"
            }

            try:
                info_response = requests.get(info_url, params=info_params)
                info_data = info_response.json()
                user_playcount = info_data.get("artist", {}).get("stats", {}).get("userplaycount", 0)
            except:
                continue

            if user_playcount and int(user_playcount) > 0:
                known_users.append((member.display_name, user_playcount, uname))

        if not known_users:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: no one in this server has listened to **{artist_name}**.",
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)
            return

        known_users.sort(key=lambda x: int(x[1]), reverse=True)



        description = "\n".join([
            f"{i+1}. **[{name}](https://www.last.fm/user/{uname})** - **{count}** plays"
            for i, (name, count, uname) in enumerate(known_users)
        ])

        artist_image = None
        if "artist" in info_data and "image" in info_data["artist"]:
            artist_image = info_data["artist"]["image"][-1].get("#text")

        embed = discord.Embed(
            title=f"{artist_name} in {ctx.guild.name}",
            url=f"https://www.last.fm/music/{artist_name.replace(' ', '+')}",
            description=description,
            color=discord.Color.from_str("#ffffff")
        )

        if artist_image:
            embed.set_thumbnail(url=artist_image)


        await ctx.send(embed=embed)


#############################################################################################################################################################


    @lf.command(name='gwk', aliases=['globallywhoknows'])
    async def gwk(self, ctx, *, artist_name=None):
        user_id = str(ctx.author.id)

        if user_id not in user_data:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: you don't have an account connected. try ;connect <username>, then try the command again.",
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)
            return        

        username = user_data[user_id]

        if not artist_name:
            recent_url = "http://ws.audioscrobbler.com/2.0/"
            recent_params = {
                "method": "user.getrecenttracks",
                "user": username,
                "api_key": API_KEY,
                "format": "json",
                "limit": 1
            }

            recent_response = requests.get(recent_url, params=recent_params)
            recent_data = recent_response.json()

            try:
                artist_name = recent_data["recenttracks"]["track"][0]["artist"]["#text"]
            except (KeyError, IndexError):
                embed = discord.Embed(
                    description=f"{ctx.author.mention}: couldn't get the currently playing artist.. try again?",
                    color=discord.Color.from_str("#ffffff"),
                )
                await ctx.send(embed=embed)
                return

        known_users = []
        artist_image = None 

        for uid, uname in user_data.items():
            info_url = "http://ws.audioscrobbler.com/2.0/"
            info_params = {
                "method": "artist.getinfo",
                "artist": artist_name,
                "username": uname,
                "api_key": API_KEY,
                "format": "json"
            }

            try:
                info_response = requests.get(info_url, params=info_params)
                info_data = info_response.json()
                user_playcount = info_data.get("artist", {}).get("stats", {}).get("userplaycount", 0)

                if not artist_image and "image" in info_data.get("artist", {}):
                    artist_image = info_data["artist"]["image"][-1].get("#text")

            except:
                continue

            if user_playcount and int(user_playcount) > 0:
                known_users.append((uname, user_playcount, uname))

        if not known_users:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: no one globally has listened to *{artist_name}*.",
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)
            return

        known_users.sort(key=lambda x: int(x[1]), reverse=True)

        description = "\n".join([
            f"{i+1}. **[{uname}](https://www.last.fm/user/{uname})** - **{count}** plays"
            for i, (uname, count, _) in enumerate(known_users[:10])
        ])

        embed = discord.Embed(
            title=f"{artist_name} globally",
            url=f"https://www.last.fm/music/{artist_name.replace(' ', '+')}",
            description=description,
            color=discord.Color.from_str("#ffffff")
        )

        if artist_image:
            embed.set_thumbnail(url=artist_image)

        await ctx.send(embed=embed)

#############################################################################################################################################################

    @lf.command(name='profile', aliases=['p'])
    async def profile(self, ctx, member: discord.Member = None):
        user_id = str(member.id) if member else str(ctx.author.id)

        if user_id not in user_data:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: you don't have an account connected. Try `;connect <username>`, then try the command again.",
                color=discord.Color.from_str("#ffffff"),
            )
            await ctx.send(embed=embed)
            return

        username = user_data[user_id]
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "user.getinfo",
            "user": username,
            "api_key": API_KEY,
            "format": "json"
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
        except requests.RequestException:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: Failed to contact Last.fm. Try again later.",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        if "user" not in data:
            embed = discord.Embed(
                description=f"{ctx.author.mention}: Could not retrieve data. Is your Last.fm username correct?",
                color=discord.Color.from_str("#ffffff")
            )
            await ctx.send(embed=embed)
            return

        user_info = data["user"]
        profile_url = user_info.get("url")
        playcount = int(user_info.get("playcount", 0))
        registered_unix = int(user_info.get("registered", {}).get("#text", 0))
        registered_date = datetime.utcfromtimestamp(registered_unix)
        now = datetime.utcnow()

        days_active = max((now - registered_date).days, 1)
        avg_daily = playcount / days_active

        # Fallback values
        avatar_url = user_info.get("image", [{}])[-1].get("#text", None)
        album_count = user_info.get("album_count", "Unknown")
        artist_count = user_info.get("artist_count", "Unknown")
        track_count = user_info.get("track_count", "Unknown")
        avatar_url = user_info.get("image", [{}])[-1].get("#text", None)

        embed = discord.Embed(
            color=discord.Color.from_str("#ffffff"),
        )

        embed.add_field(
            name=f"last.fm profile",
            value=f"**[{username}](https://www.last.fm/user/{username})**",
            inline=False
        )
        embed.add_field(name=f"**created on:**", value=registered_date.strftime("%m/%d/%Y"), inline=False)
        embed.add_field(
            name="**stats:**",
            value=(
                f"**{playcount:,}** scrobbles\n"
                f"**{avg_daily:.2f}** average scrobbles a day"
            ),
            inline=True
        )

        if avatar_url:
            embed.set_thumbnail(url=avatar_url)

        await ctx.send(embed=embed)

#############################################################################################################################################################

    

#############################################################################################################################################################


async def setup(bot):
    await bot.add_cog(lastfm(bot))