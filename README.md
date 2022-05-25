# Grim
## few lib to create fast ping-pong Discord bots

## TODO

* add async support
* add FastAPI-like arguments via type annotations

## Example

```py
from grim import App, Message

TOKEN = "..."


app = App(TOKEN, prefix="!")


@app.command
def ping(message: Message) -> str:
    return f"pong {message.author.full_name} !"


app.listen()
```
