import discord
import os
from discord.ext import commands
from flask import Flask, request

# Load environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GITHUB_PAT = os.getenv("GITHUB_PAT")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Initialize bot and GitHub client
bot = commands.Bot(command_prefix="!")
g = Github(GITHUB_PAT)

# Flask app for GitHub webhooks
app = Flask(__name__)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command()
async def pr_status(ctx, repo_name: str, pr_number: int):
    try:
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        status = f'PR #{pr_number} - {pr.title}\nState: {pr.state}\nMergeable: {pr.mergeable}'
        await ctx.send(status)
    except Exception as e:
        await ctx.send(f'Error: {e}')


@bot.command()
async def notify_pr(ctx, repo_name: str):
    try:
        repo = g.get_repo(repo_name)
        prs = repo.get_pulls(state='open')
        if prs.totalCount == 0:
            await ctx.send('No open PRs found.')
        else:
            message = '\n'.join([f'#{pr.number}: {pr.title}' for pr in prs])
            await ctx.send(f'Open PRs:\n{message}')
    except Exception as e:
        await ctx.send(f'Error: {e}')


@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json
    action = data.get('action')
    repo_name = data['repository']['full_name']
    pr_number = data['pull_request']['number']
    pr_title = data['pull_request']['title']

    message = f'PR #{pr_number}: {pr_title} ({action}) in {repo_name}'

    async def send_message():
        channel = bot.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            await channel.send(message)

    bot.loop.create_task(send_message())
    return '', 200


if __name__ == '__main__':
    from threading import Thread

    Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()
    bot.run(DISCORD_TOKEN)
