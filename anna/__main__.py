from __future__ import annotations
from os import environ
from typing import Optional
from dotenv import load_dotenv
load_dotenv()
import os
import nextcord
from nextcord import ApplicationError, Game, Intents
from nextcord.ext import application_checks as ac
from nextcord.ext import commands, help_commands, tasks  # type: ignore
import asyncio
from extensions.help_forum.database import Database
import subprocess
from extensions.help_forum.config import DATABASE_PATH

prefix = "a!" if os.getenv("TEST") else "a?" # bot prefix, first value is for when the bot is in test mode, second is the general prefix

class Bot(commands.Bot):
    def __init__(self, db_path: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.db = Database(db_path)
        self.persistent_views_added = False

    async def on_command_error(
        self, context: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.NotOwner):
            await context.send("Only Anna's maintainers can run this command.")
        elif isinstance(error, commands.UserInputError):
            await context.send("User input error.")
        elif isinstance(error, commands.CommandNotFound):
            await context.send("Command not found.")
        elif isinstance(error, commands.errors.DisabledCommand):
            await context.send("This command has been disabled by Anna's maintainers.")
        else:
            await context.send("An error was caught while attempting to run the command.")
            await super().on_command_error(context, error)

    async def on_application_command_error(
        self, interaction: nextcord.Interaction, exception: ApplicationError
    ) -> None:
        if isinstance(exception, ac.ApplicationMissingRole):
            await interaction.send("You must be a staff member to use this command.")
        else:
            await interaction.send("An error was caught while attempting to run the command.")
            await super().on_application_command_error(interaction, exception)

    @commands.Cog.listener()
    async def on_ready(self):
        """ Event triggered when the bot is ready """
        print(f'{self.user} is now online!')
        await self.db.create_tables()

owner_ids = [716306888492318790, 961063229168164864]  # Cutedog and orangc
intents = Intents.all()
intents.message_content = True
intents.members = True

bot = Bot(
    db_path=DATABASE_PATH,
    intents=intents,
    command_prefix=prefix,
    help_command=help_commands.PaginatedHelpCommand(),
    case_insensitive=True,
    owner_ids=owner_ids,
    allowed_mentions=nextcord.AllowedMentions(everyone=False, roles=False, users=True, replied_user=True),
    activity=nextcord.Activity(
        type=nextcord.ActivityType.watching, 
        name="is-a.dev",                      
        assets={"large_image": "is-a-dev"}    
    )
)

# TODO: Remove onami when nextcord 3.0 release
# WARNING: Do not remove this if!
if nextcord.version_info < (3, 0, 0):
    bot.load_extension("onami")
if os.getenv("HASDB"):
    bot.load_extension("extensions.tags_reworked")
    
extensions = ["extensions.help_forum.help_system", "extensions.antihoist", "extensions.fun", "extensions.faq", "extensions.antiphishing", "extensions.testing_functions", "extensions.nonsense", "extensions.dns", "extensions.suggestions", "extensions.delete_response", "extensions.github", "extensions.oneword", "extensions.sender", "extensions.tags", "extensions.purge", "extensions.ping_cutedog"]
for i in extensions:
    bot.load_extension(i)
bot.run(environ["TOKEN"])