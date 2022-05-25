import grim.bot

TOKEN = "..."


app = grim.bot.App(TOKEN)


@app.command
def ping(message: grim.bot.Message) -> str:
    return f"pong {message.author.full_name} !"


app.listen()
