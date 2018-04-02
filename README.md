C# CLI Helper
=============

    $ cs

    C# CLI Helper v0.2
    ------------------
    init              dotnet new console                   create a new project
    sample                                                 create / overwrite sample file Program.cs
    edit              code .                               launch VS Code
    comp              dotnet build                         compile only, build for local dev.
    exe [params]      dotnet bin/.../*.dll [params]        execute only, don't compile
    run [params]      dotnet run [params]                  compile and execute
    test              dotnet test *.csproj                 run unit tests on the project
    test sln          dotnet test *.sln                    run unit tests on the solution
    fdd               dotnet publish -o dist -c Release    a framework-dependent deployment (output: in the dist/ folder)
    scd [RID]         dotnet publish -o dist -c Release    a self-contained deployment (output: in the dist/ folder)
                        --runtime RID                        RID: runtime ID (ex.: win-x64, linux-x64 [default], osx-x64)
                                                            list of RIDs: https://docs.microsoft.com/en-us/dotnet/core/rid-catalog
                                                            Deploying .NET Core apps with CLI tools: https://goo.gl/YAhpsQ
    select <fname.cs> [params]                             compile and execute the given source
                                                            Use this if you have multiple Main functions.
                                                            It uses the main_functions.txt file.
    clean                                                  clean the project folder
