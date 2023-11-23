C# CLI Helper
=============

A little wrapper around the `dotnet` command. It can be useful
if you want to develop in .NET using the command-line.

It was tested with .NET 7 under Linux.

    $ cs

    C# CLI Helper v0.3.5
    ====================
    option            what it does                         notes
    ------            ------------                         -----
    init              dotnet new console                   create a new project
    sample                                                 create / overwrite sample file Program.cs (v1)
    sample2                                                create / overwrite sample file Program.cs (v2)
    edit              code .                               launch VS Code
    restore           dotnet restore                       restore dependencies
    add <pkg>         dotnet add package <pkg>             add the given package as a dependency
    proj              cat *.csproj                         show the content of the .csproj file
    comp              dotnet build                         compile only, build for local dev.
    exe [params]      dotnet bin/.../*.dll [params]        execute only, don't compile
    run [params]      dotnet run [params]                  compile and execute
    test              dotnet test                          run unit tests (if *Test/ dir. was found, run on it)
    fdd               dotnet publish -o dist -c Release    a framework-dependent deployment (in the dist/ folder)
    scd [RID]         dotnet publish -o dist -c Release    a self-contained deployment (in the dist/ folder)
                        --runtime RID                      RID: runtime ID (ex.: win-x64, linux-x64 [default], osx-x64)
                                                            list of RIDs: https://goo.gl/8nNU2W
                                                            Deploying .NET Core apps with CLI tools: https://goo.gl/YAhpsQ
    scd1                                                   like `scd`, but it produces a single (but big) EXE file
    scd1s                                                  like `scd1`, but it produces a smaller, single EXE file
    open                                                   show the path of the .sln file
                                                            if not found, show the path of the .csproj file
    ver                                                    version info
    space                                                  show disk usage of the project folder
    clean                                                  clean the project folder (remove bin/, dist/, obj/)


Example
-------

Create a new project:

    $ cd projects
    $ mkdir Hello
    $ cd Hello
    $ cs init

Compile and run the program:

    $ cs run

Pass some command-line parameters:

    $ cs run 2 3

Create a self-contained deployment for Windows:

    $ cs scd win-x64
