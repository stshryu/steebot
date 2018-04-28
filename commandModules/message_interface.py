import discord
import botMain
import config
import commandModules.cowsay_driver as cowsay

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
        # Cowsay Templates
        self.default_image = [[' ', '\\', ' ', ' ', ' ', '^', '_', '_', '^'], [' ', ' ', '\\', ' ', ' ', '(', 'o', 'o', ')', '\\', '_', '_', '_', '_', '_', '_', '_'], [' ', ' ', ' ', ' ', ' ', '(', '_', '_', ')', '\\', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ')', '\\', '/', '\\'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', '|', '-', '-', '-', '-', 'w', ' ', '|'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', '|', ' ', ' ', ' ', ' ', ' ', '|', '|'],[1,6],[1,7],[3,7]]

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
        elif _type == 2:
            message = ":ballot_box_with_check:NEW JOB <@" + config.ownerID + ">:ballot_box_with_check:NEW CAT <@" \
                        + config.ownerID + "> :ballot_box_with_check:NO POOP <@" + config.ownerID + ">:ballot_box_with_check:" \
                        + "MUST BE NEW <@" + config.ownerID + ">:100: :100: :ok_hand:"
            return self.clap_template.format(author, message)

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

    def returnCowsay(self, message, author):
        # Cowsay templates must be refreshsed?? Or something because they no longer work
        # with a globally asigned image
        image = [[' ', '\\', ' ', ' ', ' ', '^', '_', '_', '^'], [' ', ' ', '\\', ' ', ' ', '(', 'o', 'o', ')', '\\', '_', '_', '_', '_', '_', '_', '_'], [' ', ' ', ' ', ' ', ' ', '(', '_', '_', ')', '\\', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ')', '\\', '/', '\\'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', '|', '-', '-', '-', '-', 'w', ' ', '|'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', '|', ' ', ' ', ' ', ' ', ' ', '|', '|'],[1,6],[1,7],[3,7]]
        flags = cowsay.msgParser(message)
        if('Error:' in flags or 'Cowsay Help:' in flags):
            return flags
        message_ = cowsay.messageEngine(flags)
        response = cowsay.imageEngine(message_, image, flags)
        return response

    #</editor-fold>
