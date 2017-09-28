import discord
import botMain
import config

# TODO: Add a DB event for messages like clap so users can make their own emoji messages

class message_handler:
    def __init__(self):
        # Basic Templates
        self.error_template = "Error: {}"
        # Emoji
        self.emojiClap = ":clap:"
        self.emojiToilet = ":toilet:"
        self.emojiPoop = ":poop:"
        # Emoji Templates
        self.clap_template = "**{}** said: **{}**"
        # Twitch Templates
        self.twitch_notification_template = ""
        self.twitch_success_template = "Successfully {} **{}**"
        # Markov Templates
        self.markov_template = "**Imitating <@{}>**: **{}**"
        self.markov_msg_error = "You must specifiy a user to imitate or specify \"me\". ({})"

    #<editor-fold> Emoji Messages

    def createEmojiMessage(self, author, message, _type):
        if _type == 'clap':
            split = message.split(' ')
            output_msg = []
            for item in split[1:]:
                output_msg.append(self.emojiClap)
                output_msg.append(item)
            output_msg.append(self.emojiClap)
            response = ''.join(map(str, output_msg))
            return self.clap_template.format(author, response)
        elif _type == 'toilet':
            split = message.split(' ')
            output_msg = []
            for item in split[1:]:
                output_msg.append(self.emojiPoop)
                output_msg.append(item)
            output_msg.append(self.emojiToilet)
            response = ''.join(map(str, output_msg))
            return self.clap_template.format(author, response)

    def returnSteebClap(self, author, _type=0):
        if _type == 0:
            message = 'don\'t pretend to be an OkBread unless you poop uncontrollably'
            split = message.split(' ')
            output_msg = []
            for item in split:
                output_msg.append(self.emojiClap)
                output_msg.append(item)
            output_msg.append(self.emojiClap)
            response = ''.join(map(str, output_msg))
            return self.clap_template.format(author, response)
        elif _type == 1:
            message = "me name steeb <@" + config.ownerID + "> me like extra cheese <@" + config.ownerID + ">"
            split = message.split(' ')
            output_msg = []
            for item in split:
                output_msg.append(self.emojiPoop)
                output_msg.append(item)
            output_msg.append(self.emojiToilet)
            response = ''.join(map(str, output_msg))
            return self.clap_template.format(author, response)

    def returnTimClap(self, author):
        message = 'member tim? always online for video games tim? i member. good ole days tim the tim timmerson'
        split = message.split(' ')
        output_msg = []
        for item in split:
            output_msg.append(self.emojiClap)
            output_msg.append(item)
        output_msg.append(self.emojiClap)
        response = ''.join(map(str, output_msg))
        return self.clap_template.format(author, response)
    #</editor-fold>

    #<editor-fold> Markov messages
    def returnMarkovChain(self, author, response):
        return self.markov_template.format(author, response)

    def returnMarkovMsgError(self, error_code):
        return self.markov_msg_error.format('Error: '+error_code)
    #</editor-fold>
