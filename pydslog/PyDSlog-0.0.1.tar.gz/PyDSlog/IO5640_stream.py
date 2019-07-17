import serial
import crc8
import struct
import numpy as np


def start_IO5640_stream(channels, frequency, connection):

    """
        Start the Data Streaming Mode
        parameters:

            channels: type= list of strings
                A list with the IO5640 ports to activate and use

            Frequency: type=integer
                The frequency of the incoming data

            Connection: serial connection

        returns: none
    """
    n_ports = 0
    
    CHANNELS = {
        "uin4": 1,                      #"\x01",  # 00000001
        "uin3": 2,                      #"\x02",  # 00000010
        "uin2": 4,                      #"\x04",  # 00000100
        "uin1": 8,                      #"\x08",  # 00001000
        "iin1": 16,                     #"\x10", # 00010000
        "iin2": 32,                     #"\x20", # 00100000
        "iin3": 64,                     #"\x40", # 01000000
        "iin4": 128,                    #"\x80"  # 10000000
    }

    #freq = (11520)/((2*N_channels) + 3)
  
    start_flag = "A"                    # write A 01000001
    ports_in   =  0     #"\x00"         # write b0000 1000 for UIN1
    read_freq1  = 0     #"\x00"         # write b0000 1000 1111 1100 for 2300Hz (byte 1)
    read_freq2  = 0     #"\x02"         # write b0000 1000 1111 1100 for 2300Hz (byte 2)
    
    
    for n in channels:
        for j in CHANNELS:
            if(n == j):
                ports_in = (ports_in | CHANNELS[j]) # set bits in variable ports_in for the selected ports to use
                n_ports = n_ports + 1               # counter n_ports
     
    
    f_upper = (frequency >> 8) & 0xff   # upper
    f_lower = frequency & 0xff          # lower
    
    f_max = 11520/((2*n_ports) + 3)     # Calculate max frequency
    
    if(f_max < frequency):
        print("f too high: ")           # if the selected frequency is higher to f_max, then print alert
        print(f_max)   
    
    arr = [ord(start_flag), ports_in, f_lower, f_upper]  # put everything in one list
    
    b_arr = bytearray(arr)              # bytearray from list

    hash = crc8.crc8()                  # crc8
    hash.update(b_arr)                  # crc with buff
    crc_val = hash.digest()             # read crc value
    b_arr = b_arr + crc_val             # add crc_val to the end of the bytearray

    connection.write(b_arr)                 # write buff with streaming settings

    
def stop_IO5640_stream(connection):             
    
    """
        Stop the Data Streaming Mode
        parameters: none
        returns: none
    """
    for i in range(0,512):                                  # send 512 times "z" to stop the streaming mode
        connection.write(b"\x5A")

        

def read_IO5640_stream_once(n_ports, connection):
    
    """
        Read the incoming data. For small quantities of data with low frequency.
        parameters:

            n_ports: type=integer
                Number of ports in use

            Connection: serial connection

        returns: tuple with n_ports values
    """

    read_qty = 2 + (n_ports * 2)                        # Calculate expected bytes to read
    f = str(n_ports) + "h"                              # h for the format integer. see python struct formats 
        
    while 1:                                            # loop   
        
        frame = connection.read(read_qty)               # read one frame from serial connection
               
        if(frame[0] == 0x4D):                           # check if first byte is a "M"
            
            hash = crc8.crc8()                          # crc8
            hash.update(frame)                           # check if received data is ok
            
            if(hash.hexdigest() != "00"):               # if crc value is not o, then we have an error
                break                                   # wait and read again new values
            else:
                
                ret = struct.unpack(f,frame[1:-1])      # unpack and put result in numpy array             
                return(ret)                             # return values
        else:

            r = connection.read(1)                      # if first byte is not a "M", we read one byte more
            frame = frame[1:] + r                       # slide one byte and append the new one at the end
            

def read_IO5640_stream_block(sz_block, n_ports, connection, n_frame=100):      
    
    """
        Read the incoming data in Blocks. Usefull for large amount of Data with a high incoming frequency.
        parameters:
        
            sz_block: type=integer
                The size of the returned array. 
                Also the dimension of one axis of the returned numpy-array 

            n_ports: type=integer
                Number of ports in use

            Connection: serial connection
            
            n_frame: type=integer default 100
                The number of Frames to read at once so we dont haveto read byte by byte and we are faster.
                Should by <= sz_block.

        returns: numpy-array with dimesion  n_ports x sz_block 
    """
    
    n_frames = n_frame                                      # number of frames we want to read at once
    read_qty = 2 + (n_ports * 2)                            # Calculate expected bytes to read
    f = str(n_ports) + "h"                                  # h for the format integer. see python struct formats
    ret = np.empty([n_ports, sz_block]).astype(int)  

    count = 0                                               # counter. If this conter has the value of sz_block, 
                                                            # then we are ready and return N-array with values
    
    while 1:                                                # loop
        
        buff = connection.read(read_qty * n_frames)         # read (read_qty x n_frames) bytes into buff 
        start_f = 0                                         # start point of the frames in the buffer
        
        while(start_f < read_qty * n_frames):               # loop as long we havent reached (read_qty x n_frames) bytes
            
            r = buff[start_f]                               # read first byte of first frame in the buffer

            if(r == 0x4D):                                  # if it is an "M" we can start unpacking
                
                frame = buff[start_f:start_f + read_qty]    # we take one frame
                start_f += read_qty                         # we update start_f for the read of the next frame

                hash = crc8.crc8()                          # crc8
                hash.update(frame)                           # check if received data is ok
              
                if(hash.hexdigest() == "00"):               # if crc value is 0, then frame is ok.
                    
                    vals = struct.unpack(f,frame[1:-1])     # unpack and put result in numpy array
                    for p in range(0, n_ports):
                        ret[p][count] = vals[p]             # numpy array at the end with sz_block x n_ports dimensions
                        
                    count += 1                              # update count
                    if(count >= sz_block):                  # if count >= sz_block, we are ready and we return all the values
                        return(ret)
                    
            else:                                           # if first byte of the first frame is not a "M"
                r = connection.read(1)                      # we read one byte
                buff = buff[1:] + r                         # we slide buff and append the new byte at the end, then we try again

               



 
"""
# demo code

# Copy and paste the following code in a new .py file stored in the same directory as IO5640_Stream.py


import IO5640_Stream as ssv_io
import time
import serial
import pandas as pd
import numpy as np

# demo code


t0 = 0
cycles = 10            
ser = serial.Serial("/dev/ttyR1", baudrate=115200)  # open serial port
ssv_io.start_IO5640_stream(["uin4","uin3","uin2","uin1","iin1","iin2","iin3","iin4"], 100, ser)           
ser.reset_input_buffer()

t0a = time.time()

arr = []

for i in range(0, cycles):
    
    
    r = ssv_io.read_IO5640_stream_block(10, 8, ser, 5)
    arr.append(r)


t0b = time.time() 
t0 += t0b-t0a 

r = np.transpose(r)

cols = ["uin4","uin3","uin2","uin1","iin1","iin2","iin3","iin4"]
df = pd.DataFrame(data=r, columns=cols)

print(df)

df.to_csv("file.csv", index=False, columns=cols, header=True)

    
print("time t0:")
print(round((t0)*1000.0) / cycles)


ssv_io.stop_IO5640_stream(ser)

ser.close()

"""