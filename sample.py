from grim import App, Message

TOKEN = "..."


app = App(TOKEN, prefix="!")


@app.command
def ping(message: Message) -> str:
    return f"pong {message.author.full_name} !"


app.listen()
