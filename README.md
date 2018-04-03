C# CLI Helper
=============

A little wrapper around the `dotnet` command. It can be useful
if you want to develop in .NET Core using the command-line.

    $ cs

    C# CLI Helper v0.2
    ==================
    option            what it does                         notes
    ------            ------------                         -----
    init              dotnet new console                   create a new project
    sample                                                 create / overwrite sample file Program.cs
    edit              code .                               launch VS Code
    comp              dotnet build                         compile only, build for local dev.
    exe [params]      dotnet bin/.../*.dll [params]        execute only, don't compile
    run [params]      dotnet run [params]                  compile and execute
    test              dotnet test *.csproj                 run unit tests on the project
    test sln          dotnet test *.sln                    run unit tests on the solution
    fdd               dotnet publish -o dist -c Release    a framework-dependent deployment (in the dist/ folder)
    scd [RID]         dotnet publish -o dist -c Release    a self-contained deployment (in the dist/ folder)
                          --runtime RID                      RID: runtime ID (ex.: win-x64, linux-x64 [default], osx-x64)
                                                             list of RIDs: https://goo.gl/8nNU2W
                                                             Deploying .NET Core apps with CLI tools: https://goo.gl/YAhpsQ
    select <fname.cs> [params]                             compile and execute the given source
                                                             Use this if you have multiple Main functions.
                                                             It uses the main_functions.txt file.
    proj                                                   show the absolute path of the .csproj file
    sln                                                    show the absolute path of the .sln file
    clean                                                  clean the project folder

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
