# bot.py
import os
import json
import requests

from web3 import Web3
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

seeder_contract = "0x2ed251752da7f24f33cfbd38438748bb8eeb44e1"
infura_url = "https://mainnet.infura.io/v3/{}".format(os.getenv('INFURA_PROJECT_ID'))

web3 = Web3(Web3.HTTPProvider(infura_url))
if web3.isConnected():
    print(f'Infura connected. Chain tip {web3.eth.blockNumber}')

f = open('seeder.json', "r")
abi = json.loads(f.read())["abi"]
address = Web3.toChecksumAddress(seeder_contract)

contract = web3.eth.contract(address=address, abi=abi)
f.close()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

def get_next_seed_timestamp(contract):
    nextseed = contract.functions.getNextAvailableBatch().call()
    response = f'<a:seeder:966863936244826152> **NEXT SEED** <t:{nextseed}:R>'
    return response

@bot.command(name='wenseed', help='Responds with the time remaining to the next seed')
async def wenseed(ctx):
    response = get_next_seed_timestamp(contract)
    await ctx.send(response)

def get_collection_floor(collection):
    response = requests.get("https://api.opensea.io/api/v1/collection/{}".format(collection))
    try:
        return response.json()["collection"]["stats"]["floor_price"]
    except Exception:
	    return "Couldn't fetch floor price"

@bot.command(name='floor', help='Responds with the time remaining to the next seed')
async def get_floor(ctx, arg=""):
    if arg == "" or arg == "fighter" or arg == "fighters":
        response = "**FIGHTER FLOOR:** " + str(get_collection_floor("raidpartyfighters")) + "Ξ"
    elif arg == "hero" or arg == "heroes":
        response = "**HERO FLOOR:** " + str(get_collection_floor("raidparty")) + "Ξ"
    else:
        response = "Can't understand the collection name (try !floor fighter or !floor hero)"

    await ctx.send(response)

bot.run(DISCORD_TOKEN)