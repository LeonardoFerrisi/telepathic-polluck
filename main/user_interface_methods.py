from termcolor import colored

def dislay_console( label='' ,msg='', color="white"):
    """
    Display a message to console
    """
    label_text = ''
    if label!='':label_text = colored(label, color='yellow') + ": "
    message_contents = label_text + colored(msg, color)
    print(message_contents)

def display_input_console( label='' ,msg='', color="white"):
    """
    Display a message to console and returns input
    """
    label_text = ''
    if label!='':label_text = colored(label, color='yellow') + ": "
    message_contents = label_text + colored(msg, color) + colored(" >> ",color="magenta")

    toReturn = input(message_contents)
    return toReturn



