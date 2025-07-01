import asyncio
import websockets
import os
import time

TEMPLATE_DIR = "app/templates"  # Directorio raíz a vigilar
PORT = 8765

connected = set()
last_mtimes = {}

def get_all_template_files():
    html_files = []
    for root, _, files in os.walk(TEMPLATE_DIR):
        for f in files:
            if f.endswith(".html"):
                html_files.append(os.path.join(root, f))
    return html_files

def scan_for_changes():
    global last_mtimes
    changed = False
    files = get_all_template_files()
    for file in files:
        try:
            mtime = os.path.getmtime(file)
            if file not in last_mtimes or last_mtimes[file] != mtime:
                last_mtimes[file] = mtime
                changed = True
        except FileNotFoundError:
            continue
    return changed

async def notify_reload():
    while True:
        await asyncio.sleep(1)
        if scan_for_changes():
            print("🔄 Cambio detectado en templates. Recargando navegadores...")
            await asyncio.gather(*[ws.send("reload") for ws in connected])

async def handler(websocket):
    print("🧠 Cliente conectado")
    connected.add(websocket)
    try:
        async for _ in websocket:
            pass
    except:
        pass
    finally:
        print("❌ Cliente desconectado")
        connected.remove(websocket)

async def main():
    server = await websockets.serve(handler, "0.0.0.0", PORT)
    print(f"📡 Servidor WebSocket escuchando en ws://0.0.0.0:{PORT}")
    await notify_reload()

if __name__ == "__main__":
    asyncio.run(main())
