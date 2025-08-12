from enum import Enum


class MessageType(Enum):
    TEXT = 'text'
    IMAGE = 'image'
    VOICE = 'voice'
    VIDEO = 'video'


class Sender(Enum):
    BOT = 'bot'
    USER = 'user'
