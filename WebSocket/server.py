import asyncio
import websockets


async def send_message(websocket, path):
    while True:
        # Ввод сообщения с консоли
        message = input("Введите сообщение для отправки клиенту: ")

        # Отправка сообщения клиенту
        await websocket.send(message)
        print(f"Сообщение отправлено: {message}")

        # Ожидание ответа от клиента (опционально)
        response = await websocket.recv()
        print(f"Ответ от клиента: {response}")


# Запуск сервера
start_server = websockets.serve(send_message, "localhost", 7665)

print("Сервер запущен на ws://localhost:7665")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


# !/usr/bin/env python

# """Client using the asyncio API."""
#
# import asyncio
# from websockets.asyncio.client import connect
#
#
# async def hello():
#     async with connect("ws://localhost:7654") as websocket:
#         await websocket.send("Hello world!")
#         message = await websocket.recv()
#         print(message)
#
#
# if __name__ == "__main__":
#     asyncio.run(hello())