#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Two-Tone Receive
# Author: esteban
# GNU Radio version: 3.10.10.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio import soapy
from gnuradio.fft import window  # Add this line for window functions
import two_tone_recieve_epy_block_0 as epy_block_0  # embedded python block
import two_tone_recieve_epy_block_1 as epy_block_1  # embedded python block
import two_tone_recieve_epy_block_2 as epy_block_2  # embedded python block
import time

class two_tone_receive(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Two-Tone Receive")

        ##################################################
        # Variables
        ##################################################
        self.transition_bw = transition_bw = 30e6
        self.tone = tone = 0
        self.samp_rate = samp_rate = 5e6
        self.decimation = decimation = 1

        ##################################################
        # Blocks
        ##################################################
        self.soapy_limesdr_source_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']
        self.soapy_limesdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_source_0.set_bandwidth(0, 0)
        self.soapy_limesdr_source_0.set_frequency(0, 420e6)
        self.soapy_limesdr_source_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_source_0.set_gain(0, min(max(40.0, -12.0), 61.0))
        
        self.soapy_limesdr_sink_0 = None
        self.soapy_limesdr_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_sink_0.set_bandwidth(0, 0.0)
        self.soapy_limesdr_sink_0.set_frequency(0, 435e6)
        self.soapy_limesdr_sink_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_sink_0.set_gain(0, min(max(20.0, -12.0), 64.0))

        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, firdes.low_pass(1, samp_rate, 2.1e6, 1e3), (-430e6), samp_rate)
        self.epy_block_2 = epy_block_2.blk(default_value=1)
        self.epy_block_1 = epy_block_1.blk(default_value=1)
        self.epy_block_0 = epy_block_0.blk(threshold=.01)

        self.blocks_rms_xx_1 = blocks.rms_cf(0.0001)
        self.blocks_rms_xx_0 = blocks.rms_cf(0.0001)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.band_pass_filter_1 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                1.95e6,
                2.05e6,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                .95e6,
                1.05e6,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 2e6, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1e6, 1, 0, 0)
        self.probe = blocks.probe_signal_f()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'out'), (self.epy_block_1, 'in'))
        self.msg_connect((self.epy_block_0, 'out'), (self.epy_block_2, 'in'))
        self.connect((self.analog_sig_source_x_0, 0), (self.epy_block_1, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.epy_block_2, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_rms_xx_0, 0))
        self.connect((self.band_pass_filter_1, 0), (self.blocks_rms_xx_1, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.soapy_limesdr_sink_0, 0))
        self.connect((self.blocks_rms_xx_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_rms_xx_1, 0), (self.epy_block_0, 1))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.band_pass_filter_1, 0))
        self.connect((self.soapy_limesdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.epy_block_2, 0), (self.blocks_add_xx_0, 1))
        self.null_sink = blocks.null_sink(gr.sizeof_float)
        self.connect((self.epy_block_0, 0), (self.null_sink, 0))
        self.connect((self.epy_block_0, 0), (self.probe, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, .95e6, 1.05e6, 1000, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_1.set_taps(firdes.band_pass(1, self.samp_rate, 1.95e6, 2.05e6, 1000, window.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.samp_rate, 2.1e6, 1e3))
        self.soapy_limesdr_sink_0.set_sample_rate(0, self.samp_rate)
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)


def main(top_block_cls=two_tone_receive, options=None):
    tb = top_block_cls()
    tb.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tb.stop()
        tb.wait()


if __name__ == '__main__':
    main()
