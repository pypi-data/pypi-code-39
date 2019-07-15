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

    Example:

        >>> get_timestamp("lidar_data3.csv", 0, single_row=True)
        >>> [33.0202114185206, 33.0202116496, 33.0202117174244, 33.0202119463, 33.0202120189236, 33.020212246132, 33.0202123185122, 33.02021254748, 33.0202126186208, 33.020212861196, 33.020212917536, 33.02021314678, 33.020213218632, 33.02021345714, 33.020213518654, 33.020213754204]

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

    Example:

        >>> get_frame_id("lidar_data3.csv", 0, single_row=True)
        >>> [222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237]

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

    Example:

        >>> get_measurement_id("lidar_data3.csv", 0,single_row=True)
        >>> [4239, 4239, 4239, 4239, 4239, 4239, 4239, 4239, 4239, 4239, 4239, 4239, 4239, 4239, 4239, 4239]

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

    Example:

        >>> get_encoder_count("lidar_data3.csv", 0, single_row=True)
        >>> [7680, 76168, 770, 7788, 77176, 788, 7896, 78184, 7916, 79104, 79192, 8024, 80112, 80200, 8132, 81120]

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

    Example:

        >>> get_signal_photons("lidar_data3.csv", 0, single_row=True, azimuth_block=0)
        >>> [26, 0, 0, 0, 48, 0, 0, 0, 26, 0, 0, 0, 14, 0, 0, 0, 11, 0, 0, 0, 15, 0, 0, 0, 17, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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

    Example:

        >>> get_range("lidar_data3.csv",0,single_row=True)
        >>> [12810, 0, 0, 0, 19810, 0, 0, 0, 3810, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1874, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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

    Example:

        >>> get_reflectivity("lidar_data3.csv",0, single_row=True)
        >>> [19, 0, 0, 0, 36, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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

    Example:

        >>> get_noise_photons("lidar_data3.csv",0, single_row=True)
        >>> [1456, 3633, 1, 129128, 1704, 400, 1920, 124176, 2274, 360, 177190, 61, 2043, 10, 369, 1287, 1214, 21022, 80, 132112, 2344, 170254, 226136, 216255, 2543, 8, 252248, 248, 1962, 9239, 150, 9663, 1647, 128148, 70, 232178, 1536, 172, 12864, 202, 1895, 2870, 157112, 214, 2203, 24172, 12639, 19253, 5012, 136128, 4, 94238, 193, 1280, 4160, 208124, 1474, 255143, 4064, 90, 2433, 848, 16724, 20068]

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
