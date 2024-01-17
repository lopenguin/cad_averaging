import os, sys
import copy
import open3d as o3d

if __name__ == "__main__":
    print("Converting .off model files to .ply files")
    off_dir = "./car_models/hole_fixed/2_watertight_frame_fixed"
    ply_dir = "./car_models/hole_fixed/2_watertight_frame_fixed_ply"
    off_files = [f for f in os.listdir(off_dir) if os.path.isfile(os.path.join(off_dir, f))]
    for off_fname in off_files:

        off_path = os.path.join(off_dir, off_fname)
        mesh_data = o3d.io.read_triangle_mesh(off_path)
        ply_fname = off_fname.split(".")[0] + ".ply"
        ply_path = os.path.join(ply_dir, ply_fname)
        o3d.io.write_triangle_mesh(ply_path, mesh_data)
