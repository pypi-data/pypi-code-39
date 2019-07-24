def get_IMU_time(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Takes in a file and row arguement(s) along with a boolean that specifies the amount of rows to read the IMU timestamps for.

    Parameter:

        data: file
            The csv file that is passed in to read.
        arg: int
            The row(s) that are to be read.
        single_row: boolean
            If chosen the IMU timestamp for a single row specified by arg will be output.
        multiple_row: boolean
            If chosen the IMU timestamp for multiple rows specified by arg will be output.
        row_section: boolean
            If chosen the IMU timestamp for a row section by arg will be output.

    Return:

        An array of IMU timestamps.
    """
    IMU_time = []
    
    print("NOTE: All timestamps measured in seconds")
    if single_row is True:
        IMU_time_segment = list(data.values[arg, 1:9])
        IMU_time_segment.reverse()
        IMU_time_segment = [int(elem) for index, elem in enumerate(IMU_time_segment)]
        del IMU_time_segment[0:3]
        IMU_time_segment[0] = float(IMU_time_segment[0])
        IMU = float("".join(map(str, IMU_time_segment)))
        IMU_time.append(IMU)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            IMU_time.append('new row')
            IMU_time_segment = list(data.values[elem, 1:9])
            IMU_time_segment.reverse()
            IMU_time_segment = [int(elem) for index, elem in enumerate(IMU_time_segment)]
            del IMU_time_segment[0:3]
            IMU_time_segment[0] = float(IMU_time_segment[0])
            IMU = float("".join(map(str, IMU_time_segment)))
            IMU_time.append(IMU)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            IMU_time.append('new row')
            IMU_time_segment = list(data.values[row, 1:9])
            IMU_time_segment.reverse()
            IMU_time_segment = [int(elem) for index, elem in enumerate(IMU_time_segment)]
            del IMU_time_segment[0:3]
            IMU_time_segment[0] = float(IMU_time_segment[0])
            IMU = float("".join(map(str, IMU_time_segment)))
            IMU_time.append(IMU)
            
    return IMU_time


def get_accel_time(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Takes in a file and row arguement(s) along with a boolean that specifies the amount of rows to read the accelerometer timestamps for.

    Parameter:

        data: file
            The csv file that is passed in to read.
        arg: int
            The row(s) that are to be read.
        single_row: boolean
            If chosen the accelerometer timestamp for a single row specified by arg will be output.
        multiple_row: boolean
            If chosen the accelerometer timestamp for multiple rows specified by arg will be output.
        row_section: boolean
            If chosen the accelerometer timestamp for a row section by arg will be output.

    Return:

        An array of accelerometer timestamps.
    """
    accel_time = []
    
    if single_row is True:
        accel_time_segment = list(data.values[arg, 9:17])
        accel_time_segment.reverse()
        accel_time_segment = [int(elem) for index, elem in enumerate(accel_time_segment)]
        del accel_time_segment[0:3]
        accel_time_segment[0] = float(accel_time_segment[0])
        accel = float("".join(map(str, accel_time_segment)))
        accel_time.append(accel)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            accel_time.append('new row')
            accel_time_segment = list(data.values[elem, 9:17])
            accel_time_segment.reverse()
            accel_time_segment = [int(elem) for index, elem in enumerate(accel_time_segment)]
            del accel_time_segment[0:3]
            accel_time_segment[0] = float(accel_time_segment[0])
            accel = float("".join(map(str, accel_time_segment)))
            accel_time.append(accel)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            accel_time.append('new row')
            accel_time_segment = list(data.values[row, 9:17])
            accel_time_segment.reverse()
            accel_time_segment = [int(elem) for index, elem in enumerate(accel_time_segment)]
            del accel_time_segment[0:3]
            accel_time_segment[0] = float(accel_time_segment[0])
            accel = float("".join(map(str, accel_time_segment)))
            accel_time.append(accel)
            
    return accel_time


def get_gyro_time(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Takes in a file and row arguement(s) along with a boolean that specifies the amount of rows to read the gyroscope timestamps for.

    Parameter:

        data: file
            The csv file that is passed in to read.
        arg: int
            The row(s) that are to be read.
        single_row: boolean
            If chosen the gyroscope timestamp for a single row specified by arg will be output.
        multiple_row: boolean
            If chosen the gyroscope timestamp for multiple rows specified by arg will be output.
        row_section: boolean
            If chosen the gyroscope timestamp for a row section by arg will be output.

    Return:

        An array of gyroscope timestamps.
    """
    gyro_time = []
    
    if single_row is True:
        gyro_time_segment = list(data.values[arg, 17:25])
        gyro_time_segment.reverse()
        gyro_time_segment = [int(elem) for index, elem in enumerate(gyro_time_segment)]
        del gyro_time_segment[0:3]
        gyro_time_segment[0] = float(gyro_time_segment[0])
        gyro = float("".join(map(str, gyro_time_segment)))
        gyro_time.append(gyro)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            gyro_time.append('new row')
            gyro_time_segment = list(data.values[elem, 17:25])
            gyro_time_segment.reverse()
            gyro_time_segment = [int(elem) for index, elem in enumerate(gyro_time_segment)]
            del gyro_time_segment[0:3]
            gyro_time_segment[0] = float(gyro_time_segment[0])
            gyro = float("".join(map(str, gyro_time_segment)))
            gyro_time.append(gyro)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            gyro_time.append('new row')
            gyro_time_segment = list(data.values[row, 17:25])
            gyro_time_segment.reverse()
            gyro_time_segment = [int(elem) for index, elem in enumerate(gyro_time_segment)]
            del gyro_time_segment[0:3]
            gyro_time_segment[0] = float(gyro_time_segment[0])
            gyro = float("".join(map(str, gyro_time_segment)))
            gyro_time.append(gyro)
            
    return gyro_time


def get_x_accel(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Takes in a file and row arguement(s) along with a boolean that specifies the amount of rows to read the x acceleration for.

    Parameter:

        data: file
            The csv file that is passed in to read.
        arg: int
            The row(s) that are to be read.
        single_row: boolean
            If chosen the x acceleration for a single row specified by arg will be output.
        multiple_row: boolean
            If chosen the x acceleration for multiple rows specified by arg will be output.
        row_section: boolean
            If chosen the x acceleration for a row section by arg will be output.

    Return:

        An array of x acceleration.
    """
    x_accel = []
    
    if single_row is True:
        x_accel_segment = list(data.values[arg, 25:29])
        x_accel_segment.reverse()
        x = int("".join(map(str, x_accel_segment)))
        x_accel.append(x)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            x_accel.append('new row')
            x_accel_segment = list(data.values[elem, 25:29])
            x_accel_segment.reverse()
            x = int("".join(map(str, x_accel_segment)))
            x_accel.append(x)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            x_accel.append('new row')
            x_accel_segment = list(data.values[row, 25:29])
            x_accel_segment.reverse()
            x = int("".join(map(str, x_accel_segment)))
            x_accel.append(x)
            
    return x_accel


def get_y_accel(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Takes in a file and row arguement(s) along with a boolean that specifies the amount of rows to read the y acceleration for.

    Parameter:

        data: file
            The csv file that is passed in to read.
        arg: int
            The row(s) that are to be read.
        single_row: boolean
            If chosen the y acceleration for a single row specified by arg will be output.
        multiple_row: boolean
            If chosen the y acceleration for multiple rows specified by arg will be output.
        row_section: boolean
            If chosen the y acceleration for a row section by arg will be output.

    Return:

        An array of y acceleration.
    """
    y_accel = []
    
    if single_row is True:
        y_accel_segment = list(data.values[arg, 29:33])
        y_accel_segment.reverse()
        y = int("".join(map(str, y_accel_segment)))
        y_accel.append(y)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            y_accel.append('new row')
            y_accel_segment = list(data.values[elem, 29:33])
            y_accel_segment.reverse()
            y = int("".join(map(str, y_accel_segment)))
            y_accel.append(y)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            y_accel.append('new row')
            y_accel_segment = list(data.values[row, 29:33])
            y_accel_segment.reverse()
            y = int("".join(map(str, y_accel_segment)))
            y_accel.append(y)
            
    return y_accel


def get_z_accel(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Takes in a file and row arguement(s) along with a boolean that specifies the amount of rows to read the z acceleration for.

    Parameter:

        data: file
            The csv file that is passed in to read.
        arg: int
            The row(s) that are to be read.
        single_row: boolean
            If chosen the z acceleration for a single row specified by arg will be output.
        multiple_row: boolean
            If chosen the z acceleration for multiple rows specified by arg will be output.
        row_section: boolean
            If chosen the z acceleration for a row section by arg will be output.

    Return:

        An array of z acceleration.
    """
    z_accel = []
    
    if single_row is True:
        z_accel_segment = list(data.values[arg, 33:37])
        z_accel_segment.reverse()
        z = int("".join(map(str, z_accel_segment)))
        z_accel.append(z)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            z_accel.append('new row')
            z_accel_segment = list(data.values[elem, 33:37])
            z_accel_segment.reverse()
            z = int("".join(map(str, z_accel_segment)))
            z_accel.append(z)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            z_accel.append('new row')
            z_accel_segment = list(data.values[row, 33:37])
            z_accel_segment.reverse()
            z = int("".join(map(str, z_accel_segment)))
            z_accel.append(z)
            
    return z_accel


def get_x_ang_vel(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Takes in a file and row arguement(s) along with a boolean that specifies the amount of rows to read the x angular velocity for.

    Parameter:

        data: file
            The csv file that is passed in to read.
        arg: int
            The row(s) that are to be read.
        single_row: boolean
            If chosen the x angular velocity for a single row specified by arg will be output.
        multiple_row: boolean
            If chosen the x angular velocity for multiple rows specified by arg will be output.
        row_section: boolean
            If chosen the x angular velocity for a row section by arg will be output.

    Return:

        An array of x angular velocity.
    """
    x_ang_vel = []
    
    if single_row is True:
        x_ang_vel_segment = list(data.values[arg, 37:41])
        x_ang_vel_segment.reverse()
        x_ang = int("".join(map(str, x_ang_vel_segment)))
        x_ang_vel.append(x_ang)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            x_ang_vel.append('new row')
            x_ang_vel_segment = list(data.values[elem, 37:41])
            x_ang_vel_segment.reverse()
            x_ang = int("".join(map(str, x_ang_vel_segment)))
            x_ang_vel.append(x_ang)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            x_ang_vel.append('new row')
            x_ang_vel_segment = list(data.values[row, 37:41])
            x_ang_vel_segment.reverse()
            x_ang = int("".join(map(str, x_ang_vel_segment)))
            x_ang_vel.append(x_ang)
            
    return x_ang_vel


def get_y_ang_vel(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Takes in a file and row arguement(s) along with a boolean that specifies the amount of rows to read the y angular velocity for.

    Parameter:

        data: file
            The csv file that is passed in to read.
        arg: int
            The row(s) that are to be read.
        single_row: boolean
            If chosen the y angular velocity for a single row specified by arg will be output.
        multiple_row: boolean
            If chosen the y angular velocity for multiple rows specified by arg will be output.
        row_section: boolean
            If chosen the y angular velocity for a row section by arg will be output.

    Return:

        An array of y angular velocity.
    """
    y_ang_vel = []
    
    if single_row is True:
        y_ang_vel_segment = list(data.values[arg, 41:45])
        y_ang_vel_segment.reverse()
        y_ang = int("".join(map(str, y_ang_vel_segment)))
        y_ang_vel.append(y_ang)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            y_ang_vel.append('new row')
            y_ang_vel_segment = list(data.values[elem, 41:45])
            y_ang_vel_segment.reverse()
            y_ang = int("".join(map(str, y_ang_vel_segment)))
            y_ang_vel.append(y_ang)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            y_ang_vel.append('new row')
            y_ang_vel_segment = list(data.values[row, 41:45])
            y_ang_vel_segment.reverse()
            y_ang = int("".join(map(str, y_ang_vel_segment)))
            y_ang_vel.append(y_ang)
            
    return y_ang_vel


def get_z_ang_vel(data, arg, single_row=False, multiple_row=False, row_section=False):
    """
    Takes in a file and row arguement(s) along with a boolean that specifies the amount of rows to read the z angular velocity for.

    Parameter:

        data: file
            The csv file that is passed in to read.
        arg: int
            The row(s) that are to be read.
        single_row: boolean
            If chosen the z angular velocity for a single row specified by arg will be output.
        multiple_row: boolean
            If chosen the z angular velocity for multiple rows specified by arg will be output.
        row_section: boolean
            If chosen the z angular velocity for a row section by arg will be output.

    Return:

        An array of z angular velocity.
    """
    z_ang_vel = []
    
    if single_row is True:
        z_ang_vel_segment = list(data.values[arg, 45:49])
        z_ang_vel_segment.reverse()
        z_ang = int("".join(map(str, z_ang_vel_segment)))
        z_ang_vel.append(z_ang)
    elif multiple_row is True:
        for index, elem in enumerate(arg):
            z_ang_vel.append('new row')
            z_ang_vel_segment = list(data.values[elem, 45:49])
            z_ang_vel_segment.reverse()
            z_ang = int("".join(map(str, z_ang_vel_segment)))
            z_ang_vel.append(z_ang)
    elif row_section is True:
        for row in range(arg[0], arg[1]+1):
            z_ang_vel.append('new row')
            z_ang_vel_segment = list(data.values[row, 45:49])
            z_ang_vel_segment.reverse()
            z_ang = int("".join(map(str, z_ang_vel_segment)))
            z_ang_vel.append(z_ang)
            
    return z_ang_vel
