import discord
import os
from dotenv import load_dotenv
from chatgpt import ask_chatgpt

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ALLOWED_CHANNEL_ID = int(os.getenv("ALLOWED_CHANNEL_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Key = (user_id, context_id) → context_id = channel ID or "dm"
conversation_history = {}

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    is_dm = isinstance(message.channel, discord.DMChannel)
    is_allowed_channel = message.channel.id == ALLOWED_CHANNEL_ID

    if not is_dm and not is_allowed_channel:
        return

    user_id = str(message.author.id)
    context_id = "dm" if is_dm else str(message.channel.id)
    key = (user_id, context_id)

    if message.content.strip().lower() == ".reset":
        if key in conversation_history:
            del conversation_history[key]
        await message.channel.send("🔄 Conversation history has been reset.")
        return

    if key not in conversation_history:
        conversation_history[key] = []

    conversation_history[key].append({"role": "user", "content": message.content})
    await message.channel.typing()

    try:
        reply = await ask_chatgpt(conversation_history[key])
        conversation_history[key].append({"role": "assistant", "content": reply})
        await message.channel.send(reply)
    except Exception as e:
        print(f"❌ Error: {e}")
        await message.channel.send("❌ An error occurred while calling OpenRouter!, join https://discord.gg/7C2HHGsnYH for help ")

client.run(DISCORD_TOKEN)


#-- MADE BY DAI VIET --
