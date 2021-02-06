import discord
import pandas as pd
from config import prefix, sheetsFile, \
    worksheetName, imageWebBase, typeName, embedColor
from auth import discord_token
from discord.ext.commands import Bot
from tools import login, find_row_in_dataframe, render_image

client = Bot(prefix)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.command(pass_context=True)
async def stats(ctx, query):

    gc = login()

    wks = gc.open(sheetsFile)
    worksheet = wks.worksheet(worksheetName)
    data_frame = pd.DataFrame(worksheet.get_all_records())
    found_row = find_row_in_dataframe(query, data_frame, typeName)

    if found_row.empty:
        await ctx.send("There are no entries that match your search.")

    elif len(found_row.index) > 1:
        await ctx.send("Too many results. Please narrow your search.")

    else:
        url_string = render_image(imageWebBase, str(found_row[typeName].item()))

        embed = discord.Embed(title=str(found_row[typeName].item()), color=embedColor)
        embed.set_thumbnail(url=url_string)
        embed.add_field(name="Health", value=str(found_row["Health"].item()), inline=True)
        embed.add_field(name="Stamina", value=str(found_row["Stamina"].item()), inline=True)
        embed.add_field(name="Food", value=str(found_row["Food"].item()), inline=True)
        embed.add_field(name="Weight", value=str(found_row["Weight"].item()), inline=True)
        embed.add_field(name="Melee", value=str(found_row["Melee"].item()), inline=True)

        await ctx.send(embed=embed)

client.run(discord_token)
