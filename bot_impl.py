# -*- coding: utf-8 -*-

import telebot
import config
from Utils import *

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["help"])
def get_help(message):
    user_id = data.register_user(message)
    bot.send_message(user_id, """Here are my commands:
    /add -- for adding new spending
    /look -- look to current container
    /history -- history of containers
    /set -- choose current container(from ones in history)
    /reset -- reset current container(also saves current to history)
    Also you can type any of these commands without slash
    E.g. add <category> <amount>""")


@bot.message_handler(commands=["add"])
def add(message):
    user_id = data.register_user(message)
    words = [word for word in message.text.split(sep=" ") if word != ""]
    if len(words) != 3:  # <command> <category> <amount>
        bot.send_message(user_id, "Usage: [/]add <category> <money amount>")
    else:
        cat = words[1]
        amount = words[2]
        result = data.get_user_container(user_id).add(cat, amount)
        bot.send_message(user_id, result)


@bot.message_handler(commands=["remove"])
def remove(message):
    user_id = data.register_user(message)
    words = [word for word in message.text.split(sep=" ") if word != ""]
    if len(words) != 2:  # <command> <category>
        bot.send_message(user_id, "Usage: [/]remove <category>")
        return
    result = data.get_user_container(user_id).remove(words[1])
    bot.send_message(user_id, result)


@bot.message_handler(commands=["look"])
def look(message):
    user_id = data.register_user(message)
    bot.send_message(user_id,  data.get_user_container(user_id).to_string())


@bot.message_handler(commands=["history"])
def get_history(message):
    user_id = data.register_user(message)
    history = data.get_user_history(user_id)
    result = ""
    for i in range(0, len(history)):
        result += "### " + str(i) + " ###\n" + history[i].to_string() + "\n\n"
    bot.send_message(user_id, result)


@bot.message_handler(commands=["set"])
def set_current(message):
    user_id = data.register_user(message)
    history = data.get_user_history(user_id)
    words = message.text.split(sep=" ")
    if len(words) != 2:  # <command> <number>
        bot.send_message(user_id, "Usage: <index of a container>")
        return

    if int(words[1]) >= len(history) | int(words[1]) < 0:
        bot.send_message(user_id, "Incorrect index")
        return

    history.save(data.get_user_container(user_id))
    new_container = history[int(words[1])]
    data.set_user_container(user_id, new_container)
    bot.send_message(user_id, "Set as current:\n\t" +
                     "\n\t".join(new_container.to_string().split(sep="\n")))


@bot.message_handler(commands=["reset"])
def reset_current(message):
    user_id = message.chat.id
    data.get_user_history(user_id).save(data.get_user_container(user_id))
    data.set_user_container(user_id, Container())
    bot.send_message(user_id, "Reset current")


@bot.message_handler(commands=["getid"])
def getid(message):
    bot.send_message(message.chat.id, str(message.chat.id))


@bot.message_handler(commands=["dump"])
def dump(message):
    data.dump_nodes()
    bot.send_message(message.chat.id, "Dumped " + ", ".join(data.users.values()))


@bot.message_handler(content_types=["text"])
def func(message):
    cmd = str(message.text).lower().split(" ")[0]
    if cmd in cmd_alias:
        cmd_alias[cmd](message)
    else:
        bot.send_message(message.chat.id, "Could not recognize your request\nPrint help for list of commands")


if __name__ == "__main__":
    data = Data()
    data.read_nodes()
    cmd_alias = {"add": add, "look": look, "history": get_history, "help": get_help,
                 "set": set_current, "reset": reset_current,
                 "l": look, "h": get_history}
    bot.polling(none_stop=True)
