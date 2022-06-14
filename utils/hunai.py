from disnake.ext import commands
from AI.ai import AI


class HunAI(commands.Bot):
    def __init__(me):
        super().__init__(["hun", "Hun"])
        me.ai_session = AI()
