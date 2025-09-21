# Keil2Cmake 转换器

2025 年 9 月 21 日：我已使用 Pyinstaller 生成了适用于 Windows 和 Linux 的可执行文件。请通过 [GitHub release](https://github.com/LoveApple14434/Keil2Cmake/releases/tag/v1) 下载使用。现在你的电脑上不再需要安装 Python 环境了。

## 环境要求

  - ~~Python3~~
  - Cmake
  - Ninja
  - Keil 编译器

## 首次使用前

2025 年 9 月 21 日：现在你不再需要在代码中填写路径了。但首次使用 keil2cmake 时，你仍需在命令行中配置路径。请参考 [配置工具链路径](https://www.google.com/search?q=%23%E9%85%8D%E7%BD%AE%E5%B7%A5%E5%85%B7%E9%93%BE%E8%B7%AF%E5%BE%84)。

~~在第一次使用之前，请转到 **第 202 行** 并填写你 PC 上 **自己的 Keil 安装路径**。~~

~~如果你不知道如何找到它，请打开 Keil 并打开 Windows 任务管理器，在其中右键单击 Keil 任务，打开文件所在位置，然后将该路径复制到 [Convert.py 的 202 行](https://www.google.com/search?q=./Convert.py) 即可。~~

## 配置工具链路径

工具链路径应存储在 `~/.keil2cmake/path.cfg` 文件中。使用以下命令来查看或编辑路径：

```bash
# 显示当前配置
keil2cmake --show-config
# 或者
keil2cmake -sc

# 编辑 ARMCC (Keil C51 编译器) 路径
keil2cmake --edit ARMCC_PATH=D:/Program/Keil_v5/ARM/ARM_Compiler_5.06u7/bin/
# 或者
keil2cmake -e ARMCC_PATH=D:/Program/Keil_v5/ARM/ARM_Compiler_5.06u7/bin/

# 编辑 ARMCLANG (Keil MDK-ARM 编译器) 路径
keil2cmake --edit ARMCLANG_PATH=D:/Program/Keil_v5/ARM/ARMCLANG/bin/
# 或者
keil2cmake -e ARMCLANG_PATH=D:/Program/Keil_v5/ARM/ARMCLANG/bin/
```

## 使用方法

### 0\. 通过 Keil 生成分散加载文件（scatter file）

2025 年 8 月 3 日：我增加了一个新功能来为你生成分散加载文件，所以**在大多数情况下你不再需要手动执行此步骤**。该功能对绝大多数 STM32 MCU 都应有效。如果它在你的项目中不起作用，请按照以下步骤使用你自己的分散加载文件替换它。

> 打开你想要转换的 Keil 项目，确保它**至少已经被编译过一次**。
>
> 打开 **'Options for Target' (目标选项)**，切换到 **'Linker' (链接器)** 标签页，**取消勾选 'Use Memory Layout from Target Dialog' (使用目标对话框中的内存布局)**，然后点击下方的 **'Edit' (编辑)** 按钮，Keil 将自动为你生成一个 `Template.sct` 文件。
>
> 关闭 Keil，然后进行下一步。

### 1\. 根据 uvprojx 文件生成 CMakeLists.txt 和 toolchain.cmake

在任意命令行中，执行：

```bash
<keil2cmake可执行文件路径> <uvision项目文件.uvprojx的路径> -o <输出目录路径>
```

例如，如果 `keil2cmake` 可执行文件在你的主目录 (`home`) 下：在 Keil 项目的目录下打开 bash 并执行：

```bash
~/keil2cmake ./USER/example.uvprojx -o ./USER/
```

然后 `CMakeLists.txt` 和 `toolchain.cmake` 文件将会生成在 `./USER/` 目录下。

在大多数情况下，你应该将输出目录设置为 `.uvprojx` 文件所在的目录，因为 .c、.h 和其他文件很可能在工程文件中是以相对路径的形式组织的。如果输出目录是其他文件夹，你可能需要手动修改 `CMakeLists.txt` 文件中的路径。

### 2\. 生成构建文件并编译

在上面提到的输出目录中，于命令行执行：

```bash
CMake -G Ninja -B ./build .
CMake --build ./build
```

然后你的目标文件（.hex 和 .bin）将会生成在 `./build/` 目录下。之后你可以使用 FLYMCU、ST-Link Utility 或任何你喜欢的工具将其烧录到你的 MCU 中。

## 在 VS Code 中使用

在 VSCode 中使用 CMake 非常简单。只需在 VS Code 中打开你项目的顶层目录，然后按 **F1** 并执行 **`CMake: Configure`**，`./build/` 目录就会被自动创建。要编译生成 .bin 和 .hex 文件，请按 **F1** 并执行 **`CMake: build`**。