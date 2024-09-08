from nextcord.ext import commands
import nextcord

class Purger(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot: commands.Bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int):
        """Purges a specified number of messages in the channel."""
        
        # Ensure the number is a positive integer
        if amount <= 0:
            await ctx.send("Please specify a positive number of messages to purge.")
            return

        # Perform the purge
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"Successfully purged {len(deleted)} messages.", delete_after=5)

def setup(bot: commands.Bot):
    bot.add_cog(Purger(bot))
