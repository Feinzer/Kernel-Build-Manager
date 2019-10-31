import os, subprocess

def check_directory(dir: str):
    if not (os.path.exists(dir)):
        os.makedirs(dir)

def run_command(command: str,
                working_dir: str = None,
                exports: list() = None):
    to_run = ""

    if exports:
        for var in exports:
            to_run += "export {} && ".format(var)

    to_run += command

    return subprocess.run(
        ["/bin/bash", "-c", to_run],
        cwd=working_dir
    )

def git_clone(url: str,
              clone_dir: str,
              branch: str = None):
    command = "git clone {url} {dir}".format(
        url = url,
        dir = clone_dir
    )

    if (branch):
        command += "-b {}".format(branch)

    run_command(command)