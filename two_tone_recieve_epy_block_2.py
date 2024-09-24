import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):  
    """Custom Block to multiply complex signal source by a message-controlled value"""

    def __init__(self, default_value=1.0):  
        gr.sync_block.__init__(
            self,
            name='amplitude_control_complex',  
            in_sig=[np.complex64],  # Complex input
            out_sig=[np.complex64]  # Complex output
        )
        self.amplitude = default_value  # Default amplitude value
        self.message_port_register_in(pmt.intern("in"))  # Register message input
        self.set_msg_handler(pmt.intern("in"), self.handle_msg)  # Set handler for incoming messages

    def handle_msg(self, msg):
        """Handle incoming messages to update amplitude"""
        # Parse the incoming PMT long integer message
        msg_value = pmt.to_long(msg)

        # Invert the amplitude based on message value: amplitude is 1.0 when message is 0, and 0.0 when message is 1
        if msg_value == 1:
            self.amplitude = 0.0  # Inverted logic: message 1 means amplitude 0
        elif msg_value == 0:
            self.amplitude = 1.0  # Inverted logic: message 0 means amplitude 1

    def work(self, input_items, output_items):
        """Multiply the complex input signal by the amplitude"""
        signal = input_items[0]
        output_items[0][:] = self.amplitude * signal  # Apply amplitude to the complex signal

        return len(output_items[0])
