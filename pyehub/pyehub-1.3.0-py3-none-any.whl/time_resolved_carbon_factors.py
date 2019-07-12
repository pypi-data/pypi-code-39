import os
import csv
from pyehub.outputter import pretty_print
from pyehub.energy_hub.ehub_model import EHubModel
from pyehub.energy_hub.utils import constraint, constraint_list
from pprint import pprint as pp

#TODO: Replace in the main model the data.carbon_factors with the actual time resolved time series from the SILVER CSV
# self.CARBON_FACTORS = data.carbon_factors

with open('hourly_GHG_emission.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    count = 0
    gen_list = []
    date_list = []
    carbon_factors = {}
    for row in readCSV:
        length = len(row)
        for column in range(length):
           #Note each generator
            if(count == 0):
                if(column!=0):
                    gen_list.append(row[column])
            #Make a key for each timeseries
            else:
                if(column==0):
                    date_list.append(row[column])
                    carbon_factors[row[column]] = {}
                    for key in gen_list:
                        carbon_factors[row[column]][key]= {}
                else:
                    carbon_factors[date_list[count-1]][gen_list[column-1]]=row[column]

        count += 1
        
carbon_factors.pop('kind')
#     pp(carbon_factors)
# pp(carbon_factors[gen_list[63]][date_list[-1]])
# pp(gen_list)
# print(length)
#     pp(date_list)
pp(carbon_factors)
    

class TimeResolvedCarbon(EHubModel):
    """
    A custom EHubModel to include the time resolved carbon factors from the Silver model
    instead of using the averaged carbon factors for each input stream.
    """
    #TODO: Override the calc_total_carbon constraint to use the time series instead. 
    #(currently I've added the default here.)
    @constraint()
    def calc_total_carbon(self):
        """A constraint for calculating the total carbon produced."""
        total_carbon_credits = 0
        for stream in self.export_streams:
            # if carbon credits for a stream are a time series
            if self.CARBON_CREDITS[stream] in self.TIME_SERIES:
                for t in self.time:
                    carbon_credit = self.TIME_SERIES[self.CARBON_CREDITS[stream]][t]
                    energy_exported = self.energy_exported[t][stream]
                    total_carbon_credits += carbon_credit * energy_exported
            else:
                total_energy_exported = sum(self.energy_exported[t][stream]
                                            for t in self.time)
                carbon_credit = self.CARBON_CREDITS[stream]
                total_carbon_credits += carbon_credit * total_energy_exported

        total_carbon_emissions = 0
        for stream in self.import_streams:
            # if carbon factors for a stream are a time series
            if self.CARBON_FACTORS[stream] in self.TIME_SERIES:
                for t in self.time:
                    carbon_factor = self.TIME_SERIES[self.CARBON_FACTORS[stream]][t]
                    energy_used = self.energy_imported[t][stream]
                    total_carbon_emissions += carbon_factor * energy_used
            else:
                total_energy_used = sum(self.energy_imported[t][stream]
                                        for t in self.time)
                carbon_factor = self.CARBON_FACTORS[stream]
                total_carbon_emissions += carbon_factor * total_energy_used

        return self.total_carbon == total_carbon_emissions - total_carbon_credits

