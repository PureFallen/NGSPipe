import os
import shutil
import subprocess
from threading import Thread

import requests
import toml
from sys import exit
from time import sleep

from Records import LogLine, Config, Request
from NGSLogPrep import NGSLogPrep
from lib import prints
from lib.colors import BColors

VERSION = '7.1.0'


def init() -> (NGSLogPrep, Config):
    # Enable ANSI codes (required for Prints/Color)
    os.system('')
    prints.print_info(f'Running Version {VERSION}')

    # Create NGSLogPrep object for chatlog
    chatlog = NGSLogPrep('ChatLog')
    prints.print_info(f'Game documents folder used is {chatlog.log_path}')

    # Open configuration file
    try:
        config = toml.load('./config.toml')
    except FileNotFoundError:
        prints.print_error('Unable to find required "config.toml". Did you extract this program correctly?')
        input()
        exit(0)

    # Open identity file id.toml; prepare global backup for future executions
    appdata_path = os.getenv('APPDATA') + '/PureFallen'
    if not os.path.isdir(appdata_path):
        os.mkdir(appdata_path)

    try:
        id_card = toml.load('./id.toml')
    except FileNotFoundError:
        try:
            id_card = toml.load(appdata_path + '/id.toml')
            prints.print_info(BColors.YELLOW + 'Local "id.toml" was not found. However, but there was a global '
                                               '"id.toml" available. Please insert a local "id.toml" if you plan to '
                                               'make changes to your identifier.')
        except FileNotFoundError:
            prints.print_error('Unable to find "id.toml" locally or globally. Please create or obtain a "id.toml" file '
                               'from the developer.')
            input()
            exit(0)
    else:
        # Backup locally found id.toml
        shutil.copyfile('./id.toml', appdata_path + '/id.toml')

    # Obtain values from configuration and identity file
    try:
        configs = Config(config, id_card, chatlog.log_path)
    except KeyError:
        prints.print_error('Unable to read toml configurations. Are the keys named and set correctly?')
        input()
        exit(0)

    prints.print_info('config read successfully.')
    return chatlog, configs


def log_loop(log_object: NGSLogPrep, parser_method, configs: Config):
    while True:
        sleep(1)

        for line in log_object.get_lines():
            log_line = LogLine(line)

            # Check if chat message comes from right chat window
            if log_line.chat_type == configs.chat_type:
                # Escape characters used for formatting of final message in usernames
                log_line.player_name = log_line.player_name.replace('`', r'\`')

                parser_method(log_line, configs)


def chat_parser(log_line: LogLine, configs: Config):
    # Setup request with default values
    request = Request(configs.chat_name, configs.webhook_url)

    # Remove commands designating chat channels
    if log_line.message.startswith(('/a ', '/p ', '/t ')):
        log_line.message = log_line.message[3:]
    log_line.message = log_line.message.replace('@everyone', '@​everyone')
    log_line.message = log_line.message.replace('@here', '@​here')

    # Check if chat message is an ingame command (catch ingame commands not meant to be displayed)
    if not log_line.message.startswith('/'):
        # Set Normal Chat Message/invalid command
        request.content = f'`{configs.chat_name}@{log_line.player_name}:` {log_line.message}'
        # Check if chat message is a bot command
        if log_line.message.startswith('!') or log_line.message.startswith('@'):
            request = chat_command_handler(log_line, configs, request)
    elif log_line.message.startswith('/toge '):
        request.content = f'`{configs.chat_name}@{log_line.player_name} screams` **{log_line.message[6:]}**'
    elif log_line.message.startswith('/moya '):
        request.content = f'`{configs.chat_name}@{log_line.player_name} thinks` *{log_line.message[6:]}*'

    # Send Webhook Request if message content was set:
    if request.content:
        web_request(request)

    del log_line


# Outsourced logic for bot command handling to decrease cyclic complexity
def chat_command_handler(log_line: LogLine, configs: Config, request: Request) -> Request:
    # Split chat message into list of words
    msg_list = log_line.message.split(' ')
    # Ensure case-insensitivity on commands
    prefix = msg_list[0][0]
    command = msg_list[0][1:].lower()

    # Check if command is in bot commands dictionary:
    if command in configs.bot_commands:
        if configs.bot_commands[command]["override_message"]:
            request.content = eval(configs.bot_commands[command]["override_message"])
        else:
            request.content = f'`{configs.chat_name}@{log_line.player_name}:` '

            if prefix == '!':
                request.content = request.content + f'<@{configs.bot_commands[command]["ping"]}> '

            request.content = request.content + f'{" ".join(msg_list[1:])}'
        if configs.bot_commands[command]["override_webhook"]:
            request.webhook_url = configs.bot_commands[command]["override_webhook"]

    return request


def symbol_parser(log_line: LogLine, configs: Config):
    # Setup request with default values
    request = Request(configs.chat_name, configs.webhook_url)
    request.content = f'`{configs.chat_name}@{log_line.player_name} has posted a Symbol Art!`'

    # Assemble path to Symbol Art
    request.files = os.path.join(configs.log_path, rf'symbolarts\cache\sa{log_line.message}')

    # Convert Symbol Art to PNG; hide console output on stderr caused by SarConvert.exe
    subprocess.run([r'.\utils\SarConvert.exe', rf'{request.files}.sar'], stderr=subprocess.DEVNULL)

    # Send Webhook Request
    web_request(request)
    del log_line


def web_request(request: Request):
    files = {}
    # Attach Symbol Art PNG
    if request.files:
        try:
            files = {'file': (f'{request.files}.png', open(f'{request.files}.png', 'rb'))}
        except FileNotFoundError:
            prints.print_error(
                f'Unable to send Symbol Art with Hash {request.files[-32:]}. Most likely, SarConvert.exe '
                f'failed to operate or the Symbol Art is in your Saved List. Unfortunately, we are '
                f'currently unable to send Symbol Arts into the Webhook that are part of your Saved '
                f'List, as the game will not store them in the cache.')
            files = {}

    while True:
        try:
            response = requests.post(request.webhook_url, files=files, data={'content': request.content})
            match response.status_code:
                # Message with file attachment send successfully
                case 200:
                    prints.print_info(f'{BColors.GREEN}{request.content} ({request.files[-32:]})')

                    # Close and delete converted Symbol Art PNG and TXT
                    files = {}
                    os.remove(f'{request.files}.png')
                    os.remove(f'{request.files}.txt')

                    break

                # Message send successfully
                case 204:
                    prints.print_info(BColors.GREEN + request.content)

                    break

                # Webhook not found
                case 404:
                    prints.print_error('Status 404: The Webhook specified in config.toml is invalid or was '
                                       'killswitched before.')
                    input()
                    exit(0)

                # "You have been rate-limited."
                case 429:
                    cooldown = response.json()['retry_after']
                    request.content(f'Notice: {request.chat_name} recovered from Webhook Rate Limitation ({cooldown} '
                                    f'seconds).` \n' + request.content)

                # Catch unexpected HTTP Status Codes
                case _:
                    prints.print_error(f'Unexpected HTTP Status Code: {response.status_code}\n'
                                       f'Message: {request.chat_name}\n'
                                       f'File: {request.files}')

                    break
        except requests.exceptions.ConnectionError as e:
            prints.print_error(e)
            sleep(5)

    del request


if __name__ == '__main__':
    try:
        log, c = init()

        # Thread Loop Chat Log Parsing
        t = Thread(target=log_loop,
                   args=(log, chat_parser, c),
                   daemon=True)
        t.start()

        # Create NGSLogPrep object for Symbolart chatlog
        symbol_chat = NGSLogPrep('SymbolChatLog')

        # Loop Symbolart Chat Log Parsing
        log_loop(symbol_chat, symbol_parser, c)
    except KeyboardInterrupt:
        prints.print_info(BColors.YELLOW + 'Program closed by user (CTRL+C)')
        exit(0)
