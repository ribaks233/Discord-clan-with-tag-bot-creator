import discord
import asyncio
import struct
import json
import os
from discord.ext import commands

TOKEN = "BOT TOKEN" # put your own token
INTERVAL = 60 # DONT CHANGE FOR RATELIMIT
DELETE_DELAY = 2 # You can change
SERVER_NAME = "Tag server" # You can change


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def murmurhash3_32_gc(key: str, seed: int = 0) -> int:
    
    key = key.encode('utf-8')
    remainder = len(key) % 4
    bytes_ = len(key) - remainder
    h1 = seed
    
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    for i in range(0, bytes_, 4):
        k1 = struct.unpack_from('<I', key, i)[0]
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF

        h1 ^= k1
        h1 = ((h1 << 13) | (h1 >> 19)) & 0xFFFFFFFF
        h1 = (h1 * 5 + 0xe6546b64) & 0xFFFFFFFF

    k1 = 0
    if remainder == 3:
        k1 ^= key[bytes_ + 2] << 16
    if remainder >= 2:
        k1 ^= key[bytes_ + 1] << 8
    if remainder >= 1:
        k1 ^= key[bytes_]
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1

    h1 ^= len(key)
    h1 ^= (h1 >> 16)
    h1 = (h1 * 0x85ebca6b) & 0xFFFFFFFF
    h1 ^= (h1 >> 13)
    h1 = (h1 * 0xc2b2ae35) & 0xFFFFFFFF
    h1 ^= (h1 >> 16)

    return h1

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

    if len(bot.guilds) > 10:
        print(f"⚠️ In {len(bot.guilds)} guilds. Attempting to delete them all...")
        input("QUIT IF YOU DONT WANT THEM TO BE DELETED (only if bot is owner)")
        for guild in bot.guilds:
            try:
                print("Trying to delete")
                await guild.delete()
                print(f"🗑️ Deleted guild: {guild.name} ({guild.id})")
                await asyncio.sleep(1.5)
            except Exception as e:
                print(f"❌ Failed to delete {guild.name} ({guild.id}): {e}")
                await asyncio.sleep(2)

        if len(bot.guilds) > 0:
            print(f"⚠️ Still in {len(bot.guilds)} guilds after deletion.")
        else:
            print("✅ All guilds deleted.")

    asyncio.create_task(start_farming())
async def start_farming():
    while True:
        try:
            new_guild = await bot.create_guild(name=SERVER_NAME)
        except discord.HTTPException:
            await asyncio.sleep(INTERVAL)
            continue

        hash_val = murmurhash3_32_gc(f"2025-02_skill_trees:{new_guild.id}") % 10000

        if (10 <= hash_val < 20) or (60 <= hash_val < 100):
            print(f"🟢 GOOD: Guild ID {new_guild.id} | hash : {hash_val}")
            break
        else:
            print(f"🔴 BAD: Guild ID {new_guild.id} | hash : {hash_val}")
            await asyncio.sleep(DELETE_DELAY)
            try:
                await new_guild.delete()
            except:
                pass

        await asyncio.sleep(INTERVAL)

bot.run(TOKEN)
