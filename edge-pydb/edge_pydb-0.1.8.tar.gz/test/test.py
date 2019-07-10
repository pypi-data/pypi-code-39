import edge_pydb
import h5py
import os

fp = edge_pydb.getfiles('NGC4047.pipe3d.hdf5')
h5py.File(fp, 'r')

# print(os.path.abspath(__file__))
# edge_pydb.Addfile('./build.sh')
# edge_pydb.listfiles('.sh')

# edge_pydb.AddDir('./dist', overwrite=True)
# edge_pydb.listfiles('.whl')
edge_pydb.listfiles()