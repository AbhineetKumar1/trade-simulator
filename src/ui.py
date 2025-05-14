import tkinter as tk
from tkinter import ttk
from websocket_client import WebSocketClient
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models import estimate_slippage, estimate_fees, estimate_market_impact
import threading, time

class TradeSimulatorUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Trade Simulator")
        self.geometry("1000x600")

        self.ws_status = tk.StringVar(value="🔴 Disconnected")
        self.latency_history, self.slippage_history, self.netcost_history = [], [], []
        self.timestamps = []

        self.create_widgets()
        self.websocket = WebSocketClient(self.process_tick, self.update_ws_status)
        threading.Thread(target=self.websocket.run_forever, daemon=True).start()

    def create_widgets(self):
        # Input Panel
        input_frame = tk.Frame(self, width=200)
        input_frame.pack(side="left", fill="y", padx=10, pady=10)
        tk.Label(input_frame, text="Order Quantity (USD):").pack()
        self.qty_entry = tk.Entry(input_frame)
        self.qty_entry.insert(0, "100")
        self.qty_entry.pack()

        self.status_label = tk.Label(input_frame, textvariable=self.ws_status, fg="red")
        self.status_label.pack(pady=10)

        # Output Panel + Chart
        right_frame = tk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.output_text = tk.Text(right_frame, height=10)
        self.output_text.pack(fill="x")

        fig, self.axs = plt.subplots(3, 1, figsize=(6, 4))
        fig.tight_layout(pad=2)
        self.chart = FigureCanvasTkAgg(fig, master=right_frame)
        self.chart.get_tk_widget().pack(fill="both", expand=True)

    def process_tick(self, tick, latency_ms):
        try:
            qty = float(self.qty_entry.get())
            slippage = estimate_slippage(tick["asks"], tick["bids"], qty)
            fees = estimate_fees(qty)
            impact = estimate_market_impact(qty)
            net = slippage + fees + impact

            timestamp = time.strftime("%H:%M:%S")
            self.timestamps.append(timestamp)
            self.latency_history.append(latency_ms)
            self.slippage_history.append(slippage)
            self.netcost_history.append(net)

            # Limit data size
            self.timestamps = self.timestamps[-30:]
            self.latency_history = self.latency_history[-30:]
            self.slippage_history = self.slippage_history[-30:]
            self.netcost_history = self.netcost_history[-30:]

            # Update text
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Slippage: {slippage:.4f}\nFees: {fees:.4f}\nImpact: {impact:.4f}\nNet Cost: {net:.4f}\nLatency: {latency_ms:.2f} ms")

            # Update charts
            for ax in self.axs: ax.clear()
            self.axs[0].plot(self.timestamps, self.latency_history, label="Latency (ms)", color="orange")
            self.axs[1].plot(self.timestamps, self.slippage_history, label="Slippage", color="blue")
            self.axs[2].plot(self.timestamps, self.netcost_history, label="Net Cost", color="green")
            for ax in self.axs: ax.legend()
            self.chart.draw()
        except Exception as e:
            print("[Error in process_tick]", e)

    def update_ws_status(self, status):
        if status == "connected":
            self.ws_status.set("🟢 Connected")
            self.status_label.config(fg="green")
        elif status == "reconnecting":
            self.ws_status.set("🟡 Reconnecting...")
            self.status_label.config(fg="orange")
        else:
            self.ws_status.set("🔴 Disconnected")
            self.status_label.config(fg="red")
