import numpy as np
from gnuradio import gr
import pmt
import os

class blk(gr.sync_block):  
    """Embedded Python Block for detecting two specific tones"""

    def __init__(self, threshold=0.1, flag_file="/tmp/tone_detected.flag"):  
        gr.sync_block.__init__(
            self,
            name='detect_two_tone',  
            in_sig=[np.float32, np.float32],
            out_sig=[np.float32]  
        )
        self.threshold = threshold
        self.flag_file = flag_file
        self.message_port_register_out(pmt.intern("out"))  # Register the output message port

    def work(self, input_items, output_items):
        """Check if both tones are present"""
        rms_431 = input_items[0]
        rms_432 = input_items[1]
        out = output_items[0]

        # Check if the RMS values exceed the threshold
        if np.mean(rms_431) > self.threshold and np.mean(rms_432) > self.threshold:
            tone_value = 1  # Detected the correct combination
        else:
            tone_value = 0  # Did not detect the correct combination

        # Send a PMT message to update the flag
        self.message_port_pub(pmt.intern("out"), pmt.from_long(tone_value))

        # Pass the value to the output for other blocks
        out[:] = float(tone_value)

        # Write the tone_value to a file for higher-level Python code to read
        with open(self.flag_file, 'w') as f:
            f.write(str(tone_value))

        return len(output_items[0])
