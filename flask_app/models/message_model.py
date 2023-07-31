from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DB
from flask_app.models import user_model
import datetime


class Message:
    def __init__(self, data):
        self.id = data['id']
        self.sender_id = data['sender_id']
        self.recipient_id = data['recipient_id']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # ------------------------------------------------ SAVE NEW Message
    @classmethod
    def save(cls,data):
        query = """
                INSERT INTO messages (sender_id, recipient_id, message) 
                VALUES (%(sender_id)s, %(recipient_id)s, %(message)s);
                """
        return connectToMySQL(DB).query_db(query, data)
    
    # ------------------------------------------------ Get # of messages
    @classmethod
    def num_of_sent(cls,data):
        query = """
                SELECT COUNT(*) as num FROM messages m 
                WHERE m.sender_id = %(id)s GROUP BY (m.sender_id); 
                """
        results = connectToMySQL(DB).query_db(query, data)
        return results[0]['num']

    # ------------------------------------------------ Get message by id
    @classmethod
    def get_by_id(cls, data):
        query = """
                SELECT * FROM messages 
                WHERE id = %(id)s; 
                """
        results = connectToMySQL(DB).query_db(query, data)
        message = cls(results[0])
        print(message.recipient_id)
        return message


    # ------------------------------------------------ GET ALL messages for user
    @classmethod
    def get_all_for_user(cls, data):
        query = """
                SELECT * FROM messages m 
                LEFT JOIN users as sb ON m.sender_id = sb.id
                LEFT JOIN users as r ON m.recipient_id = r.id
                WHERE r.id = %(id)s;
                """
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            print(results)
            all_messages = []
            for row in results:
                message = cls(row)
                sb_user = {
                    **row,
                    'id': row['sb.id'],
                    'created_at': row['sb.created_at'],
                    'updated_at': row['sb.updated_at']
                }
                message.sender = user_model.User(sb_user)
                message.created_at = pretty_date(message.created_at)
                all_messages.append(message)
            return all_messages
        return False

    # ------------------------------------------ DESTROY
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)

    





    @staticmethod
    def validation(data):
        is_valid = True
        # -----------------------------------------First Name
        if len(data['message']) < 1 :
            is_valid = False
            flash('Invalid First Name!', 'message')
        elif len(data['message']) < 2 :
            is_valid = False
            flash('Invalid First Name! * must be 2 characters long', 'message')


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = 0
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff // 30) + " months ago"
    return str(day_diff // 365) + " years ago"
