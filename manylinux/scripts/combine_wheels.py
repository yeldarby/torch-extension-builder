from distutils import dir_util
import os
import glob
import shutil
import argparse
from subprocess import check_output

import utils

import inspect

IMPORT_WRAPPER_TEMPLATE = inspect.getsource(utils.get_ptcu_code) + '''
def __bootstrap__():
    global __bootstrap__, __loader__, __file__
    import sys, pkg_resources, imp
    __file__ = pkg_resources.resource_filename(__name__, '{0}.so.' + get_ptcu_code())
    __loader__ = None; del __bootstrap__, __loader__
    imp.load_dynamic(__name__,__file__)
__bootstrap__()
'''

def wrap_libraries(wheel_dir):

    all_libraries = glob.glob(f"{wheel_dir}/*.so.*")
    library_files = list(set([lib.split("/")[-1].split(".so.")[0] for lib in all_libraries]))
    library_names = [file.split(".")[0] for file in library_files]

    for lib_name, lib_file in zip(library_names, library_files):
        wrapper_file_text = IMPORT_WRAPPER_TEMPLATE.format(lib_file)
        
        with open(wheel_dir + "/" + lib_name + ".py", "w") as f:
            f.write(wrapper_file_text)

def combine_wheels(wheels, output_dir="combined_wheels"):
    
    print("Combining wheels...")
    map(print, wheels)

    wheel_file = os.path.basename(wheels[0])
    wheel_name = wheel_file.split(".whl.")[0]
    work_dir = "-".join(wheel_name.split("-")[0:2])

    distribution, version = wheel_name.split('-')[0:2]

    # replace manylinux2014_x86_64.manylinux_2_17_x86_64.whl
    # with manylinux_2_17_x86_64.whl in wheel_name
    wheel_name = wheel_name.replace("manylinux2014_x86_64.", "")

    for wheel in wheels:
        wheel_tag = wheel.split(".whl.")[-1]
        print("rename", wheel, wheel_name)

        os.rename(wheel, f"{wheel_name}.whl")
        utils.unpack_wheel(f"{wheel_name}.whl")
        os.rename(f"{wheel_name}.whl", wheel)
        
        for library in glob.glob(f"{work_dir}/*.so"):
            os.rename(library, f"{library}.{wheel_tag}")
    
    print("Wrapping libraries...")
    wrap_libraries(work_dir)

    # Correcting the WHEEL metadata
    print("Correcting the WHEEL metadata...")
    wheel_metadata_file = os.path.join(work_dir, f"{distribution}-{version}.dist-info", 'WHEEL')
    with open(wheel_metadata_file, 'r') as f:
        lines = f.readlines()
    with open(wheel_metadata_file, 'w') as f:
        for line in lines:
            if line.strip().startswith('Tag') and 'manylinux2014_x86_64' in line:
                continue
            f.write(line)

    dir_util.mkpath(output_dir)
    print("Packing wheel...")
    utils.pack_wheel(work_dir, output_dir)
    shutil.rmtree(work_dir)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Combine wheel files comompiled with different versions of PyTorch and CUDA.')
    parser.add_argument('wheels', type=str, nargs='+', help='The wheel files to be combined.')
    args = parser.parse_args()

    print("COMBINE", args.wheels)
    combine_wheels(args.wheels)
