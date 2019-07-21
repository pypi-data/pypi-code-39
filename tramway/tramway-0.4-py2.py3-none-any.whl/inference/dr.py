import numpy as np

# The `setup` variable is required, should it be empty.
# Define the output variable name in `setup['returns']`
setup = {'returns': ['displacement_size']}

# Either choose a function name that begins with 'infer' or specify the function name in `setup['infer']`
def infer(cells, quantile=1):

    # The `cells` dict-like object is the only compulsory input argument provided by `tramway.helper.inference.infer`.
    # The other input arguments are free.

    # To make the `quantile` argument available in the `tramway infer dr` command, define:
    #    setup['arguments'] = {'quantile': dict(type=float, default=1, help="quantile of the displacement amplitude")}
    # This will make the following command possible: `tramway infer dr --quantile .5`
    # The dict associated with the 'quantile' key contains arguments to `add_parser` (`argparse` library).
    for i in cells:
        cell = cells[i]

        # Attribute `dr` is a N*D ndarray with N the number of displacements (guaranteed not to be null) and D the dimension
        dr_norms = np.sqrt(np.sum(cell.dr * cell.dr, axis=1))

        # Attribute `displacement_size` is avaible thanks to `setup['returns']`;
        # note that attribute name 'dr' is reserved.
        cell.displacement_size = np.quantile(dr_norms, quantile)

        # That's all!
        # Copy this file into the tramway/inference directory and try `infer(my_file.rwa, 'dr')`.
        # The resulting DataFrame will exhibit a 'displacement_size' column.

