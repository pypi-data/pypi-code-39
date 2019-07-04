import edge_pydb
import h5py

fp = edge_pydb.getfiles('NGC4047.pipe3d.hdf5')
h5py.File(fp, 'r')