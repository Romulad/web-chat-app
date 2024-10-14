from pymongo.database import Database

from ..app.schemas import UserWithPassword, ChatMessage
from ..app.database import db_collection_names


class BaseTestClass:

    def create_user(self, db:Database, email=""):
        user_data = UserWithPassword(
            email= email if email else "test@gmail.com",
            first_name="Socket user",
            password="mypassword1234"
        )

        user_id = db.get_collection(
            db_collection_names.users
        ).insert_one(
            user_data.model_dump()
        ).inserted_id

        return str(user_id)

    def create_users(self, db:Database):
        user_data = [
            UserWithPassword(
                email="test@gmail.com",
                first_name="Socket user",
                password="mypassword1234"
            ),
            UserWithPassword(
                email="test@gmail22.com",
                first_name="test22",
                password="mypassword1234"
            ),
            UserWithPassword(
                email="test@gmail223.com",
                first_name="test252",
                password="mypassword1234"
            )
        ]

        user_ids = db.get_collection(
            db_collection_names.users
        ).insert_many(
            [user.model_dump() for user in user_data]
        ).inserted_ids

        for user_id in user_ids:
            yield str(user_id)

    def generate_chat_messages(
            self, db:Database, chat_id: str, id1: str, id2: str,
        ):
        msgs = ["hi", "hw doing", "gd ths && yw", "Gd too, ths", "you' quit welm", "okay ):"]
        switch = False

        for msg in msgs:
            data = ChatMessage(
                chat_id=chat_id,
                receiver_id=id1 if switch else id2,
                sender_id=id2 if switch else id1,
                text=msg,
            )
            db.get_collection(
                db_collection_names.chat_messages
            ).insert_one(data.model_dump())
            switch = False if switch else True