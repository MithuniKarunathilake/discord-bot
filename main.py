import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import requests
import json
import config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

queues = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print("✅ The bot is now ready!")


@client.event
async def on_member_join(member):

    channel = client.get_channel(config.DISCORD_CHANNEL_ID)
    if not channel:
        print("⚠️ Channel not found! Make sure the bot has access to the correct channel.")
        return

    joke_url = "https://random-jokes-api.p.rapidapi.com/single"
    headers = {
        "x-rapidapi-key": "3a444c039amsh396e41ff52853fep1f58d6jsnaec66dac15f2",
        "x-rapidapi-host": "random-jokes-api.p.rapidapi.com"
    }

    try:
        response = requests.get(joke_url, headers=headers)
        joke_data = json.loads(response.text)
        joke = joke_data.get("content", "Oops! I couldn't fetch a joke right now. 😅")
    except Exception as e:
        print(f"⚠️ Error fetching joke: {e}")
        joke = "Oops! I couldn't fetch a joke right now. 😅"

    await channel.send(f"👋 Welcome to the server, {member.mention}! 🎉\nHere's a joke for you:\n\nWhy don't skeletons fight each other?\n\n...\n\nBecause they don’t have the guts! 💀😂")


@client.event
async def on_member_remove(member):
    channel = client.get_channel(1341653218517712990)
    if channel:
        await channel.send(f"Goodbye, {member.name}. We hope you have a great day! 😢")


@client.command()
async def hello(ctx):
    await ctx.send("Hello, I'm your virtual assistant! 😊")

@client.command(pass_content = True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        await ctx.send("I've joined the Voice channel!")
    else:
        await ctx.send("You're not in a Voice channel!")

@client.command(pass_content = True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the Voice channel!")
    else:
        await ctx.send("I'm not in a Voice channel!")

@client.command(pass_content = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
        await ctx.send("The music has been paused.")
    else:
        await ctx.send("There is no music currently playing.")

@client.command(pass_content = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        voice.resume()
        await ctx.send("The music has been resumed.")
    else:
        await ctx.send("The music is not paused.")

@client.command(pass_content = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.stop()
        await ctx.send("The music has been stopped.")
    else:
        await ctx.send("There is no music currently playing.")

@client.command(pass_content = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg + '.mp3')
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
    await ctx.send("The music " + arg + " has been played.")

@client.command(pass_content = True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg + '.mp3')
    guild_id = ctx.message.guild.id
    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]
    await ctx.send("The music has been queued.")

client.run(config.DISCORD_BOT_TOKEN)
