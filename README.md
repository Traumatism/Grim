# Grim
## few lib to create fast ping-pong Discord bots

## TODO

* add async support
* gateway keep-alive
* add FastAPI-like arguments via type annotations

## Example

```py
from grim import App, Message
from grim.markdown import bold

TOKEN = "..."


app = App(TOKEN, prefix="!")


@app.command
def ping(message: Message) -> str:
    return f"pong {message.author.full_name} !"


@app.command
def echo(message: Message) -> str:
    return bold(" ".join(message.arguments))


app.listen()

```
