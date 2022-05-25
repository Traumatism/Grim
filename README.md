# Grim
## few lib to create fast ping-pong Discord bots

## TODO

* add async support
* gateway keep-alive
* add FastAPI-like arguments via type annotations

## Example

```py
import time

from grim import App, Message
from grim.markdown import bold

TOKEN = "..."


app = App(TOKEN, prefix="!")


@app.command
def job(_):
    yield "task #1 done"
    time.sleep(1)
    yield "task #2 done"
    time.sleep(1)
    yield "task #3 done"


@app.command
def ping(message: Message):
    yield f"pong {message.author.full_name}"


@app.command
def echo(message: Message):
    yield bold(" ".join(message.arguments))


app.listen()


```
