import mido
from mido import MidiFile, MidiTrack, Message

class TraktorIntegration:
    def __init__(self):
        self.output_port = None
        self.input_port = None
        self._initialize_midi()

    def _initialize_midi(self):
        try:
            self.output_port = mido.open_output('Traktor Virtual Output')
            self.input_port = mido.open_input('Traktor Virtual Input')
            print("Connected to Traktor.")
        except Exception as e:
            print(f"Failed to connect to Traktor: {e}")

    def load_track_to_deck(self, deck, file_path):
        """
        Load a track to a specific deck (1 or 2).
        """
        if deck not in [1, 2]:
            raise ValueError("Deck must be 1 or 2.")

        msg = Message('program_change', program=deck, channel=0)
        self.output_port.send(msg)
        print(f"Loaded {file_path} to Deck {deck}.")

    def sync_bpm(self, deck, bpm):
        """
        Sync the BPM of a deck to a specific value.
        """
        msg = Message('control_change', control=deck, value=int(bpm), channel=1)
        self.output_port.send(msg)
        print(f"Set Deck {deck} BPM to {bpm}.")

    def sync_key(self, deck, key):
        """
        Sync the key of a deck to a specific value.
        """
        msg = Message('control_change', control=deck + 2, value=key, channel=1)
        self.output_port.send(msg)
        print(f"Set Deck {deck} key to {key}.")

    def close(self):
        self.output_port.close()
        self.input_port.close()