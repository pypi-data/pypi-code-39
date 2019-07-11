import numpy as np
from collections import deque


class AccelSimModel(object):
    """A simulation model of the signal chain inside the accelerometer tile.

    All calculations are done in fixed point exactly as they are on the tile.
    The results should be directly comparable.

    Args:
        sampling_rate (int): The sampling rate configured for the accelerometer
            chip.
        lowpass (bool): Whether to enable the 2-pole butterworth lowpass
            filter at 330 hz.
    """

    DC_INVPOLES = {
        3200: 5,
        1600: 11,
        800: 23,
        400: 45
    }

    DC_SETTLING = {
        3200: 23576,
        1600: 10716,
        800: 5124,
        400: 2618
    }

    # Measured white noise standard deviation
    NOISE = {
        3200: 4.2,
        1600: 4.2,
        800: 4.2,
        400: 4.2
    }

    # The nominal LSB value of the accelerometer on this tile
    # in units of G's / LSB
    LSB_VALUE = 0.049

    # Store a and b coefficients for a biquad 2nd order
    # lowpass filter
    LOWPASS_COEFFS = {
        3200: [(-73246, 26329), (4654, 9309, 4654)],
        1600: [(-21170, 12457), (14205, 28411, 14205)],
        800: [(81606, 30174), (44329, 88658, 44329)]
    }

    def __init__(self, sampling_rate=3200, lowpass=True, include_noise=True):
        self.dc_invpole = self.DC_INVPOLES[sampling_rate]
        self.dc_settling = self.DC_SETTLING[sampling_rate]
        self.dc_state = None

        self.sampling_rate = sampling_rate
        self.noise = self.NOISE[sampling_rate]
        self.include_noise = include_noise

        self.lowpass = lowpass
        self.lp_a, self.lp_b = self.LOWPASS_COEFFS[sampling_rate]
        self.lp_state = None

    @classmethod
    def _truncate_int(cls, num, size):
        mask16 = 0xFFFF
        mask32 = 0xFFFFFFFF
        mask64 = 0xFFFFFFFFFFFFFFFF

        if size == 16:
            num_mask = num & mask16
            num_b = bin(num_mask)

            if num >= 0:
                return int(num_b[2:], 2)
            if num < 0:
                return int(num_b[2:], 2) - (1 << size)
        elif size == 32:
            #mask 32 bits
            num_mask = num & mask32
            num_b = bin(num_mask)

            if num >= 0:
                return int(num_b[2:], 2)
            if num < 0:
                return int(num_b[2:], 2) - (1 << size)
        elif size == 64:
            num_mask = num & mask64
            num_b = bin(num_mask)
            if num >= 0:
                return int(num_b[2:], 2)
            if num < 0:
                return int(num_b[2:], 2) - (1 << size)

    @classmethod
    def _multiply(cls, in_x, in_y, shift):
        return (in_x * in_y) >> shift

    def _dc_blocking(self, sig):
        curr_y = 0
        w_val = 0

        if self.dc_state is not None:
            curr_y, w_val = self.dc_state

        out = np.zeros_like(sig)

        for i, in_x in enumerate(sig):
            curr_y = self._truncate_int(in_x - (w_val >> 15), 32)
            w_val += self._truncate_int(self.dc_invpole * curr_y, 32)
            out[i] = self._truncate_int(curr_y, 16)

        self.dc_state = (curr_y, w_val)
        return out

    def _lp_filter(self, sig):
        """A fixed point implementation of a biquad filter."""

        v = [int(0), int(0), int(0)]
        shift = 16

        a = self.lp_a
        b = self.lp_b

        if self.lp_state is not None:
            v = self.lp_state

        y = np.zeros(len(sig),dtype=np.int)

        for i, x in enumerate(sig):
            v[2] = v[1]
            v[1] = v[0]

            temp1 = int(x * (1 << shift)) - self._multiply(a[0], v[1], shift) - self._multiply(a[1], v[2], shift)
            v[0] = self._truncate_int(temp1, 64)

            temp2 = ((self._multiply(b[0], v[0], shift) + self._multiply(b[1], v[1], shift) + self._multiply(b[2], v[2], shift)) >> shift)
            y[i] = self._truncate_int(temp2, 32)

        self.lp_state = v
        return y

    def process(self, input_sig):
        """Process an input signal as if it came from the accelerometer."""

        out = self._dc_blocking(input_sig)

        if self.lowpass:
            out = self._lp_filter(out)

        return out

    def build_waveform(self, shape, peak, duration, rise_time, offset=0.0):
        """Build a shock waveform for injecting into the tile.

        Args:
            shape (str): The shape of the waveform, currently supports trapezoid, constant and half-sine
            peak (float): The peak value of the shock in G's
            duration (float): The duration of the shock in ms
            rise_time (float): The rise and fall times of the shock in ms
            offset (float): A constant offset that can be applied to the axis to simulate gravity
        """

        sample_time = 1.0/self.sampling_rate*1000.0

        samples = []

        if shape == 'trapezoid':
            rise_samples = int(rise_time / sample_time)
            top_samples = int(duration / sample_time)

            for i in xrange(0, rise_samples):
                value = int(peak / self.LSB_VALUE * (float(i) / rise_samples) + offset / self.LSB_VALUE)
                samples.append(value)

            for i in xrange(0, top_samples):
                value = int(peak / self.LSB_VALUE + offset / self.LSB_VALUE)
                samples.append(value)

            for i in xrange(0, rise_samples):
                value = int(peak / self.LSB_VALUE * (float(rise_samples - i - 1) / rise_samples) + offset / self.LSB_VALUE)
                samples.append(value)
        elif shape == 'constant':
            sample_count = int(duration / sample_time)

            for i in xrange(0, sample_count):
                samples.append((peak + offset) / self.LSB_VALUE)
        else:
            raise ValueError("Unknown shock shape: %s" % shape)

        return np.array(samples).astype(int)

    def characterize_shock(self, shock, threshold=0.5):
        """Characterize a shock."""

        delta_t = 1.0 / self.sampling_rate

        peak = np.max(shock)

        threshold = int(threshold / self.LSB_VALUE)

        duration = len(np.where(shock >= threshold)[0])*delta_t*1000
        integral = np.trapz(shock[shock >= threshold], dx=delta_t)
        integral *= 9.80665  # convert from g to m/s^2
        integral *= 39.3701  # convert from m/s to in/s

        return np.array([duration, peak * self.LSB_VALUE, integral])

    def settle(self, offset):
        """Settle the dc blocking filter given a fixed offset level."""

        const_in = self.build_waveform('constant', offset, self.dc_settling, 0)
        self.process(const_in)

    @classmethod
    def _compare_shocks(cls, sum1, sum2):
        return np.abs(sum2 - sum1) * 100.0 / sum2

    def trap_test(self, peak, top, rise, offset=1.0):
        self.settle(offset)

        ideal = self.build_waveform('trapezoid', peak, top, rise, offset)

        if self.include_noise:
            trap_in = ideal + np.random.normal(0, self.noise, len(ideal)).astype(int)
        else:
            trap_in = ideal.copy()

        trap_out = self.process(trap_in)

        ideal -= int(offset / self.LSB_VALUE)
        trap_in -= int(offset / self.LSB_VALUE)

        ideal_results = self.characterize_shock(ideal)
        filtered_results = self.characterize_shock(trap_out)

        return {
            'ideal_results': ideal_results,
            'unfiltered_results': self.characterize_shock(trap_in),
            'filtered_results': filtered_results,
            'error': self._compare_shocks(ideal_results, filtered_results),
            'ideal_wave': ideal,
            'input_wave': trap_in,
            'filtered_wave': trap_out
        }

    def polyphase_decimate(self, in_data, coeff=None, decimation_factor=1, fixed=False):
        """Polyphase filter and decimate an input signal.

        Args:
            input (array(int)): The input signal to process
            coeff (array(int)): The fir coefficients, the length must be a multiple of
                the decimation factor
            decimation_factor (int): The factor by by which to decimate the output rate
            fixed (bool): If fixed, perform the filter in fixed point by quantizing the
                input coefficients and input data.  Both are quantized to 16 bits.
        """

        coeff_mat = []
        delay_mat = []
        acc_mat = []

        if fixed:
            in_data = (in_data/self.LSB_VALUE).astype(int)
            coeff = (coeff*65536).astype(int)

        for i in xrange(0, decimation_factor):
            coeff_row = coeff[i::decimation_factor]
            delay_row = deque([0 for i in xrange(0, len(coeff_row))], len(coeff_row))

            coeff_mat.append(coeff_row)
            delay_mat.append(delay_row)
            acc_mat.append(0)

        coeff_mat.reverse()

        phase = 0
        out_data = np.zeros(len(in_data) // decimation_factor)
        j = 0

        for x in in_data:
            delay_row = delay_mat[phase]
            coeff_row = coeff_mat[phase]

            delay_row.appendleft(x)

            acc_mat[phase] = 0
            for i in xrange(0, len(delay_row)):
                acc_mat[phase] += delay_row[i]*coeff_row[i]

            phase += 1
            if phase == decimation_factor:
                out_data[j] = sum(acc_mat)
                if fixed:
                    out_data[j] /= 65536

                phase = 0
                j += 1

        return out_data
