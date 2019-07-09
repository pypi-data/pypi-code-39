import machine


clk = None
data = None


def setup_leds():
    pin_clk = 13
    pin_data = 4

    global clk, data

    if clk is None and data is None:
        clk = machine.Pin(pin_clk, machine.Pin.OUT)
        data = machine.Pin(pin_data, machine.Pin.OUT)

        clk.value(0)
        data.value(0)


def __write_led_start_stop(dat):
    for i in range(32):
        data.value(dat & 1)  # constant data (SDI) signal
        clk.value(1)  # "sending the data signal" on each switch => 32 times
        clk.value(0)
        dat = dat >> 1


def _write_start_frame():
    __write_led_start_stop(0)


def _write_end_frame():
    __write_led_start_stop(~0)


def __write_global_brightness(gl):
    for i in range(5):
        data.value(gl & (1 << (4 - i)))
        clk.value(1)
        clk.value(0)


def __write_rgb(r, g, b):
    for c in [r, g, b]:
        for i in range(8):
            data.value(c & (1 << (7 - i)))
            clk.value(1)
            clk.value(0)


def _write_color(r, g, b, gl):
    __write_global_brightness(gl)
    __write_rgb(r, g, b)


def _write_LED_frame(brightness=0, blue=0, green=0, red=0):
    def _write_LED_frame_start():
        data.value(1)
        for i in range(3):
            clk.value(1)
            clk.value(0)

    _write_LED_frame_start()

    _write_color(red, green, blue, brightness)


def write_LED_CDS(led_settings):
    _write_start_frame()
    for settings in led_settings:
        _write_LED_frame(**settings)
    _write_end_frame()


def write_shutoff_frame():
    _write_start_frame()
    _write_LED_frame(0, 0, 0, 0)
    _write_LED_frame(0, 0, 0, 0)
    _write_LED_frame(0, 0, 0, 0)
    _write_LED_frame(0, 0, 0, 0)
    _write_end_frame()


LEDs = [{
    'brightness': 0,
    'blue': 0,
    'green': 0,
    'red': 0
    },
    {
        'brightness': 0,
        'blue': 0,
        'green': 0,
        'red': 0
    },
    {
        'brightness': 0,
        'blue': 0,
        'green': 0,
        'red': 0
    },
    {
        'brightness': 0,
        'blue': 0,
        'green': 0,
        'red': 0
    }
]
