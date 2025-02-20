import socket


class SeratoIntegration:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 50001
        self.sock = None
        self._initialize_osc()

    def _initialize_osc(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("Connected to Serato.")
        except Exception as e:
            print(f"Failed to connect to Serato: {e}")

    def load_track_to_deck(self, deck, file_path):
        """
        Load a track to a specific deck (1 or 2).
        """
        if deck not in [1, 2]:
            raise ValueError("Deck must be 1 or 2.")

        message = f"/load_track,{deck},{file_path}"
        self.sock.sendto(message.encode(), (self.host, self.port))
        print(f"Loaded {file_path} to Deck {deck}.")

    def sync_bpm(self, deck, bpm):
        """
        Sync the BPM of a deck to a specific value.
        """
        message = f"/sync_bpm,{deck},{bpm}"
        self.sock.sendto(message.encode(), (self.host, self.port))
        print(f"Set Deck {deck} BPM to {bpm}.")

    def sync_key(self, deck, key):
        """
        Sync the key of a deck to a specific value.
        """
        message = f"/sync_key,{deck},{key}"
        self.sock.sendto(message.encode(), (self.host, self.port))
        print(f"Set Deck {deck} key to {key}.")

    def close(self):
        self.sock.close()