def get_timestamp(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Returns the timestamp of the csv file made from the lidar recording. Based on what boolean the user set to be true,
    the timestamp will output for those row(s).

    Parameters:

        data: Pandas dataframe
            A pandas dataframe used to extract values.
        arg: int
            The row(s) number to be read.
        single_row: boolean
            If this is set to true, output the timestamps for the row that the user selected.
        multiple_row: boolean
            If this is set to true, output the timestamps for the rows that the user selected.
        row_section: boolean
            If this is set to true, output the timestamps for the row sections the user selected.

    Return:

        An array of all the timestamps the user desired to read.
    """

    timestamp = []

    print("NOTE: All timestamps measured in seconds and each element is a timestamp for single azimuth block")
    if single_row is True:
        for col in range(1, len(data.columns)-1, 788):
            timestamp_segment = list(data.values[arg, col:col+8])
            timestamp_segment.reverse()
            timestamp_segment = [int(elem) for index, elem in enumerate(timestamp_segment)]
            del timestamp_segment[0:3]
            timestamp_segment[0] = float(timestamp_segment[0])
            time = float("".join(map(str, timestamp_segment)))
            timestamp.append(time)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            timestamp.append("new row")
            for col in range(1, len(data.columns)-1, 788):
                timestamp_segment = list(data.values[elem, col:col+8])
                timestamp_segment.reverse()
                timestamp_segment = [int(elem) for index, elem in enumerate(timestamp_segment)]
                del timestamp_segment[0:3]
                timestamp_segment[0] = float(timestamp_segment[0])
                time = float("".join(map(str, timestamp_segment)))
                timestamp.append(time)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            timestamp.append("new row")
            for col in range(1, len(data.columns)-1, 788):
                timestamp_segment = list(data.values[row, col:col+8])
                timestamp_segment.reverse()
                timestamp_segment = [int(elem) for index, elem in enumerate(timestamp_segment)]
                del timestamp_segment[0:3]
                timestamp_segment[0] = float(timestamp_segment[0])
                time = float("".join(map(str, timestamp_segment)))
                timestamp.append(time)

    return timestamp


def get_frame_id(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Returns the frame ID of the csv file made from the lidar recording. Based on what boolean the user set to be true,
    the frame ID will output for those row(s).

    Parameters:

        data: Pandas dataframe
            A pandas dataframe used to extract values.
        arg: int
            The row(s) number to be read.
        single_row: boolean
            If this is set to true, output the frame IDs for the row that the user selected.
        multiple_row: boolean
            If this is set to true, output the frame IDs for the rows that the user selected.
        row_section: boolean
            If this is set to true, output the frame IDs for the row sections the user selected.

    Return:

        An array of all the frame IDs the user desired to read.
    """
    frame_id = []

    print("NOTE: Each element is a frame ID for single azimuth block")
    if single_row is True:
        for col in range(9, len(data.columns) - 1, 788):
            frame_id_segment = list(data.values[arg, col:col + 2])
            frame_id_segment.reverse()
            frame_id_segment = [int(elem) for index, elem in enumerate(frame_id_segment)]
            frame = int("".join(map(str, frame_id_segment)))
            frame_id.append(frame)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            frame_id.append("new row")
            for col in range(9, len(data.columns) - 1, 788):
                frame_id_segment = list(data.values[elem, col:col + 2])
                frame_id_segment.reverse()
                frame_id_segment = [int(elem) for index, elem in enumerate(frame_id_segment)]
                frame = int("".join(map(str, frame_id_segment)))
                frame_id.append(frame)
    elif row_section is True:
        for row in range(arg[0], arg[1] + 1):
            frame_id.append("new row")
            for col in range(9, len(data.columns) - 1, 788):
                frame_id_segment = list(data.values[row, col:col + 2])
                frame_id_segment.reverse()
                frame_id_segment = [int(elem) for index, elem in enumerate(frame_id_segment)]
                frame = int("".join(map(str, frame_id_segment)))
                frame_id.append(frame)

    return frame_id


def get_measurement_id(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Returns the measurement ID of the csv file made from the lidar recording. Based on what boolean the user set to be true,
    the measurement ID will output for those row(s).

    Parameters:

        data: Pandas dataframe
            A pandas dataframe used to extract values.
        arg: int
            The row(s) number to be read.
        single_row: boolean
            If this is set to true, output the measurement IDs for the row that the user selected.
        multiple_row: boolean
            If this is set to true, output the measurement IDs for the rows that the user selected.
        row_section: boolean
            If this is set to true, output the measurement IDs for the row sections the user selected.

    Return:

        An array of all the measurement IDs the user desired to read.
    """
    measurement_id = []

    print("NOTE: Each element is a measurement ID for single azimuth block")
    if single_row is True:
        for col in range(11, len(data.columns)-1,788):
            measurement_id_segment = list(data.values[arg, col:col+2])
            measurement_id_segment.reverse()
            measurement_id_segment = [int(elem) for index, elem in enumerate(measurement_id_segment)]
            measurement = int("".join(map(str, measurement_id_segment)))
            measurement_id.append(measurement)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            measurement_id.append("new row")
            for col in range(11, len(data.columns)-1,788):
                measurement_id_segment = list(data.values[elem, col:col+2])
                measurement_id_segment.reverse()
                measurement_id_segment = [int(elem) for index, elem in enumerate(measurement_id_segment)]
                measurement = int("".join(map(str, measurement_id_segment)))
                measurement_id.append(measurement)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            measurement_id.append("new row")
            for col in range(11, len(data.columns)-1, 788):
                measurement_id_segment = list(data.values[row, col:col+2])
                measurement_id_segment.reverse()
                measurement_id_segment = [int(elem) for index, elem in enumerate(measurement_id_segment)]
                measurement = int("".join(map(str, measurement_id_segment)))
                measurement_id.append(measurement)

    return measurement_id


def get_encoder_count(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Returns the encoder count of the csv file made from the lidar recording. Based on what boolean the user set to be true,
    the encoder count will output for those row(s).

    Parameters:

        data: Pandas dataframe
            A pandas dataframe used to extract values.
        arg: int
            The row(s) number to be read.
        single_row: boolean
            If this is set to true, output the encoder count for the row that the user selected.
        multiple_row: boolean
            If this is set to true, output the encoder count for the rows that the user selected.
        row_section: boolean
            If this is set to true, output the encoder count for the row sections the user selected.

    Return:

        An array of all the encoder count the user desired to read.
    """

    encoder_count = []

    print("NOTE: Each element is a encoder count for single azimuth block")
    if single_row is True:
        for col in range(13, len(data.columns) - 1, 788):
            encoder_count_segment = list(data.values[arg, col:col + 4])
            encoder_count_segment.reverse()
            encoder_count_segment = [int(elem) for index, elem in enumerate(encoder_count_segment)]
            encoder = int("".join(map(str, encoder_count_segment)))
            encoder_count.append(encoder)

    elif multiple_row is True:
        for index, elem in enumerate(arg):
            encoder_count.append('new row')
            for col in range(13, len(data.columns) - 1, 788):
                encoder_count_segment = list(data.values[elem, col:col + 4])
                encoder_count_segment.reverse()
                encoder_count_segment = [int(elem) for index, elem in enumerate(encoder_count_segment)]
                encoder = int("".join(map(str, encoder_count_segment)))
                encoder_count.append(encoder)
    elif row_section is True:
        for row in range(arg[0], arg[1] + 1):
            encoder_count.append('new row')
            for col in range(13, len(data.columns) - 1, 788):
                encoder_count_segment = list(data.values[row, col:col + 4])
                encoder_count_segment.reverse()
                encoder_count_segment = [int(elem) for index, elem in enumerate(encoder_count_segment)]
                encoder = int("".join(map(str, encoder_count_segment)))
                encoder_count.append(encoder)

    return encoder_count


def get_signal_photons(data, arg, single_row=False, multiple_row=False, row_section=False, azimuth_block=0):
    """
    Returns the signal photons of the csv file made from the lidar recording. Based on what boolean the user set to be true,
    the signal photons will output for those row(s).

    Parameters:

        azimuth_block: int
            Specifies which azimuth to read signal photons values from.
        single_row: boolean
            If this is set to true, output the signal photons for the row that the user selected.
        multiple_row: boolean
            If this is set to true, output the signal photons for the rows that the user selected.
        row_section: boolean
            If this is set to true, output the signal photons for the row sections the user selected.

    Return:

        An array of all the signal photons the user desired to read.
    """
    signal_photons = []

    print("NOTE: Each element is a signal photon count for single channel in azimuth block")
    if single_row is True:
        for col in (range(22+azimuth_block, azimuth_block+784, 12)):
            signal_photons_segment = list(data.values[arg, col:col+2])
            signal_photons_segment = [int(elem) for index, elem in enumerate(signal_photons_segment)]
            signl_p = int("".join(map(str, signal_photons_segment)))
            signal_photons.append(signl_p)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            signal_photons.append('new row')
            for col in (range(22+azimuth_block, azimuth_block+784, 12)):
                signal_photons_segment = list(data.values[elem, col:col+2])
                signal_photons_segment = [int(elem) for index, elem in enumerate(signal_photons_segment)]
                signl_p = int("".join(map(str, signal_photons_segment)))
                signal_photons.append(signl_p)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            signal_photons.append('new row')
            for col in (range(22+azimuth_block, azimuth_block+784, 12)):
                signal_photons_segment = list(data.values[row, col:col+2])
                signal_photons_segment = [int(elem) for index, elem in enumerate(signal_photons_segment)]
                signl_p = int("".join(map(str, signal_photons_segment)))
                signal_photons.append(signl_p)

    return signal_photons


def get_range(data, arg, single_row=False, multiple_row=False, row_section=False, azimuth_block=0):
    """
    Returns the range of the csv file made from the lidar recording. Based on what boolean the user set to be true,
    the range will output for those row(s).

    Parameters:

        data: Pandas dataframe
            A pandas dataframe used to extract values.
        arg: int
            The row(s) number to be read.
        azimuth_block: int
            Specifies which azimuth to read range values from.
        single_row: boolean
            If this is set to true, output the range for the row that the user selected.
        multiple_row: boolean
            If this is set to true, output the range for the rows that the user selected.
        row_section: boolean
            If this is set to true, output the erange for the row sections the user selected.

    Return:

        An array of all the range the user desired to read.
    """
    range_mm = []

    print("NOTE: Each element is a range in millimeters for single channel in azimuth block")
    if single_row is True:
        for col in (range(16+azimuth_block, azimuth_block+784, 12)):
            range_segment = list(data.values[arg, col:col+3])
            range_segment = [int(elem) for index, elem in enumerate(range_segment)]
            rang = int("".join(map(str, range_segment)))
            range_mm.append(rang)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            range_mm.append('new row')
            for col in (range(16+azimuth_block, azimuth_block+784, 12)):
                range_segment = list(data.values[elem, col:col+3])
                range_segment = [int(elem) for index, elem in enumerate(range_segment)]
                rang = int("".join(map(str, range_segment)))
                range_mm.append(rang)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            range_mm.append('new row')
            for col in (range(16+azimuth_block, azimuth_block+784, 12)):
                range_segment = list(data.values[row, col:col+3])
                range_segment = [int(elem) for index, elem in enumerate(range_segment)]
                rang = int("".join(map(str, range_segment)))
                range_mm.append(rang)

    return range_mm


def get_reflectivity(data, arg, single_row=False, multiple_row=False, row_section=False, azimuth_block=0):
    """
    Returns the reflectivity of the csv file made from the lidar recording. Based on what boolean the user set to be true,
    the reflectivity will output for those row(s).

    Parameters:

        data: Pandas dataframe
            A pandas dataframe used to extract values.
        arg: int
            The row(s) number to be read.
        azimuth_block: int
            Specifies which azimuth to read reflectivity values from.
        single_row: boolean
            If this is set to true, output the reflectivity for the row that the user selected.
        multiple_row: boolean
            If this is set to true, output the reflectivity for the rows that the user selected.
        row_section: boolean
            If this is set to true, output the reflectivity for the row sections the user selected.

    Return:

        An array of all the reflectivity the user desired to read.
    """
    reflectivity = []

    print("NOTE: Each element is a reflectivity for single channel in azimuth block")
    if single_row is True:
        for col in (range(20+azimuth_block, azimuth_block+784, 12)):
            reflectivity_segment = list(data.values[arg, col:col+2])
            reflectivity_segment = [int(elem) for index, elem in enumerate(reflectivity_segment)]
            reflect = int("".join(map(str, reflectivity_segment)))
            reflectivity.append(reflect)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            reflectivity.append('new row')
            for col in (range(20+azimuth_block, azimuth_block+784, 12)):
                reflectivity_segment = list(data.values[elem, col:col+2])
                reflectivity_segment = [int(elem) for index, elem in enumerate(reflectivity_segment)]
                reflect = int("".join(map(str, reflectivity_segment)))
                reflectivity.append(reflect)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            reflectivity.append('new row')
            for col in (range(20+azimuth_block, azimuth_block+784, 12)):
                reflectivity_segment = list(data.values[row, col:col+2])
                reflectivity_segment = [int(elem) for index, elem in enumerate(reflectivity_segment)]
                reflect = int("".join(map(str, reflectivity_segment)))
                reflectivity.append(reflect)

    return reflectivity


def get_noise_photons(data, arg, single_row=False, multiple_row=False, row_section=False, azimuth_block=0):
    """
    Returns the noise photons of the csv file made from the lidar recording. Based on what boolean the user set to be true,
    the noise photons will output for those row(s).

    Parameters:

        data: Pandas dataframe
            A pandas dataframe used to extract values.
        arg: int
            The row(s) number to be read.
        azimuth_block: int
            Specifies which azimuth to read noise photons values from.
        single_row: boolean
            If this is set to true, output the noise photons for the row that the user selected.
        multiple_row: boolean
            If this is set to true, output the noise photons for the rows that the user selected.
        row_section: boolean
            If this is set to true, output the noise photons for the row sections the user selected.

    Return:

        An array of all the noise photons the user desired to read.
    """
    noise_photons = []

    print("NOTE: Each element is a noise photon count for single channel in azimuth block")
    if single_row is True:
        for col in (range(24+azimuth_block, azimuth_block+788, 12)):
            noise_photons_segment = list(data.values[arg, col:col+3])
            noise_photons_segment = [int(elem) for index, elem in enumerate(noise_photons_segment)]
            noise_p = int("".join(map(str, noise_photons_segment)))
            noise_photons.append(noise_p)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            noise_photons.append('new row')
            for col in (range(24+azimuth_block, azimuth_block+788, 12)):
                noise_photons_segment = list(data.values[elem, col:col+3])
                noise_photons_segment = [int(elem) for index, elem in enumerate(noise_photons_segment)]
                noise_p = int("".join(map(str, noise_photons_segment)))
                noise_photons.append(noise_p)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            noise_photons.append('new row')
            for col in (range(24+azimuth_block, azimuth_block+788, 12)):
                noise_photons_segment = list(data.values[row, col:col+3])
                noise_photons_segment = [int(elem) for index, elem in enumerate(noise_photons_segment)]
                noise_p = int("".join(map(str, noise_photons_segment)))
                noise_photons.append(noise_p)


    return noise_photons
