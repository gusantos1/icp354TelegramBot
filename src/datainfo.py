from dataclasses import dataclass


@dataclass
class InfoUser:
    id: int
    firstname: str
    username: str
    isbot: bool


@dataclass
class InfoMsg:
    id: int
    timestamp: int
    text: str


def generic_info(message):
    user = InfoUser(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username,
        message.from_user.is_bot,
    )
    msg = InfoMsg(message.chat.id, message.date, message.text)
    return user, msg
