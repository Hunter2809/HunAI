from __future__ import annotations

from asyncio import sleep
from disnake.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.hunai import HunAI


class Tasks(commands.Cog):
    def __init__(me, bot: HunAI) -> None:
        load_dotenv()
        me.bot = bot
        me.set_bot_gender.start()
        me.update_db.start()

    @tasks.loop(minutes=15)
    async def update_db(me):
        ai = me.bot.ai_session
        session = ai.db
        latest_users = ai.get_all_info()
        session.delete_many({})
        users = [dict([*user]) for user in latest_users]
        ids = (await session.insert_many(users)).inserted_ids
        print(
            f"Updated the db for {len(ids)} users at {datetime.now()}. User IDs updated: {ids}"
        )

    @update_db.before_loop
    async def before_updating_db(me):
        await me.bot.wait_until_ready()
        await sleep(10 * 60)

    @tasks.loop(minutes=3)
    async def set_bot_gender(me):
        ai = me.bot.ai_session
        users = ai.get_all_info()
        for user in users:
            if user.get_predicate("botgender") is None:
                user.set_predicate("botgender", user.get_predicate("gender") or "male")


def setup(bot: HunAI):
    bot.add_cog(Tasks(bot))
