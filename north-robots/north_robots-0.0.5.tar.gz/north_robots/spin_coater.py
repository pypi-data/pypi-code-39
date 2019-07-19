from typing import Optional, List, Tuple
import time
import threading
from north_c9.controller import C9Controller
from north_c9.axis import RevoluteAxis, Output
from north_robots.robot import Robot


class SpinCoater(Robot):
    def __init__(self, controller: C9Controller, axis: int=0, lid_output: int=0, suction_output: int=1, home: bool=False):
        Robot.__init__(self, controller)
        self.axis = RevoluteAxis(controller, axis)
        self.cover = Output(controller, lid_output)
        self.suction = Output(controller, suction_output)
        self.spin_profile_thread: Optional[threading.Thread] = None
        self.spin_profile_running: bool = False

        if home:
            self.home()

    @property
    def spinning(self):
        return self.controller.axis_moving(self.axis)

    def home(self):
        self.axis.home()

    def open_cover(self):
        self.cover.on()

    def close_cover(self):
        self.cover.off()

    def suction_on(self):
        self.suction.on()

    def suction_off(self):
        self.suction.off()

    def spin(self, velocity_rpm: float, acceleration_rpm: float, duration: Optional[float]=None):
        self.axis.spin(velocity_rpm, acceleration_rpm, duration)

    def wait_for_stop(self):
        self.axis.wait()

    def spin_stop(self, profile_timeout: float=5.0, wait: bool=True):
        self.axis.spin_stop(wait=False)

        if self.spin_profile_thread is not None and self.spin_profile_running:
            self.spin_profile_running = False
            self.spin_profile_thread.join(timeout=profile_timeout)

        if wait:
            self.axis.wait()

    def run_spin_profile(self, profile: List[Tuple[int, int, float]], home: bool=True):
        self.spin_profile_running = True

        for velocity, acceleration, duration in profile:
            self.spin(velocity, acceleration)

            end_time = time.time() + duration
            while time.time() < end_time:
                if not self.spin_profile_running:
                    return

                time.sleep(0.01)

        self.spin_profile_running = False
        self.spin_stop(wait=True)

        if home:
            self.axis.home()

    def spin_profile(self, profile: List[Tuple[int, int, float]], wait: bool=True, home: bool=True):
        if wait:
            self.run_spin_profile(profile, home=home)
        else:
            self.spin_profile_thread = threading.Thread(target=self.run_spin_profile, args=[profile])
            self.spin_profile_thread.start()
