import configparser

# Initialize
config = configparser.ConfigParser()
config.read('config/config.ini')

# Bot Information
Bot_Username = config['Bot Info']['username']
Bot_Token = config['Bot Info']['token']

# App Information
App_ID = config['App Info']['ID']
App_Secret = config['App Info']['secret']
