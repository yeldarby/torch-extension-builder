import subprocess

def get_ptcu_code():
    from torch.version import __version__, cuda
    torch_version = "".join(__version__.split(".")[:2])
    cuda_version = "".join(cuda.split("+cu")[-1].split("."))
    return "pt" + torch_version + "cu" + cuda_version

def unpack_wheel(wheel_path, directory=None):
    print("unpack", wheel_path, directory)
    if directory == None:
        try:
            subprocess.check_output(["python", "-m", "wheel", "unpack", wheel_path], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            print('1 error unpacking wheel: ', e.output)
            exit(1)
    else:
        try:
            subprocess.check_output(["python", "-m", "wheel", "unpack", wheel_path, "-d", directory], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            print('2 error unpacking wheel: ', e.output)
            exit(1)

def pack_wheel(input_directory, output_directory):
    subprocess.check_output(["python", "-m", "wheel", "pack", input_directory, "-d", output_directory])

def replace_dependancy(library, original_dep, new_dep):
    subprocess.check_output(["patchelf", "--replace-needed", original_dep, new_dep, library])
    
def write_rpath(library, rpath):
    subprocess.check_output(["patchelf", "--set-rpath", rpath, library])
