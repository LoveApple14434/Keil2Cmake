import xml.etree.ElementTree as ET
import os
import argparse


def parse_uvprojx(uvprojx_path):
    """解析uvprojx文件，提取项目配置"""
    tree = ET.parse(uvprojx_path)
    root = tree.getroot()
    
    # 项目基本信息
    print("Getting target info...")
    project_name = root.find('.//Targets/Target/TargetName').text
    output_dir = root.find('.//Targets/Target/TargetOption/TargetCommonOption/OutputDirectory').text or 'build/'
    
    # 源文件收集
    print("Collecting source files...")
    source_files = []
    for group in root.findall('.//Groups/Group'):
        for file in group.findall('Files/File'):
            file_path = file.find('FilePath').text
            if file_path.endswith(('.c', '.C', '.cpp', '.s', '.S', '.asm')):
                source_files.append(file_path)
    
    # 包含路径
    print("Setting include paths...")
    include_paths = []
    includes = root.find('.//TargetOption/TargetArmAds/Cads/VariousControls/IncludePath')
    if includes is not None and includes.text:
        include_paths.extend(includes.text.split(';'))
    
    # 预定义宏
    print("Loading preset defines...")
    defines = []
    defs = root.find('.//TargetOption/TargetArmAds/Cads/VariousControls/Define')
    if defs is not None and defs.text:
        defines.extend([d.strip() for d in defs.text.split(',')])
    
    # 链接器脚本
    print("Looking for scatter file...")
    linker_script = None
    scatter_file = root.find('.//TargetOption/TargetArmAds/LDads/ScatterFile')
    if scatter_file is not None and scatter_file.text:
        linker_script = scatter_file.text
    
    # 设备信息
    print("Getting device info...")
    device_name = None
    device_node = root.find('.//Targets/Target/TargetOption/TargetCommonOption/Device')
    if device_node is not None and device_node.text:
        device_name = device_node.text
    
    # 编译器版本检测
    print("Validating compilor version...")
    use_armclang = False
    armclang_node = root.find('.//TargetOption/TargetArmAds/UseArmClang')
    if armclang_node is not None and armclang_node.text == '1':
        use_armclang = True
    
    # 编译器选项
    print("Setting options for compilors and linkers...")
    c_flags = root.find('.//TargetOption/TargetArmAds/Cads/VariousControls/MiscControls') 
    asm_flags = root.find('.//TargetOption/TargetArmAds/Aads/VariousControls/MiscControls') 
    ld_flags = root.find('.//TargetOption/TargetArmAds/LDads/VariousControls/MiscControls') 
    if c_flags is not None and c_flags.text is not None:
        c_flags = c_flags.text
    else:
        c_flags = ''
    if asm_flags is not None and asm_flags.text is not None:
        asm_flags = asm_flags.text
    else:
        asm_flags = ''
    if ld_flags is not None:
        ld_flags = ld_flags.text
    else:
        ld_flags = ''
    
    # 优化级别
    print("Defining optimize level...")
    opt_level = "0"
    opt_node = root.find('.//TargetOption/TargetArmAds/Cads/Optimization')
    if opt_node is not None and opt_node.text:
        opt_level = opt_node.text
    
    print()
    
    return {
        'project_name': project_name,
        'source_files': source_files,
        'include_paths': include_paths,
        'defines': defines,
        'linker_script': linker_script,
        'device': device_name.strip() if device_name else "Unknown",
        'c_flags': c_flags,
        'asm_flags': asm_flags,
        'ld_flags': ld_flags,
        'output_dir': output_dir,
        'use_armclang': use_armclang,
        'opt_level': opt_level
    }


def detect_cpu_architecture(device_name):
    """根据设备名称推断CPU架构"""
    device_lower = device_name.lower()
    
    # 尝试匹配常见ARM架构
    if 'cortex-m0' in device_lower:
        return "Cortex-M0"
    elif 'cortex-m3' in device_lower:
        return "Cortex-M3"
    elif 'cortex-m4' in device_lower:
        return "Cortex-M4"
    elif 'cortex-m7' in device_lower:
        return "Cortex-M7"
    elif 'cortex-m33' in device_lower:
        return "Cortex-M33"
    elif 'cortex-m55' in device_lower:
        return "Cortex-M55"
    
    # 默认值
    return "Cortex-M4"


def generate_cmakelists(project_data, output_dir):
    """生成CMakeLists.txt文件"""
    # 处理包含路径中的空格问题
    include_paths_formatted = []
    for path in project_data['include_paths']:
        if ' ' in path:
            include_paths_formatted.append(f'"{path}"')
        else:
            include_paths_formatted.append(path)

    # 处理源文件路径中的空格问题
    source_files_formatted = []
    for file in project_data['source_files']:
        if ' ' in file:
            source_files_formatted.append(f'"{file}"')
        else:
            source_files_formatted.append(file)

    # 解决 f-string 表达式不允许出现反斜杠的问题
    src_files = "\n    ".join(source_files_formatted)
    src_files = src_files.replace('\\', '/')
    inc_paths = "\n    ".join(include_paths_formatted)
    inc_paths = inc_paths.replace('\\', '/')
    defines = "\n    ".join(project_data['defines'])
    # 单独处理 linker_script，防止 f-string 内部出现反斜杠
    # linker_script_path = project_data['linker_script'].replace('\\', '/') if project_data['linker_script'] else ''
    # if linker_script_path.strip()=='' or linker_script_path=='/':
        # linker_script_path='Template.sct'
    linker_script_path='Template.sct'
    ld_flags = project_data['ld_flags']

    content = (
        'cmake_minimum_required(VERSION 4.0)\n\n'
        '# 包含工具链配置\n'
        'set(CMAKE_TOOLCHAIN_FILE ${CMAKE_CURRENT_SOURCE_DIR}/toolchain.cmake)\n\n'
        f'project({project_data["project_name"]} LANGUAGES C ASM)\n\n'
        '# 添加可执行文件\n'
        'add_executable(${PROJECT_NAME}\n'
        f'    {src_files}\n'  # 源文件
        ')\n\n'
        '# 添加自定义目标用于生成二进制文件 (使用 POST_BUILD)\n'
        'add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD\n'
        '    COMMAND ${CMAKE_FROMELF} --i32combined --output="${CMAKE_RUNTIME_OUTPUT_DIRECTORY}${PROJECT_NAME}.hex" "$<TARGET_FILE:${PROJECT_NAME}>"\n'
        '    COMMENT "Generating HEX file"\n'
        ')\n\n'
        'add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD\n'
        '    COMMAND ${CMAKE_FROMELF} --bin --output="${CMAKE_RUNTIME_OUTPUT_DIRECTORY}${PROJECT_NAME}.bin" "$<TARGET_FILE:${PROJECT_NAME}>"\n'
        '    COMMENT "Generating BIN file"\n'
        ')\n\n'
        '# 包含目录\n'
        'target_include_directories(${PROJECT_NAME} PRIVATE\n'
        f'    {inc_paths}\n'
        ')\n\n'
        '# 预处理器定义\n'
        'target_compile_definitions(${PROJECT_NAME} PRIVATE\n'
        f'    {defines}\n'
        ')\n\n'
        '# 链接器脚本设置\n'
        f'set(LINKER_SCRIPT "${{CMAKE_SOURCE_DIR}}/{linker_script_path}")\n\n'
        '# 链接选项\n'
        'target_link_options(${PROJECT_NAME} PRIVATE\n'
        '    ${LINKER_FLAGS}\n'
        '    "--scatter=${LINKER_SCRIPT}"\n'
        f'    {ld_flags}\n'
        ')\n'
    )

    with open(os.path.join(output_dir, 'CMakeLists.txt'), 'w', encoding="UTF-8") as f:
        f.write(content)


def generate_toolchain(project_data, output_dir):
    """生成ARMCC工具链配置文件"""
    # 推断CPU架构
    cpu = detect_cpu_architecture(project_data['device'])
    
    # 确定编译器类型
    compiler_type = "armclang" if project_data['use_armclang'] else "armcc"
    
    content = f"""# ARM Compiler (Keil) 工具链配置
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR ARM)

# 设置编译器路径（根据实际Keil安装路径修改）
set(KEIL_PATH "D:/Program/Keil_v5/")
set(ARMCC_BIN "${{KEIL_PATH}}ARM/ARM_Compiler_5.06u7/bin/")
set(ARMCLANG_BIN "${{KEIL_PATH}}ARM/ARMCLANG/bin/")

# 根据项目配置选择编译器
if ("{compiler_type}" STREQUAL "armclang")
    set(CMAKE_C_COMPILER "${{ARMCLANG_BIN}}armclang.exe")
    set(CMAKE_CXX_COMPILER "${{ARMCLANG_BIN}}armclang.exe")
    set(CMAKE_ASM_COMPILER "${{ARMCLANG_BIN}}armclang.exe")
    set(CMAKE_LINKER "${{ARMCLANG_BIN}}armlink.exe")
    set(CMAKE_AR "${{ARMCLANG_BIN}}armar.exe")
    set(CMAKE_FROMELF "${{ARMCLANG_BIN}}fromelf.exe")
else()
    set(CMAKE_C_COMPILER "${{ARMCC_BIN}}armcc.exe")
    set(CMAKE_CXX_COMPILER "${{ARMCC_BIN}}armcc.exe")
    set(CMAKE_ASM_COMPILER "${{ARMCC_BIN}}armasm.exe")
    set(CMAKE_LINKER "${{ARMCC_BIN}}armlink.exe")
    set(CMAKE_AR "${{ARMCC_BIN}}armar.exe")
    set(CMAKE_FROMELF "${{ARMCC_BIN}}fromelf.exe")
endif()

# 确保使用正确的工具链
set(CMAKE_C_COMPILER_WORKS 1 INTERNAL)
set(CMAKE_ASM_COMPILER_WORKS 1 INTERNAL)
set(CMAKE_CXX_COMPILER_WORKS 1 INTERNAL)

# 公共编译器选项
set(COMMON_FLAGS "--cpu={cpu} --apcs=interwork --c99 --split_sections {project_data['c_flags']}")

# 汇编器选项
set(ASM_FLAGS "--cpu={cpu} --apcs=interwork --pd \\"__MICROLIB SETA 1\\" {project_data['asm_flags']}")

# 链接器选项
set(LINKER_FLAGS
    "--map"
    "--info=summarysizes,sizes,totals,unused,veneers"
    "--callgraph"
    "--xref"
    "--entry=Reset_Handler"
    "--strict"
    "--summary_stderr"
    "{project_data['ld_flags']}"
)

# 配置编译器选项
set(CMAKE_C_FLAGS "${{COMMON_FLAGS}} -O{project_data['opt_level']}")
set(CMAKE_CXX_FLAGS "${{COMMON_FLAGS}} -O{project_data['opt_level']} --cpp")
set(CMAKE_ASM_FLAGS "${{ASM_FLAGS}}")

# 设置链接器
set(CMAKE_C_LINK_EXECUTABLE 
    "${{CMAKE_LINKER}} <CMAKE_C_LINK_FLAGS> <LINK_FLAGS> <OBJECTS> -o <TARGET> <LINK_LIBRARIES>"
)

# 交叉编译设置（跳过编译器测试）
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

# 构建类型配置
set(CMAKE_BUILD_TYPE "Debug" CACHE STRING "Build type (Debug or Release)")

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    if ("{compiler_type}" STREQUAL "armclang")
        set(CMAKE_C_FLAGS "${{CMAKE_C_FLAGS}} -g")
    else()
        set(CMAKE_C_FLAGS "${{CMAKE_C_FLAGS}} --debug")
    endif()
else()
    set(CMAKE_C_FLAGS "${{CMAKE_C_FLAGS}} --no_debug")
endif()

# 设置目标属性
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

# 添加诊断信息
message(STATUS "=== 使用 ARM 工具链 ===")
message(STATUS "编译器类型: ${{CMAKE_C_COMPILER}}")
message(STATUS "构建类型: ${{CMAKE_BUILD_TYPE}}")
"""

    with open(os.path.join(output_dir, 'toolchain.cmake'), 'w', encoding="UTF-8") as f:
        f.write(content)


def generate_scatter_file(destination:str):
    templateScatter = """
; *************************************************************
; *** Scatter-Loading Description File generated by uVision ***
; *************************************************************

LR_IROM1 0x08000000 0x00100000  {    ; load region size_region
  ER_IROM1 0x08000000 0x00100000  {  ; load address = execution address
   *.o (RESET, +First)
   *(InRoot$$Sections)
   .ANY (+RO)
   .ANY (+XO)
  }
  RW_IRAM1 0x20000000 0x00020000  {  ; RW data
   .ANY (+RW +ZI)
  }
}

    """
    with open(os.path.join(destination,"Template.sct"),'w',encoding='UTF-8') as f:
        f.write(templateScatter)

    

def main():
    parser = argparse.ArgumentParser(description='Convert Keil uVision project to CMake for ARM Compiler')
    parser.add_argument('uvprojx', help='Path to .uvprojx file')
    parser.add_argument('-o', '--output', default='.', help='Output directory')
    args = parser.parse_args()

    # 解析项目文件
    project_data = parse_uvprojx(args.uvprojx)
    
    # 确保输出目录存在
    os.makedirs(args.output, exist_ok=True)
    
    # 生成CMake文件
    generate_cmakelists(project_data, args.output)
    generate_toolchain(project_data, args.output)
    
    # 生成scatter文件
    generate_scatter_file(args.output)
    
    print(f"Generated CMakeLists.txt and toolchain.cmake in {args.output}")
    print(f"Project name: {project_data['project_name']}")
    print(f"Device: {project_data['device']}")
    print(f"Compiler: {'armclang' if project_data['use_armclang'] else 'armcc'}")
    print(f"Optimization level: -O{project_data['opt_level']}")
    print(f"Note: Please verify Keil installation path in toolchain.cmake before use")
    print(f"Build commands:")
    print(f"  cmake -G Ninja -B build .")
    print(f"  cmake --build build")


if __name__ == '__main__':
    main()
