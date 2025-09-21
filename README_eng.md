# Keil2Cmake Converter

Sep 21 2025: I have generated executable file for Windows and Linux using Pyinstaller. Download and use them through [GitHub release](https://github.com/LoveApple14434/Keil2Cmake/releases/tag/v1). Now you don't need python on your Computer anymore.
## env requirement
- ~~Python3~~
- Cmake
- Ninja
- Keil compilor


## before use

Sep 21 2025: Now you don't need to fill in your path in the code anymore. But you still need to configure the paths in command line when you first use keil2cmake. See [Configure Toolchain Path](#configure-toolchain-path) instead.

~~Before your first use, turn to **line 202** and fill in **your own keil path** installed on your PC.~~

~~In case that you do not know how to find it, open keil and open Windows task manager, in which right click the Keil task, open the path and just copy it into [Convert.py line 202](./Convert.py).~~

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

## usage
### 0. Generate scatter file through keil
Aug 03 2025: I added a new function to generate a scatter file for you, so **in most cases you do not need to do it any more**. It should work for most STM32 MCUs. If it does not work in your case, replace it with your own scatter file as below.

>Open the keil project you want to convert. Assure it **has >been built** once at least.
>
>Open **'Options for Target'**, turn to **'Linker'** page, >unselect the **'Use Memory Layout for Target Dialog'**, then >press **'Edit'** button below, and keil will automatically >generate a Template.sct for you. 
>
>Close Keil and head onto the next step.

### 0.5 (optional) Add keil2cmake to your Path environment
Do this so that you don't need to type the full path (which could be really long). 

About how to add the path you put keil2cmake.exe to Path environment, you can search "< Windows/Linux > add environment variable Path" on the Internet. 


### 1. Generate CMakeLists.txt and toolchain.cmake according to uvprojx file
In any command line, do
```bash
<path/to/keil2cmake> <path/to/uvision/file.uvprojx> -o <path/to/output/directory>
```
For example, if the keil2cmake executable file is in home directory: open bash in keil project directory and do
```bash
~/keil2cmake ./USER/example.uvprojx -o ./USER/
```
and then the CMakeLists.txt and toolchain.cmake will be generated at ./USER/

If you have done [add keil2cmake to your path environment](#05-optional-add-keil2cmake-to-your-path-environment), you can just type `keil2cmake` instead of its path, like
```bash
keil2cmake ./USER/example.uvprojx -o ./USER/
```

In most cases you should set the ouput directory exactly to the one where uvprojx file is in, because the .c and .h and other files are most likely to be listed in the form of relative path. If the output dir is another one, you may need to manually modify the paths in CMakeLists.txt. 

### 2. Generate build chain and build it
In the dir mentioned above, do in command line
```bash
CMake -G Ninja -B ./build .
CMake --build ./build
```
Then your build target(.hex and .bin) will be generated in ./build/. Then use FLYMCU or ST-Link Utility or anything you like to burn it into your MCU.

## Use it in VS Code
It's very easy to use CMake in VSCode. Just open the top directory for your project in VS Code, then press **F1** and exec **`CMake: Configure`**, and the `./build/` directory will be generated for you. To build bin and hex files, press **F1** and exec **`CMake: build`**. 

