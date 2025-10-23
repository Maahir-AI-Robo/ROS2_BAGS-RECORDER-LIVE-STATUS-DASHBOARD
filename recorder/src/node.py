import threading
import time

class RecorderNode:
    def __init__(self):
        self.is_recording = False
        self.is_paused = False
        self.data_buffer = []
        self.lock = threading.Lock()
        
    def initialize(self):
        # Initialize the node, set up subscriptions and other necessary parameters
        print("Initializing RecorderNode...")

    def start_recording(self):
        with self.lock:
            self.is_recording = True
            self.is_paused = False
            print("Recording started.")
            self.data_buffer.clear()
            threading.Thread(target=self._discovery_loop).start()
            threading.Thread(target=self._flush_loop).start()

    def stop_recording(self):
        with self.lock:
            self.is_recording = False
            print("Recording stopped.")

    def pause_recording(self):
        with self.lock:
            if self.is_recording:
                self.is_paused = True
                print("Recording paused.")

    def resume_recording(self):
        with self.lock:
            if self.is_recording and self.is_paused:
                self.is_paused = False
                print("Recording resumed.")

    def _discovery_loop(self):
        while self.is_recording:
            if not self.is_paused:
                # Simulate data discovery
                data = "data"  # Replace with actual data discovery logic
                self._on_message(data)
            time.sleep(1)  # Adjust the frequency of data discovery

    def _flush_loop(self):
        while self.is_recording:
            if not self.is_paused and self.data_buffer:
                # Simulate flushing data to storage
                print("Flushing data:", self.data_buffer)
                self.data_buffer.clear()
            time.sleep(5)  # Adjust the flush frequency

    def _on_message(self, message):
        with self.lock:
            if self.is_recording and not self.is_paused:
                self.data_buffer.append(message)
                print("Message received and stored:", message)