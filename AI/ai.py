from __future__ import annotations

from json import load
from os import getenv, path
from typing import TYPE_CHECKING

from aiml import Kernel
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from utils.AIUser import AIUser

if TYPE_CHECKING:
    from disnake import Message
    from typing_extensions import Self as Me


class AI:
    """This class provides access to HunAI's AI response system."""

    def __init__(me) -> None:
        load_dotenv()
        me.kernel = Kernel()
        session = AsyncIOMotorClient(getenv("CONNECTION_STRING"))
        me.db = session["AI"]["Predicates"]
        me.existing_users: list[AIUser] = []

    def learn(me) -> None:
        """This should only be called once on startup. This loads all the bot predicates into the memory"""
        predicates: list[list[str]] = load(open("preds.json"))
        for pred in predicates:
            me.kernel.setBotPredicate(*pred)
        if path.isfile("AI/bot_brain.brn"):
            me.kernel.bootstrap(brainFile="AI/bot_brain.brn")
        else:
            me.kernel.bootstrap(learnFiles="AI/std-startup.xml", commands="LOAD AIML B")
            me.kernel.saveBrain("AI/bot_brain.brn")

    async def get_predicates(me) -> Me:
        """Fetches the user predicates from MongoDB and appends those to the internal users list"""
        async for doc in me.db.find({}):
            user = AIUser(doc)
            me.existing_users.append(user)
        me.load_preds()
        return me

    def load_preds(me) -> None:
        """Loads all the user predicates into memory"""
        for user in me.existing_users:
            for name, value in user:
                if name not in ("_inputHistory", "_outputHistory", "_inputStack"):
                    me.kernel.setPredicate(name, value, str(user))

    def get_response(me, msg: Message) -> str:
        """Gets a response to a message object"""
        ques = msg.content
        author = str(msg.author.id)
        answer: str = me.kernel.respond(ques, author)
        answer = " ".join(answer.split())  # To remove unwanted spaces
        if len(answer) > 2000:
            answer = answer[:2000]
        return answer

    def get_all_info(me) -> list[AIUser]:
        """Gets the list of all the AIUser objects the bot has"""
        info = me.kernel.getSessionData()
        del info["_global"]
        user_list = []
        for user_id in info:
            user_dict = {"_id": user_id, **info[user_id]}
            user_list.append(user_dict)
        return [AIUser(info_dict) for info_dict in user_list]

    def get_user_info(me, author: str) -> AIUser:
        """Gets the AI information about a single user"""
        all_info = me.get_all_info()
        user_info = tuple(filter(lambda user: str(user) == author, all_info))[0]
        return user_info
