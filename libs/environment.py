import os
import libs.tools as tools

GOOGLE_TOOLCHAIN = {
    "arm":"https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/arm/arm-linux-androideabi-4.9",
    "arm64":"https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9"
}

class Environment():
    def __init__(self, userfiles: str):
        self.user_files = userfiles
        self.user_kernels = os.path.join(self.user_files, "Kernels")
        self.user_toolchains = os.path.join(self.user_files, "Toolchain")

    def setup(self):
        _folders = vars(self)
        for _key in _folders:
            tools.check_directory(_folders[_key])

    def get_toolchain(self, kernel_arch: str,
                            custom_toolchain_url: str = None):

        # Check for custom toolchain and download it.
        if custom_toolchain_url:
            _custom_dir = os.path.join(self.user_toolchains, "custom")
            if (os.path.exists(_custom_dir)):
                print("\n Custom toolchain already present in {}\n".format(_custom_dir))
            else:
                print("\n Downloading custom toolchain from {}\n".format(custom_toolchain_url))
                tools.git_clone(custom_toolchain_url, _custom_dir)
            return

        # Check for the current architecture toolchain and download it if missing.
        _toolchain_dir = os.path.join(self.user_toolchains, kernel_arch)
        if not (os.path.exists(_toolchain_dir)):
            print("\n Toolchain for {} not found, downloading automatically from google...\n".format(kernel_arch))
            tools.git_clone(GOOGLE_TOOLCHAIN[kernel_arch], _toolchain_dir)
        return

