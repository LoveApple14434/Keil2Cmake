# Keil2Cmake Converter

## env requirement
- Python3
- Cmake
- Ninja
- Keil compilor

## before use
Before your first use, turn to **line 202** and fill in **your own keil path** installed on your PC.

In case that you do not know how to find it, open keil and open Windows task manager, in which right click the Keil task, open the path and just copy it into [Convert.py line 202](./Convert.py).



## usage
### 0.generate scatter file through keil
Aug 03 2025: I added a new function to generate a scatter file for you, so in most cases you do not need to do it any more. It should work for most STM32 MCUs. If it does not work in your case, replace it with your own scatter file as below.

>Open the keil project you want to convert. Assure it **has >been built** once at least.
>
>Open **'Options for Target'**, turn to **'Linker'** page, >unselect the **'Use Memory Layout for Target Dialog'**, then >press **'Edit'** button below, and keil will automatically >generate a Template.sct for you. 
>
>Close Keil and head onto the next step.

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

## Configure Toolchain Path

Toolchain path should be stored in `~/.keil2cmake/path.cfg` . Use commands as follow to view or edit the paths:

```bash
keil2cmake --show-config
keil2cmake -sc

keil2cmake --edit ARMCC_PATH=D:/Program/Keil_v5/ARM/ARM_Compiler_5.06u7/bin/
keil2cmake -e ARMCC_PATH=D:/Program/Keil_v5/ARM/ARM_Compiler_5.06u7/bin/
keil2cmake --edit ARMCLANG_PATH=D:/Program/Keil_v5/ARM/ARMCLANG/bin/
keil2cmake -e ARMCLANG_PATH=D:/Program/Keil_v5/ARM/ARMCLANG/bin/
```