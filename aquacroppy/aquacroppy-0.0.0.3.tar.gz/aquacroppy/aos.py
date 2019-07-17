"""
Python port of the AquaCropOS codebase for the WAVES lab at UCSB
variables and calculations are generally along the lines of those from
AquaCrop. 
Read about their methods: http://www.fao.org/3/a-br248e.pdf
"""

import logging
import arrow
from .utils import keyword_value
from .elements import read_weather_inputs, Crop, Crops, Soil

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


class AOS:
    """
    AquaCropPy's main class. Similar to a high level view of the entry point of
    Aquacrop_RUN.mat in the Matlab version of Aquacrop
    """

    def __init__(self, input_directory="./Input"):
        """Defining initial values to the class variables. The AOS class is
        written to loosely mimic the data structures of the original Matlab
        implementation"""
        self.elapsed = 0
        self.running = False
        self.start = None
        self.end = None
        self.off_season = None
        self.total_days = 0
        self.weather = None
        self.soil = None
        self.crops = None
        self.input_directory = input_directory

        # Populating class variables to real values
        self.read_inputs(self.input_directory)

    def read_inputs(self, in_dir):
        """Read each input file. Populating the AOS object with attributes like
        those of AOS_InitializeStruct in the Matlab code.

        Function called from within __init__. Must be called before run()

        :param in_dir: input directory that contains all the input files

        :returns: True
        """
        # TODO: write this as an abstract class & raise 'not implemented error'
        # https://docs.python.org/3/library/exceptions.html#NotImplementedError

        # TODO perhaps a JSON object of a certain shape which defined all
        # inputs would be better suited for this use case

        # This implementation aims to have all the input files in one method
        # Even though they are 'hard-coded' it seems to be a move in the right
        # direction over the previous iteration

        logging.debug("Reading Inputs")
        self.define_run_time("{}/Clock.txt".format(in_dir))

        # Weather
        self.weather = read_weather_inputs("{}/Weather.txt".format(in_dir))

        # Soil
        self.soil = Soil(
            in_dir=in_dir, 
            soil_file="/Soil.txt", 
            soil_profile_file="/SoilProfile.txt"
        )

        # Crops
        crop_dict = {}
        crop_dict["Quinoa"] = [
            "Quinoa.txt",
            "IrrigationManagement.txt",
            "IrrigationSchedule.txt",
        ]
        lst = []
        for i in crop_dict["Quinoa"]:
            lst.append("./Input/{}".format(i))

        crop_dict["Quinoa"] = lst

        planting_calendar = "{}/PlantingCalendar.txt".format(in_dir)

        self.crops = Crops(planting_calendar, crop_dict)
        return self

    def define_run_time(self, path_to_clock_file):
        """Simplified method to read from the Clock file to define simulation
           run time

           :param path_to_clock_file: tells us where to find the file
           :pre-condition: 4 time based attibutes are initialized to None
           :post-condition: 4 time based attributes are set for this object
               start
               end
               off_season
               total_days
           """
        logging.debug("  Defining run time")
        input_file = open(path_to_clock_file, "r")
        for line in input_file:
            if line.count("SimulationStartTime"):
                start = keyword_value(line)
            if line.count("SimulationEndTime"):
                end = keyword_value(line)
            if line.count("OffSeason"):
                self.off_season = keyword_value(line)
        input_file.close()

        self.start = arrow.get(start, "YYYY-MM-DD")
        self.end = arrow.get(end, "YYYY-MM-DD")
        assert start < end
        self.total_days = (self.end - self.start).days
        logging.debug("    %s days", str(self.total_days))

    def termination(self):
        """Check to see if the the simulated days elapsed matches total days to
        simulate
           :param: None
           :returns: Boolean
           """
        return self.total_days == self.elapsed

    def __str__(self):
        return "AOS simulating " + str(self.elapsed)

    def _perform_time_step(self):
        """Increment the elapsed time simulation
        This is the most involved step

        for example:
          %% Get weather inputs for current time step %%
          Weather = AOS_ExtractWeatherData();

          %% Get model solution %%
          [NewCond,Outputs] = AOS_Solution(Weather);

          %% Update initial conditions and outputs %%
          AOS_InitialiseStruct.InitialCondition = NewCond;
          AOS_InitialiseStruct.Outputs = Outputs;

          %% Check model termination %%
          AOS_CheckModelTermination();

          %% Update time step %%
          AOS_UpdateTime();
        """
        if (self.elapsed % 200) == 0:
            logging.debug(self)
            # Solution goes here
            # refer to chapter 1 in handbook
            # for explanations of variables
            # involved in solution calculations
        self.elapsed += 1

    def finish(self):
        """Finish method to write outputs"""
        logging.debug("Finishing AOS")
        self.running = False

    def run(self):
        """Run the model according to the input parameters"""
        self.running = True
        while self.termination() is False:
            self._perform_time_step()
        self.finish()
