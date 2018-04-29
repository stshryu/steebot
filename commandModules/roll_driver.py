import random
from datetime import datetime

HELP = "```\n Roll Help: \n\n \
You can roll for a random number in a range <lower upper> \n \
E.G: !roll 20 600 returns a random number between 20 and 600 \n \
\n \
Typing just !roll returns a random number between 1 and 100 \
```"

def doesContainHelp(message):
    if '-h' in message or '-H' in message:
        return True
    else:
        return False

def msgParser(message):
    if doesContainHelp(message):
        return HELP
    if len(message.split(' ')) == 1:
        return "DEFAULT"
    no_cmd = message.split(' ')[1:]
    output = []
    if no_cmd[0].isdigit() and no_cmd[1].isdigit():
        if int(no_cmd[0]) > int(no_cmd[1]):
            return "**Error:** The lower bound can't be higher than the upper bound\n\
            Did you mean to say: _!roll " + str(no_cmd[1]) + " " + str(no_cmd[0]) + "?_"
        output.append(int(no_cmd[0]))
        output.append(int(no_cmd[1]))
        return output
    else:
        return "**Error:** The correct usage is *!roll lower upper*"

def roll(low=1, high=100):
    random.seed(datetime.now())
    return random.randint(low, high)

def roll_engine(message):
    output = []
    flags = msgParser(message)
    if('Error:' in flags or 'Roll Help:' in flags):
        return flags
    if('DEFAULT' in flags):
        output.append(1)
        output.append(100)
        output.append(roll())
        return output
    else:
        output.append(flags[0])
        output.append(flags[1])
        output.append(roll(flags[0], flags[1]))
        return output
