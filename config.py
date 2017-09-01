import configparser

# Initialize
config = configparser.ConfigParser()
config.read('config/config.ini')

# Bot Information
Bot_Username = config['Bot Info']['username']
Bot_Token = config['Bot Info']['token']
ownerID = config['Bot Info']['ownerID']

# App Information
App_ID = config['App Info']['ID']
App_Secret = config['App Info']['secret']
APP_DB_IP = config['App Info']['mysqlStagingIP']
APP_DB_USER = config['App Info']['mysqlStagingUser']
APP_DB_PASS = config['App Info']['mysqlStagingPassword']
APP_DB_DEFAULTDB = config['App Info']['mysqlStagingDatabase']

# Twitch Information
Twitch_ClientID = config['Twitch Info']['ID']
Twitch_Secret = config['Twitch Info']['secret']
