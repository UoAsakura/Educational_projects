import asyncio
import websockets


async def listen():
    uri = "ws://localhost:7665"
    async with websockets.connect(uri) as websocket:
        print("Подключено к серверу. Ожидание сообщений...")

        while True:
            # Получение сообщения от сервера
            message = await websocket.recv()
            print(f"Получено сообщение от сервера: {message}")

            # Отправка ответа серверу (опционально)
            response = f"Клиент получил: {message}"
            await websocket.send(response)


# Запуск клиента
asyncio.get_event_loop().run_until_complete(listen())

#!/usr/bin/env python

# """Echo server using the asyncio API."""
#
# import asyncio
# from websockets.asyncio.server import serve
#
#
# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send(message)
#
#
# async def main():
#     async with serve(echo, "localhost", 7654) as server:
#         await server.serve_forever()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())