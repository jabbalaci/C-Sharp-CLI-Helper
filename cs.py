#!/usr/bin/env python3

"""
C# CLI Helper

Goal: facilitate C# development in the command-line.

by Laszlo Szathmary (jabba.laci@gmail.com), 2018
"""

import os
import shlex
import sys
from glob import glob
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen


VERSION = "0.3"

ENV = {
    "TERM": "xterm"
}

MAIN_FUNCTIONS = "main_functions.txt"

CURRENT_DIR_NAME = Path(os.getcwd()).name

TEMPLATE = """
using System;
using static System.Console;
using System.Linq;
using System.Collections;
using System.Collections.Generic;

namespace SampleApp
{
    class Program
    {
        public static void Main(string[] args)
        {
            WriteLine("Hello World!");
        }
    }
}
""".strip().replace("SampleApp", CURRENT_DIR_NAME)

MAIN_FUNCTIONS_CONTENT = """
# Specify a filename and after the "=" sign indicate the
# namespace and the class that contains the Main function.
# That is, if you want to execute the file, then call the
# Main function in the given class.
""".lstrip()


def usage():
    old = """
pub         dotnet publish                         build the app. for deployment to other machines
                                                   deals with dependencies too
"""

    print("""
C# CLI Helper v{ver}
==================
option            what it does                         notes
------            ------------                         -----
init              dotnet new console                   create a new project
sample                                                 create / overwrite sample file Program.cs
edit              code .                               launch VS Code
restore           dotnet restore                       restore dependencies
comp              dotnet build                         compile only, build for local dev.
exe [params]      dotnet bin/.../*.dll [params]        execute only, don't compile
run [params]      dotnet run [params]                  compile and execute
test              dotnet test                          run unit tests (if *Test/ dir. was found, run on it)
fdd               dotnet publish -o dist -c Release    a framework-dependent deployment (in the dist/ folder)
scd [RID]         dotnet publish -o dist -c Release    a self-contained deployment (in the dist/ folder)
                      --runtime RID                      RID: runtime ID (ex.: win-x64, linux-x64 [default], osx-x64)
                                                         list of RIDs: https://goo.gl/8nNU2W
                                                         Deploying .NET Core apps with CLI tools: https://goo.gl/YAhpsQ
select <fname.cs> [params]                             compile and execute the given source
                                                         Use this if you have multiple Main functions.
                                                         It uses the main_functions.txt file.
open                                                   show the path of the .sln file
                                                         if not found, show the path of the .csproj file
ver                                                    version info
clean                                                  clean the project folder
""".strip().format(ver=VERSION))


def create_sample_file():

    def create_file():
        with open("Program.cs", "w") as f:
            f.write(TEMPLATE)

    if not os.path.isfile("Program.cs"):
        create_file()
        print("# sample file created")
    else:    # Program.cs exists
        res = input("> Program.cs exists. Overwrite (Y/n)? ").strip().lower()
        if res in ["", "y"]:
            create_file()
            print("# overwritten")
        else:
            print("# no")


def create_main_functions_file():
    if os.path.isfile(MAIN_FUNCTIONS):
        print("# Warning: the file {fname} already exists!".format(fname=MAIN_FUNCTIONS))
        return

    with open(MAIN_FUNCTIONS, "w") as f:
        print(MAIN_FUNCTIONS_CONTENT, file=f)
        print("Program.cs={ns}.Program".format(ns=CURRENT_DIR_NAME), file=f)


def check_if_in_project_dir():
    project_file = glob("./*.csproj")
    return len(project_file) > 0


def remove_dll():
    if not check_if_in_project_dir():
        print("# Error: it seems you are not in the root of a project folder!")
        return

    try:
        dll = glob("obj/Debug/netcoreapp*/*.dll")[0]
        os.unlink(dll)
        print("# {fname} was removed".format(fname=dll))
    except:
        pass


def read_value_from_file(fname):
    try:
        with open(MAIN_FUNCTIONS) as f:
            for line in f:
                line = line.rstrip("\n")
                if not line or line.startswith("#"):
                    continue
                parts = line.split("=")
                if parts[0] == fname:
                    return parts[1]
    except:
        return None
    #
    return None


def clean(dname):
    if not check_if_in_project_dir():
        print("# Error: it seems you are not in the root of a project folder!")
        return

    if os.path.isdir(dname):
        for fname in glob("{dir}/*".format(dir=dname)):
            os.unlink(fname)
        print("# {dir}/ cleaned".format(dir=dname))

    remove_dll()


def execute_command(cmd):
    """
    Execute a simple external command and return its exit status.
    """
    my_env = os.environ.copy()
    my_env.update(ENV)
    print('#', cmd)
    args = shlex.split(cmd)
    child = Popen(args, env=my_env)
    child.communicate()
    return child.returncode


def get_simple_cmd_output(cmd, stderr=STDOUT):
    """Execute a simple external command and get its output.

    The command contains no pipes. Error messages are
    redirected to the standard output by default.
    """
    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0].decode("utf8")


def version_info():
    dotnet = get_simple_cmd_output("dotnet --version").splitlines()[0]
    nuget = get_simple_cmd_output("nuget").splitlines()[0].replace(" V", "  V")
    print("dotnet version: {}".format(dotnet))
    print(nuget)


def process(args):
    param = args[0]
    params = " ".join(args[1:])
    exit_code = 0
    #
    if param == 'init':
        cmd = 'dotnet new console'
        exit_code = execute_command(cmd)
        #
        create_sample_file()
        create_main_functions_file()
        p = Path(glob("*.csproj")[0])
        print('#', p.absolute())
    elif param == 'sample':
        create_sample_file()
    elif param == 'edit':
        cmd = 'code .'
        exit_code = execute_command(cmd)
    elif param == 'run':
        cmd = 'dotnet run {params}'.format(params=params)
        exit_code = execute_command(cmd)
    elif param == 'restore':
        cmd = 'dotnet restore'
        exit_code = execute_command(cmd)
    elif param == 'test':
        cmd = 'dotnet test'
        #
        dirs = [entry for entry in os.listdir() if os.path.isdir(entry) and entry.endswith("Test")]
        if len(dirs) == 1:
            cmd = 'dotnet test {dname}'.format(dname=dirs[0])
        else:    # no Test dir. was found
            sln = glob("*.sln")
            if len(sln) == 1:
                cmd = 'dotnet test {sln}'.format(sln=sln[0])
            else:    # no .sln was found
                proj = glob("*.csproj")
                if len(proj) == 1:
                    cmd = 'dotnet test {proj}'.format(proj=proj[0])
        #
        exit_code = execute_command(cmd)
    elif param == 'select':
        fname = args[1]
        params = " ".join(args[2:])
        value = read_value_from_file(fname)
        if not value:
            print("# Error! The given file name was not found in {fname}!".format(fname=MAIN_FUNCTIONS))
        else:
            remove_dll()
            cmd = "dotnet build /p:StartupObject={value}".format(value=value)
            print("#", cmd)
            exit_code = execute_command(cmd)
            #
            cmd = 'dotnet run {params}'.format(params=params)
            exit_code = execute_command(cmd)
    elif param == 'comp':
        cmd = 'dotnet build'
        exit_code = execute_command(cmd)
    elif param == 'exe':
        dll = glob("bin/Debug/netcoreapp*/*.dll")[0]
        cmd = 'dotnet {dll} {params}'.format(dll=dll, params=params)
        exit_code = execute_command(cmd)
    elif param == 'pub':
        cmd = 'dotnet publish'
        exit_code = execute_command(cmd)
    elif param == 'fdd':
        cmd = 'dotnet publish -o dist -c Release'
        exit_code = execute_command(cmd)
    elif param == 'scd':
        rid = 'linux-x64'    # default
        try:
            rid = args[1]
        except IndexError:
            pass
        cmd = 'dotnet publish -o dist -c Release --runtime {rid}'.format(rid=rid)
        exit_code = execute_command(cmd)
    elif param == 'open':
        try:
            p = Path(glob("*.sln")[0])
            print(p.absolute())
        except:
            print("# no .sln file was found", file=sys.stderr)
            try:
                p = Path(glob("*.csproj")[0])
                print(p.absolute())
            except:
                print("# no .csproj file was found", file=sys.stderr)
    elif param == 'ver':
        version_info()
    elif param == 'clean':
        clean("dist")
    else:
        print("Error: unknown parameter")
    #
    return exit_code


def main():
    if len(sys.argv) == 1:
        usage()
        return 0;
    # else
    return process(sys.argv[1:])

##############################################################################

if __name__ == "__main__":
    exit(main())
