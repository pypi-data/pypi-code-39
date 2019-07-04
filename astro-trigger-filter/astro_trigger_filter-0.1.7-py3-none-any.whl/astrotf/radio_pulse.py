import sys

def dm_one_delay(freq_lo_mhz, freq_hi_mhz):
    return 4.15E3 * (freq_lo_mhz**-2 - freq_hi_mhz**-2)


def test_radio_pulse_intersection(t_i, w_i, dm_i, t_k, w_k, dm_k, dm1, tol):
    if t_i >= t_k:
        return (t_i <= t_k + w_k + tol) or \
               (t_i + dm_i * dm1 <= t_k + w_k + tol + dm_k * dm1)
    else:
        return (t_k <= t_i + w_i + tol) or \
               (t_k + dm_k * dm1 <= t_i + w_i + tol + dm_i * dm1)


class RadioPulseIntersectionGen:

    def __init__(self, freq_lo_mhz, freq_hi_mhz, time_tol=0.0):
        self.tol = time_tol
        self.dm1 = dm_one_delay(freq_lo_mhz, freq_hi_mhz)

    def __call__(self, expression):
        # Input a list of tuples: [ (t, w, dm, snr), ... ]

        # A set of active trigger that started before the current one,
        # and have not yet ended. This set is sorted on time
        active_set = []

        # Accumulate Performance Statistics: number of trigger that went in/out.
        self.num_in = 0
        self.num_out = 0
        trigger_id = -1

        # The main loop, we process items from an iterable object
        it = expression.__iter__()
        while True:

            try:
                t_i, w_i, dm_i = it.__next__()
                self.num_in += 1
                trigger_id += 1

                # compare the current trigger against all triggers in the active set
                k = 0
                while k < len(active_set):
                    t_k, w_k, dm_k, id_k, end_k = active_set[k]

                    # remove expired trigger and optionally yield them if they were local_max
                    if t_i > end_k:
                        del active_set[k]
                        continue

                    # check if trigger_i intersects with trigger_k
                    if (t_i <= t_k + w_k + self.tol) or (t_i + dm_i * self.dm1 <= end_k):
                        self.num_out += 1
                        yield trigger_id, id_k

                    k += 1
                end_i = t_i + w_i + dm_i * self.dm1 + self.tol
                active_set.append((t_i, w_i, dm_i, trigger_id, end_i))

            except StopIteration:
                break


class RadioPulseFilterGen:

    def __init__(self, freq_lo_mhz, freq_hi_mhz, time_tol=0.0, buffersize=0, autoflush=True):
        self.tol = time_tol
        self.dm1 = dm_one_delay(freq_lo_mhz, freq_hi_mhz)

        self.active_set = []
        self.is_local_max = []
        self.buffersize = buffersize
        self.autoflush = autoflush

        # Accumulate Performance Statistics: number of trigger that went in/out.
        self.num_in = 0
        self.num_out = 0

    def clear(self):
        # A set of active trigger that started before the current one,
        # and have not yet ended. This set is sorted on time

        self.active_set = []
        self.is_local_max = []

        # Accumulate Performance Statistics: number of trigger that went in/out.
        self.num_in = 0
        self.num_out = 0

    def flush(self):
        while len(self.active_set) > 0:
            is_local_max_k = self.is_local_max[0]
            ttl_k, w_k, dm_k, snr_k, ttr_k, tbr_k = self.active_set[0]

            del self.active_set[0]
            del self.is_local_max[0]

            if is_local_max_k:
                self.num_out += 1
                yield ttl_k, w_k, dm_k, snr_k

    def __call__(self, expression):
        # Input a list of tuples: [ (t, w, dm, snr), ... ]

        # The main loop, we process items from an iterable object
        it = expression.__iter__()

        # Support both Python 2 and 3
        if (sys.version_info > (3, 0)):
            def get_next(it):
                return it.__next__()
        else:
            def get_next(it):
                return it.next()

        while True:

            try:
                ttl_i, w_i, dm_i, snr_i = get_next(it) #it.__next__()
                self.num_in += 1

                # compute template time at bottom left and right
                ttr_i = ttl_i + w_i + self.tol
                tbl_i = ttl_i + dm_i * self.dm1
                tbr_i = tbl_i + w_i + self.tol

                # Unless proven otherwise we assume this trigger has no intersection
                is_local_max_i = True
                add_to_active_set = True

                # compare the current trigger against all triggers in the active set
                # the active set changes size inside this loop so we manage our own loop counter
                k = 0
                while k < len(self.active_set):

                    # get the k-th trigger daat from the active set
                    is_local_max_k = self.is_local_max[k]
                    ttl_k, w_k, dm_k, snr_k, ttr_k, tbr_k = self.active_set[k]

                    # handle expired triggers
                    if tbr_k < ttl_i:

                        # remove expired trigger from the active set
                        del self.active_set[k]
                        del self.is_local_max[k]

                        # yield it if this was a local_max
                        if is_local_max_k:
                            self.num_out += 1
                            yield ttl_k, w_k, dm_k, snr_k

                        # continue to compare this trigger against the next one in the active set
                        continue

                    # analyse what to do if triggerst intersect
                    if (ttl_i <= ttr_k) or (tbl_i <= tbr_k):

                        # do we have the highest S/R ?
                        if snr_i > snr_k:
                            self.is_local_max[k] = False

                        # do we have the smallest S/R ?
                        else:
                            is_local_max_i = False
                            contained = (tbr_i <= tbr_k)

                            # Are we completely covered by this higher S/R trigger?
                            if contained:
                                add_to_active_set = False
                    k += 1

                if add_to_active_set:

                    # do we need to first make room?
                    if self.buffersize > 0:
                        while len(self.active_set) >= self.buffersize:

                            # pop the oldest
                            is_local_max_k = self.is_local_max[0]
                            ttl_k, w_k, dm_k, snr_k, ttr_k, tbr_k = self.active_set[0]

                            del self.active_set[0]
                            del self.is_local_max[0]

                            if is_local_max_k:
                                self.num_out += 1
                                yield ttl_k, w_k, dm_k, snr_k

                    # now add
                    self.active_set.append((ttl_i, w_i, dm_i, snr_i, ttr_i, tbr_i))
                    self.is_local_max.append(is_local_max_i)

            except StopIteration:
                # we are done processing triggers, flush the active set
                if self.autoflush:
                    self.flush()
                break


def radio_pulse_polygon(t0, w, dm, num_steps=100, freq_lo=1249.8046875, freq_hi=1549.8046875):

    f_step = (freq_hi - freq_lo) / (num_steps - 1)

    v0 = []
    v1 = []

    for i in range(num_steps):
        f_i = freq_hi - i * f_step
        delay_i = dm_one_delay(f_i, freq_hi) * dm
        v0.append((t0 + delay_i, f_i))
        v1.append((t0 + delay_i + w, f_i))

    return v0 + v1[::-1]
