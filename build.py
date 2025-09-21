#!/usr/bin/env python3
import PyInstaller.__main__
import os
import platform

def build():
    # 获取当前操作系统
    system = platform.system().lower()
    
    # 基本参数
    params = [
        'Convert.py',
        '--name=keil2cmake',
        '--onefile',
        '--console',
        '--clean',
        '--add-data=README.md;.' if system == 'windows' else '--add-data=README.md:.',
    ]
    
    # 添加图标（如果有）
    if os.path.exists('icon.ico'):
        params.append('--icon=icon.ico')
    
    # 设置输出目录
    output_dir = f"dist/{system}"
    params.extend(['--distpath', output_dir])
    
    # 执行打包
    PyInstaller.__main__.run(params)

if __name__ == '__main__':
    build()