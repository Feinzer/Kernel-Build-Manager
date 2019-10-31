import os, json
import libs.tools as tools

TOOLCHAIN_PREFIX = {
    "arm":os.path.join(
        "arm",
        os.path.join("bin", "arm-linux-androideabi-")
    ),
    "arm64":os.path.join(
        "arm64",
        os.path.join("bin", "aarch64-linux-android-")
    )
}

class Kernel():
    def __init__(self, 
                name: str,
                version: str,
                arch: str,
                target_android: str,
                stable_release: bool,
                device_codename: str,
                defconfig: str,
                auto_dtb: bool,
                clean_build: bool,
                configs_dir: str,
                toolchains_dir: str,
                custom_toolchain_dir: str = None):
        self.name = name
        self.config_dir = os.path.join(configs_dir, self.name)
        self.source_code = os.path.join(self.config_dir, "source")
        self.version = version
        self.arch = arch
        self.target_android = target_android
        self.stable_release = stable_release
        self.device_codename = device_codename
        self.defconfig = defconfig
        self.auto_dtb = auto_dtb
        self.clean_build = clean_build

        if (custom_toolchain_dir and os.path.exists(custom_toolchain_dir)):
            self.toolchain = custom_toolchain_dir
        else:
            self.toolchain = os.path.join(
                toolchains_dir,
                TOOLCHAIN_PREFIX[self.arch]
            )
            if (self.arch == "arm64"):
                self.toolchain32 = os.path.join(
                    toolchains_dir,
                    TOOLCHAIN_PREFIX["arm"]
                )

    def create_config(self):
        if (os.path.exists(self.config_dir)):
            raise FileExistsError("Kernel already exists")
        os.makedirs(self.config_dir)
        
        if not (os.path.exists(self.source_code)):
            _select = input("Clone kernel source from git repository? [Y/N]: ")
            if(_select == "Y" or _select == "y"):
                _git_url = input("Git URL: ")
                _git_branch = input("Branch: ")
                tools.git_clone(_git_url, self.source_code, _git_branch)
            else:
                os.makedirs(self.source_code)
        
        self.save_config()

    def save_config(self):
        _config_file = os.path.join(self.config_dir, "config.json")
        _config = vars(self)
        with open(_config_file, 'w') as _output:
            json.dump(_config, _output, indent=4)

    def build(self):
        if not (os.path.exists(self.source_code)):
            raise FileNotFoundError("Kernel source code not found")

        print("\n\n Started build for {name} {version} {arch}".format(
            name = self.name,
            version = self.version,
            arch = self.arch
        ))

        # Clean source code before compilation
        if (self.clean_build):
            print("\n - Cleaning up the source code")
            tools.run_command("make clean", self.source_code)

        # Load selected defconfig
        print("\n - Loading {defconfig} for {device} {arch}".format(
            defconfig = self.defconfig,
            device = self.device_codename,
            arch = self.arch
        ))
        tools.run_command("make {}".format(self.defconfig),
                          self.source_code,
                          ["ARCH={}".format(self.arch)])

        # Declaration for necessary variables.
        _variables = [
            "KCONFIG_NOTIMESTAMP=true",
            "ARCH={}".format(self.arch),
            "SUB_ARCH={}".format(self.arch),
            "CROSS_COMPILE={}".format(self.toolchain),
        ]

        # Add CROSS_COMPILE_ARM32 for some devices
        if (self.arch == "arm64"):
            _variables.append("CROSS_COMPILE_ARM32={}".format(self.toolchain32))

        # Start compiling.
        print("\n\n")
        tools.run_command("make -j$(nproc)",
                          self.source_code,
                          _variables)
