import re

# Internal Cowsay Constants
FLAG_N = 1
FLAG_W = 2
FLAG_b = 4
FLAG_d = 8
FLAG_g = 16
FLAG_p = 32
FLAG_t = 64
FLAG_w = 128

# Parse msg for flags
def msgParser(message):
    conv_table = {
        '-n':1,
        '-W':2,
        '-b':4,
        '-d':8,
        '-g':16,
        '-p':32,
        '-t':64,
        '-w':128,
    }
    # Remove the command from message
    no_cmd = message.split(' ')[1:]
    user_id = r"(<@)\d+(>)"
    emote = r"[:].+[:]"
    if re.search(user_id, ''.join(no_cmd)) or re.search(emote, ''.join(no_cmd)):
        return "Error: @mentions and :emotes: are not allowed"
    # Loop through parsed message for flags
    no_msg = []
    indexes_to_remove = []
    for i in range(0,len(no_cmd)):
        if '-e' in no_cmd[i] or '-i' in no_cmd[i]:
            no_msg.append(no_cmd[i])
            no_msg.append(no_cmd[i+1])
            indexes_to_remove.append(i)
            indexes_to_remove.append(i+1)
        if no_cmd[i] in conv_table:
            no_msg.append(no_cmd[i])
            indexes_to_remove.append(i)
    # Pop indexes we don't want and remove from final message
    no_cmd = no_cmd[len(indexes_to_remove):]

    # Set msg as option
    msg = no_cmd
    custom_eye = ' '
    custom_tongue = ' '
    output = [0]

    # Parse flags
    for i in range(0, len(no_msg)):
        if no_msg[i] == '0':
            pass
        else:
            if '-i' in no_msg[i]:
                if len(no_msg[i+1]) > 1:
                    return "Error: Custom character cannot be more than 1 char"
                custom_eye = no_msg[i+1]
                no_msg[i+1] = '0'
                no_msg[i] = '0'
            if '-e' in no_msg[i]:
                if len(no_msg[i+1]) > 1:
                    return "Error: Custom character cannot be more than 1 char"
                custom_tongue = no_msg[i+1]
                no_msg[i+1] = '0'
                no_msg[i] = '0'
            if no_msg[i] in conv_table:
                output[0] = output[0] | conv_table[no_msg[i]]
                no_msg[i] = '0'
    output.append(custom_eye)
    output.append(custom_tongue)
    output.append(msg)
    return output

# Create message from message
def messageEngine(options):
    msg = options[3]
    flag = options[0]
    wrap_len = 40

    # Check word wrap option
    if (flag & FLAG_N):
        wrap_len = 0

    # Render message
    msg_string = ' '.join(msg)
    message_array = []
    if wrap_len == 0 or len(msg_string) <= wrap_len:
        # If message is not wrapped
        middle = "< " + ' '.join(msg) + " >"
        msg_len = len(middle)
        top = ["-" for x in range(msg_len-2)]
        bot = ["-" for x in range(msg_len-2)]
        top = " " + ''.join(top) + " "
        bot = " " + ''.join(bot) + " "
        message_array.append(list(top))
        message_array.append(list(middle))
        message_array.append(list(bot))
    else:
        # If message is wrapped at wrap_length
        msg_len = len(msg_string)
        # Find required empty space for message
        div = int(msg_len/40) + 1
        diff = (div * 40) - msg_len
        # Split message into characters
        split_msg = list(msg_string)
        # Insert differential as whitespace
        for i in range(0, diff):
            split_msg.append(' ')
        message_body_array = []
        total_step = 0
        step = 0
        temp_arr = []
        # Break message into chunks
        while True:
            # Break if total length hits the message length
            if total_step == len(split_msg) - 1:
                break
            # Continue until the 39th step before wrapping
            if step == 39:
                temp_arr.append(split_msg[total_step])
                if len(message_body_array) != 0:
                    temp_arr.append(' ')
                message_body_array.append(''.join(temp_arr))
                temp_arr = []
                step = 0
            else:
                temp_arr.append(split_msg[total_step])
            step += 1
            total_step += 1
        # Format messsage
        border = ["-" for x in range(0,42)]
        if len(message_body_array) == 2:
            middle1 = "/ " + message_body_array[0] + " \\"
            middle2 = "\ " + message_body_array[1] + " /"
            top = " " + ''.join(border) + " "
            bot = " " + ''.join(border) + " "
            message_array.append(list(top))
            message_array.append(list(middle1))
            message_array.append(list(middle2))
            message_array.append(list(bot))
        else:
            middle_arr = []
            for i in range(0, len(message_body_array)):
                middle_arr.append("| " + message_body_array[i] + " |")
            top = "+" + ''.join(border) + "+"
            bot = "+" + ''.join(border) + "+"
            message_array.append(list(top))
            for item in middle_arr:
                message_array.append(list(item))
            message_array.append(list(bot))
    return message_array

# Create image from array
def imageEngine(message, img_input, options):

    # Gather metadata
    metadata = img_input[-3:]
    img_array = img_input[:-3]
    msg_array = message
    eye_char = options[1]
    tongue_char = options[2]
    flag = options[0]

    # Gather eye (X,Y) from metadata
    i_right = metadata[0]
    i_left = metadata[1]
    # Gather tongue (X,Y) from metadata
    tongue = metadata[2]

    # If custom eye flag is inactive
    if eye_char == ' ':
        # Gather eye flags and replace
        # Done this way so only 1 flag can be active at a time
        if(flag & FLAG_b):
            img_array[i_right[0]][i_right[1]] = "="
            img_array[i_left[0]][i_left[1]] = "="
        elif(flag & FLAG_d):
            img_array[i_right[0]][i_right[1]] = "x"
            img_array[i_left[0]][i_left[1]] = "x"
            if tongue[0] !=0 and tongue[1] != 0:
                img_array[tongue[0]][tongue[1]] = "U"
        elif(flag & FLAG_g):
            img_array[i_right[0]][i_right[1]] = "$"
            img_array[i_left[0]][i_left[1]] = "$"
        elif(flag & FLAG_p):
            img_array[i_right[0]][i_right[1]] = "@"
            img_array[i_left[0]][i_left[1]] = "@"
        elif(flag & FLAG_t):
            img_array[i_right[0]][i_right[1]] = "-"
            img_array[i_left[0]][i_left[1]] = "-"
        elif(flag & FLAG_w):
            img_array[i_right[0]][i_right[1]] = "O"
            img_array[i_left[0]][i_left[1]] = "O"
    else:
    # Overrides all other flags if custom eye is active
        img_array[i_right[0]][i_right[1]] = eye_char
        img_array[i_left[0]][i_left[1]] = eye_char

    # If custom tongue flag is active
    if tongue_char != ' ':
        img_array[tongue[0]][tongue[1]] = tongue_char

    # Get image height
    img_height = len(img_array)
    msg_height = len(msg_array)

    # Initialize reponse block
    response_string = "```\n"

    # Print the message
    for i in range(0, msg_height):
        line = ''.join(msg_array[i])
        response_string = response_string + line + '\n'

    # Add an additional line break
    response_string = response_string + '\n'

    # Print the image
    for i in range(0, img_height):
        line = ''.join(img_array[i])
        response_string = response_string + line + '\n'

    # Close the block
    response_string = response_string + '\n```'

    return response_string
