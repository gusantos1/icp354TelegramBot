from __future__ import annotations
import re
from time import sleep
from datetime import datetime
from src.app import bot, CONNECTION, QUERIES, TEXT
from src.datainfo import generic_info


def greet() -> str:
    """
        Retorna um cumprimento de acordo com o horário nacional UTC-3.
    """
    hour = datetime.now().hour
    if hour < 12:
        return "Bom dia"
    if hour > 18:
        return "Boa noite"
    return "Boa tarde"


def validate_fake(text: str) -> bool | int:
    """
        Valida se um texto contém a palavra `fake` seguido do número correspondente ao id da fakenews.
    Ex:
        fake10 -> 10
        feike5 -> False
    """
    regex = r"[fake]"
    try:
        if "fake" in text:
            rework = int(re.sub(regex, "", text))
            return rework
        return False
    except ValueError:
        return False


def show_options(connecion) -> str:
    query = QUERIES["show_options"]
    with connecion:
        response = connecion.execute(query).fetchall()
    format_resp = [f"• *Fake{item[0]}* - {item[1]}" for item in response]
    return "\n".join(format_resp)


@bot.message_handler(func=lambda anything: True)
def response_message(message) -> int:
    user, msg = generic_info(message)
    id = validate_fake(msg.text.lower())
    if not id:
        ## greet message
        bot.send_message(
            msg.id,
            f'{greet()}, {user.firstname}.🤖\n{TEXT["greet"]}',
            parse_mode="Markdown",
        )
        sleep(2)

        ## show options
        options = show_options(CONNECTION)
        bot.send_message(
            msg.id,
            f'{TEXT["options"]}\n{TEXT["example"]}\n\n{options}',
            parse_mode="Markdown",
        )
        return 1

    query = f'{QUERIES["info_fake"]} id == {id}'
    with CONNECTION:
        cur = CONNECTION.cursor()
        response = cur.execute(query).fetchone()
    sleep(1.5)
    bot.reply_to(message, response)
    return 2


@bot.message_handler(commands=["info"])
def response_info(message: str) -> bool:
    bot.reply_to(message, TEXT["info"])
    return True
