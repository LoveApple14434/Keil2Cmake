# Makefile for PyInstaller project

# 配置
PROJECT_NAME := keil2cmake
MAIN_SCRIPT := Keil2Cmake.py
VENV_DIR := venv
DIST_DIR := dist
BUILD_DIR := build
ICON_DIR := icon_make
REQUIREMENTS := requirements.txt

# 平台检测
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    PLATFORM := linux
    ACTIVATE := $(VENV_DIR)/bin/activate
else
    PLATFORM := windows
    ACTIVATE := $(VENV_DIR)/Scripts/activate
endif

# 颜色定义
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m

.PHONY: all clean build linux windows deps venv test help

all: deps build

## 初始化虚拟环境
venv:
	@echo "$(YELLOW)Creating virtual environment...$(NC)"
	python -m venv $(VENV_DIR)
	@echo "$(GREEN)Virtual environment created$(NC)"

## 安装依赖
deps: venv
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	. $(ACTIVATE) && pip install -r $(REQUIREMENTS)
	@echo "$(GREEN)Dependencies installed$(NC)"

## 构建当前平台
build:
	@echo "$(YELLOW)Building for $(PLATFORM)...$(NC)"
	. $(ACTIVATE) && pyinstaller \
		--name $(PROJECT_NAME) \
		--onefile \
		--distpath $(DIST_DIR)/$(PLATFORM) \
		--workpath $(BUILD_DIR) \
		--specpath $(BUILD_DIR) \
		$(MAIN_SCRIPT)
	@echo "$(GREEN)Build completed for $(PLATFORM)$(NC)"

## 构建 Linux 版本
linux:
	@echo "$(YELLOW)Building for Linux...$(NC)"
	. $(ACTIVATE) && pyinstaller \
		--name $(PROJECT_NAME) \
		--onefile \
		--distpath $(DIST_DIR)/linux \
		--workpath $(BUILD_DIR) \
		--specpath $(BUILD_DIR) \
		$(MAIN_SCRIPT)
	@echo "$(GREEN)Linux build completed$(NC)"

## 构建 Windows 版本
windows:
	@echo "$(YELLOW)Building for Windows...$(NC)"
	. $(ACTIVATE) && pyinstaller \
		--name $(PROJECT_NAME) \
		--onefile \
		--windowed \
		--icon $(ICON_DIR)/icon.ico \
		--distpath $(DIST_DIR)/windows \
		--workpath $(BUILD_DIR) \
		--specpath $(BUILD_DIR) \
		$(MAIN_SCRIPT)
	@echo "$(GREEN)Windows build completed$(NC)"

## 构建所有平台
all-platforms: deps linux windows
	@echo "$(GREEN)All platform builds completed$(NC)"

## 清理构建文件
clean:
	@echo "$(YELLOW)Cleaning build files...$(NC)"
	rm -rf $(BUILD_DIR)
	rm -rf $(DIST_DIR)
	rm -rf __pycache__
	rm -rf *.spec
	@echo "$(GREEN)Clean completed$(NC)"

## 深度清理（包括虚拟环境）
deep-clean: clean
	@echo "$(YELLOW)Deep cleaning...$(NC)"
	rm -rf $(VENV_DIR)
	@echo "$(GREEN)Deep clean completed$(NC)"

## 运行测试
test: deps
	@echo "$(YELLOW)Running tests...$(NC)"
	. $(ACTIVATE) && python -m pytest tests/ -v

## 显示帮助
help:
	@echo "$(GREEN)Available targets:$(NC)"
	@echo "  all           - Build for current platform (default)"
	@echo "  deps          - Install dependencies"
	@echo "  build         - Build for current platform"
	@echo "  linux         - Build Linux version"
	@echo "  windows       - Build Windows version"
	@echo "  all-platforms - Build for all platforms"
	@echo "  clean         - Clean build files"
	@echo "  deep-clean    - Clean everything including venv"
	@echo "  test          - Run tests"
	@echo "  help          - Show this help"
