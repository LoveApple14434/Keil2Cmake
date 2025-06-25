# Keil2Cmake Converter

## env requirement
-Python3
-Cmake
-Ninja
-Keil compilor

## before use
Before your first use, turn to line 202 and fill in your own keil path installed on your PC.

In case that you do not know how to find it, open keil and open Windows task manager, in which right click the Keil task, open the path and just copy it into Convert.py line 202.

## usage
### 1.generate CMakeLists.txt and toolchain.cmake according to uvprojx file
In any command line, do
```bash
Python <path/to/Convert.py> <path/to/uvision/file.uvprojx> -o <path/to/output/directory>
```
For example, I would copy Convert.py into the root dir of one project, open pwsh in that dir, and do
```bash
Python ./Convert.py ./USER/example.uvprojx -o .
```
and then the CMakeLists.txt and toolchain.cmake will be generated at ./

### 2.generate build chain and build it
In the dir mentioned above, do in command line
```bash
CMake -G Ninja -B build .
CMake --build build
```
Then your build target(.hex and .bin) will be generated in ./build/. Then use FLYMCU or ST-Link Utility or anything you like to burn it into your MCU.