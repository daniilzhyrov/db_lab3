from enum import Enum

class Neo4j(Enum):
    HOST = 'neo4j://10.2.14.137:31300'
    USER = 'neo4j'
    PWD = 'f8'

class Redis:
    HOST = '10.2.14.137'
    PORT = 32457
    PASSWORD = 'a-very-complex-password-here'

class Keys:
    USERS_SET = "users"
    ONLINE_USERS = "users_online"
    NEW_MESSAGES_CHANNEL = "new_message_channel"
    SPAM_CHANNEL = "spam_channel"
    LOG_CHANNEL = "log_channel"
    LOG_LIST = "log"
    SPAM_LIST = "spam_list"
    SPAM_COUNTER = "spam_counter"
    MESSAGES_QUEUE = "queue"
    MESSAGE_HASH = "message"
    LAST_MESSAGE_ID = "last_message_id"
    SENT_MESSAGES_LIST = "sent_messages"
    RECEIVED_MESSAGES_LIST = "received_messages"

class UserType:
    ADMIN_USER_LABEL = "admin"
    USER_LABEL = "user"

class MessageState:
    CREATED = 'Created'
    IN_THE_QUEUE = 'In the queue'
    SPAM_CHECK = 'Spam check'
    BLOCKED = 'Blocked'
    SENT = 'Sent'
    DELIVERED = 'Delivered'

class MessageTags(Enum):
    GENERAL = 'General'
    IMPORTANT = 'Important'
    AD = 'Ad'
    SOCIAL = 'Social'
    INFO = 'Info'

class Const:
    ADDED_TO_QUEUE_NOTIFICATION = "8"
    SPAM_DELAY = 0.1