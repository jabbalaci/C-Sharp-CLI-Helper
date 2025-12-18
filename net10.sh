#!/usr/bin/env bash

# Warning! It modifies the .csproj file **in-place**!

sed -i "s/net8.0/net10.0/g" *.csproj
sed -i "s/net9.0/net10.0/g" *.csproj
