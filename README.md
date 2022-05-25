# Grim
## few lib to create fast ping-pong Discord bots

## TODO

* add async support
* add FastAPI-like arguments via type annotations

## Example

```py
import grim

TOKEN = "..."


app = grim.App(TOKEN)


@app.command
def ping(message: grim.Message) -> str:
    """Answer 'pong {username}' to a 'ping' message"""
    return f"pong {message.author.full_name} !"


app.listen()
```
