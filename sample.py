import grim

TOKEN = "..."


app = grim.App(TOKEN)


@app.command
def ping(message: grim.Message) -> str:
    return f"pong {message.author.full_name} !"


app.listen()
