import teca
import numpy as np

class TECAComponentCount:

    def __init__(self):
         return

    def get_execute_callback(self):
        def execute(port, data_in, md_in, req):
            # get the input mesh
            in_mesh = teca.as_teca_cartesian_mesh(data_in[0])

            ts = in_mesh.get_time_step()
            tsa = teca.teca_variant_array.New(np.array([ts],'int32'))

            md = in_mesh.get_metadata()
            try:
                num_ars = len(md['component_area'])
            except:
                num_ars = 0

            ncc = teca.teca_variant_array.New(np.array([num_ars],'int32'))

            tab = teca.teca_table.New()
            tab.append_column('step', tsa)
            tab.append_column('count', ncc)

            return tab

        return execute

class TECAMERRAARCounter:
    """ Counts ARs in MERRA output. This is designed to be run repeatedly after updates to the parameter inputs (i.e., MCMC).

        This pipeline is based explicitly on the pipeline defined in TECA/alg/teca_bayesian_ar_detect.cxx at revision 2104b37.

        The pipeline is reconstructed and modified here in order to obtain the counts of ARs in a batch of input files.

    """

    def __init__(self,
                  mesh_data_regex = "MERRA_test/ARTMIP_MERRA_2D_2017021.*\.nc$", \
                  water_vapor_variable = "IVT",
                  no_time_var = True,
                 ):

        # store the input arguments
        self.water_vapor_variable = water_vapor_variable
        self.mesh_data_regex = mesh_data_regex

        #*****************************
        # create the reader component
        #*****************************
        self.mesh_data_reader = teca.teca_cf_reader.New()
        self.mesh_data_reader.set_communicator(MPI.COMM_SELF)
        # set the filenames
        self.mesh_data_reader.set_files_regex(mesh_data_regex)
        # indicate that longitude is periodic
        self.mesh_data_reader.set_periodic_in_x(1)
        # set the lat/lon variables
        self.mesh_data_reader.set_x_axis_variable('lon')
        self.mesh_data_reader.set_y_axis_variable('lat')
        if no_time_var:
            # indicate that there is no time variable
            self.mesh_data_reader.set_t_axis_variable('')
        else:
            # set the time variable
            self.mesh_data_reader.set_t_axis_variable('time')

        #**************************************
        # create the latitude damper component
        #**************************************
        self.damp = teca.teca_latitude_damper.New()
        self.damp.set_communicator(MPI.COMM_SELF)
        # connect it to the reader
        self.damp.set_input_connection(self.mesh_data_reader.get_output_port())
        # set the variable for damping
        self.damp.set_damped_variables([water_vapor_variable])

        #**************************************
        # create the segmentation component
        #**************************************
        self.seg = teca.teca_binary_segmentation.New()
        self.seg.set_communicator(MPI.COMM_SELF)
        # connect it to the latitude dampber
        self.seg.set_input_connection(self.damp.get_output_port())
        # set the variable work on
        self.seg.set_threshold_variable(water_vapor_variable)
        # set the name of the output field of this component
        self.seg.set_segmentation_variable("wv_seg")
        # indicate that we are thresholding by percentile rather than absolute value
        self.seg.set_threshold_by_percentile()

        #******************************************
        # create the connected component algorithm
        #******************************************
        self.cc = teca.teca_connected_components.New()
        self.cc.set_communicator(MPI.COMM_SELF)
        # connect it to the segmentation algorithm
        self.cc.set_input_connection(self.seg.get_output_port())
        # set the variable name from the segmentation algorithm
        self.cc.set_segmentation_variable("wv_seg")
        # set the name of the output field
        self.cc.set_component_variable("wv_cc")

        #**************************************
        # create the component area calculator
        #**************************************
        self.ca = teca.teca_2d_component_area.New()
        self.ca.set_communicator(MPI.COMM_SELF)
        # connect it to the connected-component algorithm
        self.ca.set_input_connection(self.cc.get_output_port())
        # set the variable name from the connected-component algorithm
        self.ca.set_component_variable("wv_cc")
        # overwrite the component IDs with areas
        # TODO: check whether that's what this is doing
        self.ca.set_contiguous_component_ids(1)

        #**********************************
        # create the component area filter
        #**********************************
        self.caf = teca.teca_component_area_filter.New()
        self.caf.set_communicator(MPI.COMM_SELF)
        # connect it to the component area algorithm
        self.caf.set_input_connection(self.ca.get_output_port())
        # set the variable name from the connected component algorithm
        self.caf.set_component_variable("wv_cc")

        #****************************************
        # create the connected-component counter
        #****************************************
        # define an instance of a custom variable counter
        self.ccnt = TECAComponentCount()
        self.pa = teca.teca_programmable_algorithm.New()
        self.pa.set_communicator(MPI.COMM_SELF)
        # connect it to the component area filter
        self.pa.set_number_of_input_connections(1)
        self.pa.set_input_connection(self.caf.get_output_port())
        # set the execute function on this custom algorithm
        self.pa.set_execute_callback(self.ccnt.get_execute_callback())

        #**************************************************
        # create the table reduction and sorting algorithm
        #**************************************************
        self.mr = teca.teca_table_reduce.New()
        # connect the table reduction to the connected component counter
        self.mr.set_input_connection(self.pa.get_output_port())
        self.mr.set_verbose(1)
        self.mr.set_thread_pool_size(-1)
        self.mr.set_communicator(MPI.COMM_SELF)

        # define a table sorter
        self.ts = teca.teca_table_sort.New()
        self.ts.set_communicator(MPI.COMM_SELF)
        # connect it to the table reduction
        self.ts.set_input_connection(self.mr.get_output_port())
        # sort on the timestep, so that the areas are ordered the same as the
        # fields in the input file(s)
        self.ts.set_index_column('step')

        #************************
        # create a table-grabber
        #************************
        self.dsc = teca.teca_dataset_capture.New()
        self.dsc.set_input_connection(self.ts.get_output_port())

    def count(self,
              relative_value_threshold = 0.85,
              hwhm_latitude = 30.0,
              area_threshold = 1e12,
              filter_center = 0.0):
        """ Sets the parameters for the TECA pipeline, executes the pipline, and counts the connected components. """

        # set the pipeline parameters
        self.seg.set_low_threshold_value(relative_value_threshold*100)
        self.damp.set_half_width_at_half_max(hwhm_latitude)
        self.damp.set_center(filter_center)
        self.caf.set_low_area_threshold(area_threshold * 1e-6)

        print("start TECAMERRAARCounter.count({})".format((relative_value_threshold, hwhm_latitude, area_threshold)))

        # run the pipeline
        retval = self.dsc.update()

        print("end TECAMERRAARCounter.count({})".format((relative_value_threshold, hwhm_latitude, area_threshold)))

        # return a vector of the number of connected components in each field
        return np.asarray(teca.as_teca_table(self.dsc.get_dataset()).get_column('count'))

if __name__ == "__main__":
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    my_counter = TECAMERRAARCounter("/work2/data/teca/for_teca_data_svn/MERRA2/ARTMIP_MERRA_2D_20170218_.*\.nc$")
    if rank == 0:
        print(my_counter.count())
