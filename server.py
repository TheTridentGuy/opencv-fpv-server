"""
server.py
WebSocket FPV server
Copyright (C) 2023  Aiden Bohlander

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import time
import cv2
import asyncio
import websockets
import base64


async def handle_connection(websocket, path):
    """
    Websocket connection handler
    :param websocket: Conected websocket
    :param path: Path of connected websocket
    :return: None
    """
    for frame in get_frames():
        await websocket.send(frame)


def get_frames():
    """
    Generator function that uses cv2 to stream frames to a websocket,
    yielding byte-encoded frames.
    :return: None
    """
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.png', frame)
            frame = base64.b64encode(buffer)
            yield b'data:image/png;base64,' + frame


# Start video capture
camera = cv2.VideoCapture(0)
# Start the server
start_server = websockets.serve(handle_connection, "localhost", 8000)

# Do async stuff
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
