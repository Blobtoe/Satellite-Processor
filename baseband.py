from gnuradio import blocks, gr, analog
from gnuradio.filter import firdes
import os


class bandpass(gr.top_block):

    def __init__(self, input_file, input_rate, offset, filter_width, output_file):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Parameters
        ##################################################
        self.filter_width = filter_width
        self.input_file = input_file
        self.input_rate = input_rate
        self.offset = offset
        self.output_file = output_file

        ##################################################
        # Blocks
        ##################################################
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                input_rate,
                filter_width/2,
                20000,
                firdes.WIN_HAMMING,
                6.76))
        self.blocks_wavfile_source_0 = blocks.wavfile_source(input_file, False)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(output_file, 2, input_rate, 16)
        self.blocks_rotator_cc_0 = blocks.rotator_cc(2*3.14159*offset / input_rate)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_wavfile_sink_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_rotator_cc_0, 0))
        self.connect((self.blocks_rotator_cc_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_float_to_complex_0, 1))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_float_0, 0))

class fm_demodulator(gr.top_block):

    def __init__(self, input_file='', input_rate=1, output_file=''):
        gr.top_block.__init__(self, "Fm Demodulator")

        ##################################################
        # Parameters
        ##################################################
        self.input_file = input_file
        self.input_rate = input_rate
        self.output_file = output_file

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 750000
        self.decim = decim = 1
        self.audio_filter_bw = audio_filter_bw = 15000
        self.audio_decim = audio_decim = 4

        ##################################################
        # Blocks
        ##################################################
        self.blocks_wavfile_source_0 = blocks.wavfile_source(input_file, False)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(output_file, 1, int(samp_rate/decim/audio_decim), 16)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=input_rate/decim,
        	audio_decim=audio_decim,
        	deviation=75000,
        	audio_pass=audio_filter_bw,
        	audio_stop=audio_filter_bw+1000,
        	gain=1.0,
        	tau=0,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.analog_fm_demod_cf_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_float_to_complex_0, 1))

def record(center_frequency, bandwidth, duration):
    os.system(f"timeout {duration} satdump-recorder sdr_config.json {bandwidth} {center_frequency/1000000} i16 recording.raw")
    os.system(f"sox -traw -es- c2 -b16 -r{bandwidth} recording.raw recording.wav")