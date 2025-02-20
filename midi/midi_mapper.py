import mido

class MIDIMapper:
    def __init__(self):
        self.mappings = {}
        self.in_port = mido.open_input('MIDIIN2')
        self.out_port = mido.open_output('MIDIOUT2')

    def map_control(self, cc_number, action):
        self.mappings[cc_number] = action

    def start_listening(self):
        print("MIDI listener active...")
        for msg in self.in_port:
            if msg.type == 'control_change':
                action = self.mappings.get(msg.control)
                if action: self._handle_action(action, msg.value)

    def _handle_action(self, action, value):
        if action == 'adjust_bpm':
            scaled_bpm = int((value / 127) * 60 + 60)
            print(f"Setting BPM to {scaled_bpm}")