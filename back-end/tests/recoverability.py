import asyncio
import websockets
import time


async def test_recoverability():
    uri = "ws://127.0.0.1:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket.")
            await asyncio.sleep(5)  # Simulate server restart or downtime

            print("Simulating server disconnect...")
            await websocket.close()

            # Attempt reconnection
            start_time = time.time()
            while True:
                try:
                    websocket = await websockets.connect(uri)
                    print("Reconnected!")
                    break
                except Exception:
                    await asyncio.sleep(1)  # Wait before trying again
            end_time = time.time()
            reconnection_time = end_time - start_time

            print(f"Reconnection Time: {reconnection_time:.3f} seconds")
            assert reconnection_time <= 10, f"Reconnection took too long: {reconnection_time:.3f} seconds"
    except Exception as e:
        print(f"WebSocket Error: {e}")

asyncio.run(test_recoverability())
