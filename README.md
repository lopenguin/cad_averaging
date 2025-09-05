# Averaging CAD Models Using TSDF Fusion
This repository shows one way to generate a CAD model from a linear combination of other CAD models. It is compiled by Lorenzo Shaikewitz using code mostly written by Jingnan Shi and based heavily on David Stutz and Andreas Geiger's TSDF fusion library.

If you use any of this code, please make sure to cite the original work:

    @article{Stutz2018ARXIV,
        author    = {David Stutz and Andreas Geiger},
        title     = {Learning 3D Shape Completion under Weak Supervision},
        journal   = {CoRR},
        volume    = {abs/1805.07290},
        year      = {2018},
        url       = {http://arxiv.org/abs/1805.07290},
    }

## Setup
### Dependencies
- [pyfusion](https://github.com/griegler/pyfusion) requires CMake and Cython; optionally it uses CUDA or OpenMP for efficiency.
- [pyrender](https://github.com/griegler/pyrender) requires Cython, as well. Additionally, it requires OpenGL, GLUT and GLEW, see `librender/setup.py`
- [PyMCubes](https://github.com/pmneila/PyMCubes) requires Cython.

Note that all 3 libraries are included in this repo.

<!-- **Update:** For newer CUDA versions/GPU architectures, the CMAKE file in `libfusiongpu` needs to be adapted as outlined in [this issue](https://github.com/davidstutz/mesh-fusion/issues/6). -->

### Build and Install Package
For building follow (illustrated for the CPU version):

    # build pyfusion
    # use libfusiongpu alternatively!
    cd libfusioncpu
    mkdir build
    cd build
    cmake ..
    make
    cd ..
    python setup.py build_ext --inplace
    
    cd ..
    # build pyrender
    cd librender
    python setup.py build_ext --inplace
    
    cd ..
    # build PyMCubes
    cd libmcubes
    python setup.py build_ext --inplace

## Usage
Usage is illustrated on the shipped examples in `examples/0_in` taken from ApolloScape. 3D models must begin as .off files. We have included a ply to off conversion script for convenience.

### 3D Model Conversion
Before averaging, we convert the 3D models into a form that can be easily converted into a TSDF. This only needs to be done once for the 3D model database.

**First**, scale the models using:

    python 1_scale.py --in_dir=examples/0_in/ --out_dir=examples/1_scaled/ --transform_out_dir=examples/1_transform

**Now** the models can be rendered, per default, 100 views (uniformly sampled
on a sphere) will be used:

    python 2_fusion.py --mode=render --in_dir=examples/1_scaled/ --depth_dir=examples/2_depth/ --out_dir=examples/2_watertight/

If you are using the gpu to render you must change the flag inside `2_fusion.py`. This may take a while on CPU.

The details of rendering can be controlled using the following options:

    --n_views N_VIEWS     Number of views per model.
    --image_height IMAGE_HEIGHT
                          Depth image height.
    --image_width IMAGE_WIDTH
                          Depth image width.
    --focal_length_x FOCAL_LENGTH_X
                          Focal length in x direction.
    --focal_length_y FOCAL_LENGTH_Y
                          Focal length in y direction.
    --principal_point_x PRINCIPAL_POINT_X
                          Principal point location in x direction.
    --principal_point_y PRINCIPAL_POINT_Y
                          Principal point location in y direction.
    --depth_offset_factor DEPTH_OFFSET_FACTOR
                          The depth maps are offsetted using
                          depth_offset_factor*voxel_size.
    --resolution RESOLUTION
                          Resolution for fusion.
    --truncation_factor TRUNCATION_FACTOR
                          Truncation for fusion is derived as
                          truncation_factor*voxel_size.

During rendering, a small offset is added to the depth maps. This is particular
important for meshes with thin details, as for example the provided chairs.
Essentially, this thickens the structures. In the code, the offset is computed as

    voxel_size = 1/resolution
    offset = depth_offset_factor*voxel_size

**Note that rendering is split as rendering might not work on all machines,
especially remotely (e.g. through ssh) on machines without monitor.**

### Averaging
A simple example is given in [tsdf_avg.py](tsdf_avg.py). Simply run this script with `python tsdf_avg.py` to see the result of averaging two cars. You may change the shape cofficient by editing the corresponding variable in the file.

For a more advanced example, the script [tsdf_morphing_animation.py](tsdf_morphing_animation.py) can be used to generate video frames. Simply call `python tsdf_morphing_animation.py` to run. Note that it may be slow. You can stitch these frames into a video using:

    ffmpeg -r 30 -f image2 -i 'car_morphing_%4d.jpg' -vcodec libx264 -crf 25 -pix_fmt yuv420p car_morphing.mp4

## Troubleshooting the install:
1. Install the old numpy: `pip install "numpy<2.0"`
2. Install glut: `sudo apt install freeglut3-dev`
3. Install glew: `sudo apt-get install libglew-dev`
4. Compile with gcc12: `cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_C_COMPILER=/usr/bin/gcc-12 .`

## Acknoweldgements
The source code is heavily based on [mesh-fusion](https://github.com/davidstutz/mesh-fusion). Included below is their license statement.

D. Stutz, A. Geiger. **Learning 3D Shape Completion under Weak Supervision.** International Journal of Computer Vision (2018).

Note that the source code and/or data is based on the following projects for which separate licenses apply:

* [pyrender](https://github.com/griegler/pyrender)
* [pyfusion](https://github.com/griegler/pyfusion)
* [PyMCubes](https://github.com/pmneila/PyMCubes)

Original source code is copyright (c) 2018 David Stutz, Max-Planck-Gesellschaft

**Please read carefully the following terms and conditions and any accompanying documentation before you download and/or use this software and associated documentation files (the "Software").**

The authors hereby grant you a non-exclusive, non-transferable, free of charge right to copy, modify, merge, publish, distribute, and sublicense the Software for the sole purpose of performing non-commercial scientific research, non-commercial education, or non-commercial artistic projects.

Any other use, in particular any use for commercial purposes, is prohibited. This includes, without limitation, incorporation in a commercial product, use in a commercial service, or production of other artefacts for commercial purposes.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

You understand and agree that the authors are under no obligation to provide either maintenance services, update services, notices of latent defects, or corrections of defects with regard to the Software. The authors nevertheless reserve the right to update, modify, or discontinue the Software at any time.

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. You agree to cite the corresponding papers (see above) in documents and papers that report on research using the Software.