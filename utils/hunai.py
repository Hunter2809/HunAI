from disnake import Intents
from disnake.ext import commands
from AI.ai import AI


class HunAI(commands.Bot):
    def __init__(me):
        super().__init__(
            command_prefix=["hun", "Hun"],
            intents=Intents(
                members=True,
                message_content=True,
                guilds=True,
                messages=True,
            ),
        )
        me.ai_session = AI()

    def on_ready(me):
        print(
            f"The bot has started up with {len(me.users)} users from {len(me.guilds)} guilds chatting with me!"
        )
