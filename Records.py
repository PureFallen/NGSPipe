class Config:
    def __init__(self, config: dict, id_card: dict, log_path: str) -> None:
        # parser_args: ('<CHAT_NAME>', '<CHAT_TYPE>', '<PUBLIC_WEBHOOK_URL>', '<BOT_COMMANDS>', '<CONFIG_VERSION>',
        # <SCRIPT_HOST>', '<GAME_DOC_PATH>')
        self.__chat_type = config['chat_type']
        self.__webhook_url = config['webhook_url']
        self.__bot_commands = config['commands']
        self.__config_version = config['version']

        self.__chat_name = id_card['chat_name']
        self.__script_host = id_card['script_host']
        self.__log_path = log_path

    @property
    def chat_type(self):
        return self.__chat_type

    @chat_type.setter
    def chat_type(self, value):
        self.__chat_type = value

    @property
    def webhook_url(self):
        return self.__webhook_url

    @webhook_url.setter
    def webhook_url(self, value):
        self.__webhook_url = value

    @property
    def bot_commands(self):
        return self.__bot_commands

    @bot_commands.setter
    def bot_commands(self, value):
        self.__bot_commands = value

    @property
    def config_version(self):
        return self.__config_version

    @config_version.setter
    def config_version(self, value):
        self.__config_version = value

    @property
    def chat_name(self):
        return self.__chat_name

    @chat_name.setter
    def chat_name(self, value):
        self.__chat_name = value

    @property
    def script_host(self):
        return self.__script_host

    @script_host.setter
    def script_host(self, value):
        self.__script_host = value

    @property
    def log_path(self):
        return self.__log_path

    @log_path.setter
    def log_path(self, value):
        self.__log_path = value


class LogLine:
    def __init__(self, line: str):
        line_list = line.split('\t')

        # line_list: ['<DATE>T<TIME>', '<MESSAGE_ID>', <'CHAT_TYPE'>, '<PLAYER_ID>', '<PLAYER_NAME>', '<MESSAGE>']
        self.__date = line_list[0].split('T')[0]
        self.__time = line_list[0].split('T')[1]
        self.__message_id = line_list[1]
        self.__chat_type = line_list[2]
        self.__player_id = line_list[3]
        self.__player_name = line_list[4]
        self.__message = line_list[5]

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = value

    @property
    def message_id(self):
        return self.__message_id

    @message_id.setter
    def message_id(self, value):
        self.__message_id = value

    @property
    def chat_type(self):
        return self.__chat_type

    @chat_type.setter
    def chat_type(self, value):
        self.__chat_type = value

    @property
    def player_id(self):
        return self.__player_id

    @player_id.setter
    def player_id(self, value):
        self.__player_id = value

    @property
    def player_name(self):
        return self.__player_name

    @player_name.setter
    def player_name(self, value):
        self.__player_name = value

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value


class Request:
    def __init__(self, chat_name, webhook_url):
        # request: ['<CHAT_NAME>', '<WEBHOOK_URL>', '<CONTENT>', '[FILES]']
        self.__chat_name = chat_name
        self.__webhook_url = webhook_url
        self.__content = ''
        self.__files = ''

    @property
    def chat_name(self):
        return self.__chat_name

    @chat_name.setter
    def chat_name(self, value):
        self.__chat_name = value

    @property
    def webhook_url(self):
        return self.__webhook_url

    @webhook_url.setter
    def webhook_url(self, value):
        self.__webhook_url = value

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    @property
    def files(self):
        return self.__files

    @files.setter
    def files(self, value):
        self.__files = value
