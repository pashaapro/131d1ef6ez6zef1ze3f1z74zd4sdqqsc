import discord
from discord.ext import commands
import datetime
from datetime import datetime
import pyfiglet
import base64
import codecs
import requests
import asyncio
import json
import wikipedia


current_time = datetime.now().strftime("%H:%M:%S")
green_check = "✅"
red_cross = "❌"
load_emoji = "🔄"
deleted_messages = {}
bot = commands.Bot(command_prefix='@', self_bot=True)
bot.remove_command('help')
perms_file = "perms.json"
already_replied = set()

try:
    with open('perms.json', 'r') as f:
        authorized_users = set(json.load(f))
except FileNotFoundError:
    authorized_users = set()


def load_perms():
    try:
        with open(perms_file, 'r') as file:
            perms = json.load(file)
    except FileNotFoundError:
        perms = []
    return perms

def save_perms(perms):
    with open(perms_file, 'w') as file:
        json.dump(perms, file, indent=4)

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

def save_config(file_path, config):
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)

config_file = "config.json"
config = load_config(config_file)



async def reconnect():
    while True:
        if not bot.is_closed():
            await asyncio.sleep(10)  
        else:
            print('Reconnecting...')
            try:
                await bot.start(config['token'])
            except Exception as e:
                print(f'Failed to reconnect')
            await asyncio.sleep(10)  

async def readyyy():
    global selfid
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    selfid = bot.user.id
    perms = load_perms()
    if selfid not in perms:
        print("Selfbot not in perms.json, adding it...")
        perms.append(selfid)
        save_perms(perms)
        print("Selfbot added in perms.json")
        print("prefix: ", config["prefix"])
    else:
        print("Selfbot in perms.json, all good")
        print("prefix: ", config["prefix"])



################################################################################
#                                                                              #
#                                                                              #
#                             bot event                                        #
#                                                                              #
#                                                                              #
################################################################################
        

@bot.event
async def on_ready():
    try:
        await readyyy()
    except Exception as e:
        print(e)


@bot.event
async def on_message(message):
    try:
        await handle_command(message)
    except Exception as e:
        pass                 


@bot.event
async def on_message_edit(before, after):
    await handle_command(after)

@bot.event
async def on_relationship_add(relationship):
    if relationship.type == discord.RelationshipType.incoming_request:
        await relationship.accept()





################################################################################
#                                                                              #
#                                                                              #
#                             bot cmd index                                    #
#                                                                              #
#                                                                              #
################################################################################

async def handle_command(message):
    prefix = config['prefix']  
    if message.author.id in authorized_users:
        content = message.content
        if content.startswith(prefix):
            content = content[len(prefix):]  
            command, *args = content.split()
            if command == 'ping':
                await ping(message)
            elif command == 'userinfo':
                await userinfo(message, *args)
            elif command == 'ascii':
                await ascii_command(message, ' '.join(args))
            elif command == 'regional':
                await regional(message, ' '.join(args))
            elif command == 'space':
                await space(message, ' '.join(args))  
            elif command == 'smart':
                await smart(message, ' '.join(args))
            elif command == 'reverse':
                await reverse(message, ' '.join(args))
            elif command == 'italic':
                await italic(message, ' '.join(args))
            elif command == 'owo':
                await owo(message, ' '.join(args))
            elif command == 'encode':
                await encode(message, ' '.join(args))
            elif command == 'decode':
                await decode(message, ' '.join(args))
            elif command == 'encrypt':
                await encrypt(message, ' '.join(args))
            elif command == 'decrypt':
                await decrypt(message, ' '.join(args))
            elif command == 'text2bin':
                await text2bin(message, ' '.join(args))
            elif command == 'bin2text':
                await bin2text(message, ' '.join(args))
            elif command == 'text2hex':
                await text2hex(message, ' '.join(args))
            elif command == 'hex2text':
                await hex2text(message, ' '.join(args))
            elif command == 'addperm':
                await addperm(message, *args)
            elif command == 'removeperm':
                await removeperm(message, *args)
            elif command == 'help':
                await help(message)
            elif command == 'cat':
                await random_cat(message)
            elif command == 'fox':
                await random_fox(message)
            elif command == 'dog':
                await random_dog(message)
            elif command == 'wiki':
                await wiki(message, ' '.join(args))
            elif command == 'snipe':
                await snipe(message, ' '.join(args))
            elif command == 'prefix':
                await update_prefix(message, *args)
            else:
                return
        else:
            await bot.process_commands(message)

################################################################################
#                                                                              #
#                                                                              #
#                             bot cmd def                                      #
#                                                                              #
#                                                                              #
################################################################################



async def ping(ctx):
    await ctx.add_reaction(load_emoji)
    print(f'Command used: ping by: {ctx.author.name} ({ctx.author.id}) at {ctx.created_at}')
    await ctx.reply(f'**Pong!** {round(bot.latency * 1000)}ms')
    await ctx.add_reaction(green_check)
    

async def userinfo(message, user_id):
    await message.add_reaction(load_emoji)
    print(f'Command used: userinfo by: {message.author.name} ({message.author.id}) at {message.created_at}')
    
    user = bot.get_user(int(user_id))
    if not user:
        await message.reply(content='User not found')
        await message.add_reaction(red_cross)
        return
    
    created_at = str(user.created_at) if user.created_at else 'Null'
    avatar_url = str(user.avatar.url) if user.avatar else 'No profile pic'
    response = f'`Account created at: {created_at}\nProfile pic: {avatar_url}\nUser ID: {user_id}\nUsername: {user.name}`'
    
    await message.reply(content=response)
    await message.add_reaction(green_check)


async def ascii_command(message, text):
    await message.add_reaction(load_emoji)
    print(f'Command used: ascii by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if text:
        ascii_art = pyfiglet.figlet_format(text)
        await message.reply(content=f"```{ascii_art}```")
        await message.add_reaction(green_check)
    else:
        await message.reply(content="Please provide text for ASCII art.")
        await message.add_reaction(red_cross)

async def regional(message, text):
    await message.add_reaction(load_emoji)
    print(f'Command used: regional by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if text:
        regional_text = "".join([chr(ord(char) + 127397) if char.isalpha() else char for char in text])
        await message.reply(content=regional_text)
        await message.add_reaction(green_check)
    else:
        await message.reply(content="Please provide text for regional conversion.")
        await message.add_reaction(red_cross)

async def space(message, text):
    await message.add_reaction(load_emoji)
    print(f'Command used: space by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if text:
        spaced_text = " ".join(list(text))
        await message.reply(content=spaced_text)
        await message.add_reaction(green_check)
    else:
        await message.reply(content="Please provide text for spaced message.")
        await message.add_reaction(red_cross)

async def smart(message, text):
    await message.add_reaction(load_emoji)
    print(f'Command used: smart by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if text:
        smart_text = "".join([char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(text)])
        await message.reply(content=smart_text)
        await message.add_reaction(green_check)
    else:
        await message.reply(content="Please provide text for smart talk.")
        await message.add_reaction(red_cross)

async def reverse(message, text):
    await message.add_reaction(load_emoji)
    print(f'Command used: reverse by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if text:
        reversed_text = text[::-1]
        await message.reply(content=reversed_text)
        await message.add_reaction(green_check)
    else:
        await message.reply(content="Please provide text for reversal.")
        await message.add_reaction(red_cross)

async def italic(message, text):
    await message.add_reaction(load_emoji)
    print(f'Command used: italic by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if text:
        italic_text = "*" + text + "*"
        await message.reply(content=italic_text)
        await message.add_reaction(green_check)
    else:
        await message.reply(content="Please provide text for italic formatting.")
        await message.add_reaction(red_cross)

async def owo(message, text):
    await message.add_reaction(load_emoji)
    print(f'Command used: owo by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if text:
        owo_text = text.replace('r', 'w').replace('l', 'w').replace('R', 'W').replace('L', 'W').replace('n', 'ny').replace('N', 'NY')
        await message.reply(content=owo_text)
        await message.add_reaction(green_check)
    else:
        await message.reply(content="Please provide text for owoification.")
        await message.add_reaction(red_cross)

async def encode(message, text):
    await message.add_reaction(load_emoji)
    print(f'Command used: encode by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if text:
        encoded_text = base64.b64encode(text.encode()).decode()
        await message.reply(content=encoded_text)
        await message.add_reaction(green_check)
    else:
        await message.reply(content="Please provide text for encoding.")
        await message.add_reaction(red_cross)

async def decode(message, base64_text):
    await message.add_reaction(load_emoji)
    print(f'Command used: decode by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if base64_text:
        try:
            decoded_text = base64.b64decode(base64_text).decode()
            await message.reply(content=decoded_text)
            await message.add_reaction(green_check)
        except Exception as e:
            await message.reply(content=f"Error decoding base64: {e}")
            await message.add_reaction(red_cross)
    else:
        await message.reply(content="Please provide base64-encoded text for decoding.")
        await message.add_reaction(red_cross)

async def encrypt(message, text):
    await message.add_reaction(load_emoji)
    print(f'Command used: encrypt by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if text:
        encrypted_text = codecs.encode(text, 'rot_13')
        await message.reply(content=encrypted_text)
        await message.add_reaction(green_check)
    else:
        await message.reply(content="Please provide text for encryption.")
        await message.add_reaction(red_cross)

async def decrypt(message, rot13_text):
    await message.add_reaction(load_emoji)
    print(f'Command used: decrypt by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if rot13_text:
        decrypted_text = codecs.decode(rot13_text, 'rot_13')
        await message.reply(content=decrypted_text)
        await message.add_reaction(green_check)
    else:
        await message.reply(content="Please provide text for decryption.")
        await message.add_reaction(red_cross)

async def text2bin(message, text):
    await message.add_reaction(load_emoji)
    print(f'Command used: text2bin by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if text:
        binary_text = ' '.join(format(ord(char), '08b') for char in text)
        await message.reply(content=binary_text)
        await message.add_reaction(green_check)
    else:
        await message.reply(content="Please provide text for binary conversion.")
        await message.add_reaction(red_cross)

async def bin2text(message, binary_text):
    await message.add_reaction(load_emoji)
    print(f'Command used: bin2text by: {message.author.name} ({message.author.id}) at {message.created_at}')

    binary_text = ''.join(filter(lambda x: x in '01', binary_text))
    if binary_text:
        try:
            text_from_binary = ''.join([chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8)])
            await message.reply(content=text_from_binary)
            await message.add_reaction(green_check)
        except ValueError:
            await message.reply(content="Invalid binary input.")
            await message.add_reaction(red_cross)
    else:
        await message.reply(content="Please provide binary text for conversion.")
        await message.add_reaction(red_cross)

async def text2hex(message, text):
    await message.add_reaction(load_emoji)
    print(f'Command used: text2hex by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if text:
        hex_text = ' '.join(hex(ord(char))[2:] for char in text)
        await message.reply(content=hex_text)
        await message.add_reaction(green_check)
    else:
        await message.reply(content="Please provide text for hexadecimal conversion.")
        await message.add_reaction(red_cross)

async def hex2text(message, hex_text):
    await message.add_reaction(load_emoji)
    print(f'Command used: hex2text by: {message.author.name} ({message.author.id}) at {message.created_at}')

    hex_text = ''.join(filter(lambda x: x.isdigit() or x.lower() in 'abcdef', hex_text))
    if hex_text:
        try:
            text_from_hex = bytearray.fromhex(hex_text).decode()
            await message.reply(content=text_from_hex)
            await message.add_reaction(green_check)
        except ValueError:
            await message.reply(content="Invalid hexadecimal input.")
            await message.add_reaction(red_cross)
    else:
        await message.reply(content="Please provide hexadecimal text for conversion.")
        await message.add_reaction(red_cross)



async def addperm(message, user_id):
    await message.add_reaction(load_emoji)
    print(f'Command used: addperm by: {message.author.name} ({message.author.id}) at {message.created_at}')

    if message.author.id == selfid:
        try:
            user_id = int(user_id)
            if user_id not in authorized_users:
                authorized_users.add(user_id)
                with open('perms.json', 'w') as f:
                    json.dump(list(authorized_users), f)
                await message.reply(content=f"{user_id} has been granted permission to use commands.")
                await message.add_reaction(green_check)
            else:
                await message.reply(content=f"{user_id} already has permission.")
                await message.add_reaction(red_cross)
        except ValueError:
            await message.reply(content="Invalid user ID.")
            await message.add_reaction(red_cross)
    else:
        await message.reply(content="You do not have permission to use this command.")
        await message.add_reaction(red_cross)

async def removeperm(message, user_id):
            await message.add_reaction(load_emoji)
            print(f'Command used: removeperm by: {message.author.name} ({message.author.id}) at {message.created_at}')

            if message.author.id == selfid:
                try:
                    user_id = int(user_id)
                    if user_id in authorized_users:
                        authorized_users.remove(user_id)
                        with open('perms.json', 'w') as f:
                            json.dump(list(authorized_users), f)
                        await message.reply(content=f"{user_id}'s permission to use commands has been revoked.")
                        await message.add_reaction(green_check)
                    else:
                        await message.reply(content=f"{user_id} does not have permission.")
                        await message.add_reaction(red_cross)
                except ValueError:
                    await message.reply(content="Invalid user ID.")
                    await message.add_reaction(red_cross)
            else:
                await message.reply(content="You do not have permission to use this command.")
                await message.add_reaction(red_cross)

async def help(message):
    await message.add_reaction(load_emoji)
    print(f'Command used: help by: {message.author.name} ({message.author.id}) at {message.created_at}')
    prefixhelp = config['prefix']
    help_message = (f"```ini\n[ Available Commands ]\n\n"
                    f"[ {prefixhelp}ping ]: Check bot's latency.\n"
                    f"[ {prefixhelp}userinfo <id> ]: Get user info.\n"
                    f"[ {prefixhelp}ascii <text> ]: Convert text to ASCII art.\n"
                    f"[ {prefixhelp}regional <text> ]: Convert text to regional indicators.\n"
                    f"[ {prefixhelp}space <text> ]: Add space between each character.\n"
                    f"[ {prefixhelp}smart <text> ]: Convert text to SmArT TeXt.\n"
                    f"[ {prefixhelp}reverse <text> ]: Reverse text.\n"
                    f"[ {prefixhelp}italic <text> ]: Format text in italic.\n"
                    f"[ {prefixhelp}owo <text> ]: Convert text to OwO language.\n"
                    f"[ {prefixhelp}encode <text> ]: Base64 encode text.\n"
                    f"[ {prefixhelp}decode <text> ]: Base64 decode text.\n"
                    f"[ {prefixhelp}encrypt <text> ]: Encrypt text with ROT13.\n"
                    f"[ {prefixhelp}decrypt <text> ]:  Decrypt ROT13 text.\n"
                    f"[ {prefixhelp}text2bin <text> ]: Convert text to binary.\n"
                    f"[ {prefixhelp}bin2text <text> ]: Convert binary to text.\n"
                    f"[ {prefixhelp}text2hex <text> ]: Convert text to hexadecimal.\n"
                    f"[ {prefixhelp}hex2text <text> ]: Convert hexadecimal to text.\n"
                    f"[ {prefixhelp}addperm <id> ]: Grant permission to a user.\n"
                    f"[ {prefixhelp}removeperm <id> ]: Revoke permission from a user.\n"
                    f"[ {prefixhelp}help ]: Show this help message.\n"
                    f"[ {prefixhelp}fox ]: Generate a random pic of a fox.\n"
                    f"[ {prefixhelp}dog ]: Generate a random pic of a dog.\n"
                    f"[ {prefixhelp}cat ]: Generate a random pic of a cat.\n"
                    f"[ {prefixhelp}wiki <lang> <text> ]: Search for a term on Wikipedia.```")
    
    await message.reply(content=help_message)
    await message.add_reaction(green_check)


async def random_cat(message):
    print(f'Command used: cat by: {message.author.name} ({message.author.id}) at {message.created_at}')
    await message.add_reaction(load_emoji)
    try:
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        data = response.json()
        cat_image_url = data[0]['url']
        await message.reply(content=cat_image_url)
        await message.add_reaction(green_check)
    except Exception as e:
        await message.add_reaction(red_cross)

async def random_fox(message):
    await message.add_reaction(load_emoji)
    print(f'Command used: fox by: {message.author.name} ({message.author.id}) at {message.created_at}')
    try:
        response = requests.get('https://randomfox.ca/floof/')
        data = response.json()
        fox_image_url = data['image']
        await message.reply(content=fox_image_url)
        await message.add_reaction(green_check)
    except Exception as e:
        await message.add_reaction(red_cross)

async def random_dog(message):
    await message.add_reaction(load_emoji)
    print(f'Command used: dog by: {message.author.name} ({message.author.id}) at {message.created_at}')
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = response.json()
        dog_image_url = data['message']
        await message.reply(content=dog_image_url)
        await message.add_reaction(green_check)
    except Exception as e:
        await message.add_reaction(red_cross)

async def wiki(message, terme):
    await message.add_reaction(load_emoji)
    print(f'Command used: wiki by: {message.author.name} ({message.author.id}) at {message.created_at}')
    args = terme.split()
    if len(args) < 2:
        await message.reply("Usage: @wiki [lang] [term]")
        await message.add_reaction(red_cross)
        return
    lang = args[0].lower()  
    terme = ' '.join(args[1:])  
    try:
        wikipedia.set_lang(lang)
        resultat = wikipedia.summary(terme, sentences=4)  
        await message.reply(resultat)
        await message.add_reaction(green_check)
    except wikipedia.exceptions.DisambiguationError as e:
        await message.reply(f"The term '{terme}' is ambiguous. Please specify.")
        await message.add_reaction(red_cross)
    except wikipedia.exceptions.PageError as e:
        await message.reply(f"No Wikipedia pages found for the term '{terme}'.")
        await message.add_reaction(red_cross)


async def snipe(message, num: int = 1):
    await message.add_reaction(load_emoji)
    channel_id = message.channel.id
    if channel_id in deleted_messages:
        deleted_message = deleted_messages[channel_id]
        if deleted_message.author == bot.user:
            await message.reply(f"{deleted_message.author}: {deleted_message.content}")
            await message.add_reaction(green_check)
        if isinstance(num, int) and num > 1:
            deleted_history = []
            async for msg in message.channel.history(limit=None):  
                if len(deleted_history) >= num:
                    break  
                if msg.author == bot.user:
                    continue  
                if msg.id in deleted_messages.values():
                    deleted_history.append(msg)
            if len(deleted_history) > 0:
                for msg in reversed(deleted_history):
                    await message.reply(f"{msg.author}: {msg.content}")
                    await message.add_reaction(green_check)
            else:
                await message.reply("No deleted messages found in this channel.")
                await message.add_reaction(red_cross)
        else:
            if deleted_message.author != bot.user:
                await message.reply(f"{deleted_message.author}: {deleted_message.content}")
                await message.add_reaction(green_check)
    else:
        await message.reply("No deleted messages found in this channel.")
        await message.add_reaction(red_cross)


async def update_prefix(message, new_prefix: str):
    print(f'Command used: prefix by: {message.author.name} ({message.author.id}) at {message.created_at}')
    await message.add_reaction(load_emoji)
    if message.author.id == selfid:
        config['prefix'] = new_prefix
        save_config('config.json', config)
        bot.command_prefix = new_prefix
        await message.reply(f"The prefix has been changed to: {new_prefix}")
        await message.add_reaction(green_check)
    else:
        await message.reply("You do not have permission to use this command.")
        await message.add_reaction(red_cross)

async def say(message):
    await message.send(message.content)



bot.run(config['token'])
