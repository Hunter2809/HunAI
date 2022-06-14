import sys
from asyncio import new_event_loop, set_event_loop
from datetime import datetime

from AI.ai import AI

logs = open("logs.txt", "a+")
logs.write(f"\n\n{datetime.now()}\n")
sys.stderr = logs
sys.stdout = logs
ai = AI()
loop = new_event_loop()
set_event_loop(loop)
loop.run_until_complete(ai.get_predicates())


async def update_db():
    ai_session = ai
    session = ai_session.db
    latest_users = ai_session.get_all_info()
    session.delete_many({})
    print("Deleted")
    users = [dict([*user]) for user in latest_users]
    await session.insert_many(users)


loop.run_until_complete(update_db())
