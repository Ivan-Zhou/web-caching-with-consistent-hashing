import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time


HEARTBEAT_TIME = 1

def on_open(ws):
    def run(*args):
        while True:
            time.sleep(HEARTBEAT_TIME)
            ws.send("Ping")

    thread.start_new_thread(run, ())
def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


if __name__ == "__main__":
    from utils import get_master_address
    master_address = get_master_address()
    SERVERIP = "ws://" + master_address["host"]    # local host, just for testing
    HBPORT = master_address["port"]            # an arbitrary UDP port
    address = SERVERIP + ":" + str(HBPORT)
    print(address)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(address,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
