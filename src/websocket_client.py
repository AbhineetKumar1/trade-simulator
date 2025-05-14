import websocket, json, threading, time

class WebSocketClient:
    def __init__(self, on_tick, on_status_change):
        self.url = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
        self.on_tick = on_tick
        self.on_status_change = on_status_change

    def run_forever(self):
        while True:
            try:
                self.ws = websocket.WebSocketApp(self.url,
                    on_open=self.on_open,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close)
                self.ws.run_forever()
            except Exception as e:
                print("[Reconnect Error]", e)
                self.on_status_change("reconnecting")
                time.sleep(3)

    def on_open(self, ws):
        print("[WebSocket] Connected")
        self.on_status_change("connected")

    def on_message(self, ws, message):
        start = time.time()
        data = json.loads(message)
        latency = (time.time() - start) * 1000
        self.on_tick(data, latency)

    def on_error(self, ws, error):
        print("[WebSocket Error]", error)
        self.on_status_change("reconnecting")

    def on_close(self, ws, close_status_code, close_msg):
        print("[WebSocket Closed]")
        self.on_status_change("disconnected")
