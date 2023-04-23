# Rooms

A stupid simple websocket service.

## About

Created because, sometimes, I want a very stupid simple websockets endpoint
to test stuff. All messages are sent to everyone connected to the same room and
that is it. Use as you will :)

## Usage

There is one thing you need to do: choose a room name:

```bash
websocat wss://rooms.jmeyer.dev/my-cool-room-name
```

## Development

Not much to talk about it here. I simply use an in memory storage to save the
connections using [Broadcaster][1]. 

```bash
pip install -r requirements.txt
uvicorn handler:app --reload
```

[1]: https://github.com/encode/broadcaster