import numpy as np
import os
import open3d as o3d

from tsdf_fusion import Fusion


'''
Run this script to test the averaging of two TSDFs from two different cars.
'''
def average_tsdf(tsdf_list, weights):
    """Function to average the tsdf
    """
    assert(len(tsdf_list) == len(weights))
    avg_tsdf = np.zeros(tsdf_list[0].shape)
    weights_sum = 0
    for tsdf, weight in zip(tsdf_list, weights):
        avg_tsdf += tsdf * weight
        weights_sum += weight
    avg_tsdf /= weights_sum
    return avg_tsdf


if __name__ == "__main__":
    print("Testing script for averaging two cars")

    # Set shape coefficient
    shape_coefficient = [0.5,0.5] # this is c

    # load off file
    suv_name = "aodi-Q7-SUV"
    sedan_name = "dazhong"
    depths_dir = "./examples/2_depth/"
    file_ext = ".off.h5"

    # load rendered depths
    suv_fpath = os.path.join(depths_dir, suv_name+file_ext)
    sedan_fpath = os.path.join(depths_dir, sedan_name+file_ext)
    model_paths = [suv_fpath, sedan_fpath]

    # fuse to generate tsdf
    app = Fusion()
    tsdf_list = app.get_tsdf(model_paths)

    # average two tsdf
    avg_tsdf = average_tsdf(tsdf_list, shape_coefficient)

    # averaged tsdf to mesh
    avg_mesh = app.tsdf_to_mesh([avg_tsdf])
    avg_mesh = avg_mesh[0]

    o3d_mesh = o3d.geometry.TriangleMesh()
    o3d_mesh.vertices = o3d.utility.Vector3dVector(avg_mesh['vertices'])
    o3d_mesh.triangles = o3d.utility.Vector3iVector(avg_mesh['triangles'])
    o3d_mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([o3d_mesh])
    #breakpoint()
