# Assignment 1

## 1. System Information

### 1.1 Ubuntu 版本

```bash
cat /etc/os-release
```

```text
PRETTY_NAME="Ubuntu 24.04.5 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.5 LTS (Noble Numbat)"
VERSION_CODENAME=noble
```

### 1.2 Kernel

```bash
uname -r
```

```text
7.0.0-34-generic
```

### 1.3 CPU

```bash
lscpu
```

主要信息：

```text
架构：x86_64
CPU：4
厂商 ID：GenuineIntel
型号名称：Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz
超管理器厂商：VMware
虚拟化类型：完全
```

### 1.4 GPU

```bash
lspci | grep -Ei 'vga|3d|display'
```

```text
00:0f.0 VGA compatible controller: VMware SVGA II Adapter
```

```bash
lspci -k | grep -EA3 'VGA|3D|Display'
```

```text
00:0f.0 VGA compatible controller: VMware SVGA II Adapter
  Subsystem: VMware SVGA II Adapter
  Kernel driver in use: vmwgfx
  Kernel modules: vmwgfx
```

当前 Ubuntu 运行在 VMware 虚拟机中，系统识别到的图形设备为 VMware SVGA II Adapter。

### 1.5 显示协议

```bash
echo "$XDG_SESSION_TYPE"
echo "$DISPLAY"
echo "$WAYLAND_DISPLAY"
```

```text
wayland
:0
wayland-0
```

### 1.6 NVIDIA / CUDA

```bash
nvidia-smi
```

```text
找不到命令 “nvidia-smi”
```

```bash
nvcc --version
```

```text
找不到命令 “nvcc”
```

因此当前环境没有可用的 NVIDIA GPU，且未安装 CUDA Toolkit，相关项目按 N/A 处理。

---

## 2. Python Project A

### 2.1 环境创建与激活

Project A 要求 Python >= 3.9, < 3.11，本项目使用 Conda 创建 Python 3.10 环境。

实际执行：

```bash
conda create -n rc_vision_a python=3.10 -y
conda activate rc_vision_a
```

### 2.2 Python 版本与路径

```bash
python --version
which python
```

```text
Python 3.10.21
/home/zhy/miniconda3/envs/rc_vision_a/bin/python
```

### 2.3 安装依赖

进入 Project A：

```bash
cd ~/ROBOCON-Vision-Assignment-1/python_A
```

安装项目依赖：

```bash
pip install -r requirements.txt
```

由于本项目使用 Intel RealSense D435i 摄像头，额外安装 RealSense Python SDK：

```bash
pip install pyrealsense2
```

检查安装：

```bash
python -c "import pyrealsense2; print('RealSense Python OK')"
```

输出：

```text
RealSense Python OK
```

### 2.4 运行

实际运行：

```bash
cd ~/ROBOCON-Vision-Assignment-1/python_A
conda activate rc_vision_a
python camera.py
```

Project A 使用 Intel RealSense D435i 摄像头持续采集视频，并输出原始画面、灰度画面和轮廓画面；同时保存未经处理的原始视频。

---

## 3. Process Observation

Project A 运行期间，在另一个终端使用 `ps` 对进程进行观察。

实际执行：

```bash
ps -p 11886 -o pid,ppid,cmd,%cpu,%mem,etime
```

输出：

```text
    PID    PPID CMD                         %CPU %MEM     ELAPSED
  11886    9906 python camera.py             6.7  1.0       00:34
```

同时使用 `htop` 观察进程：

```bash
htop
```

---

## 4. Python Project B

### 4.1 环境创建与激活

Project B 使用独立的 Conda 环境。

```bash
cd ~/ROBOCON-Vision-Assignment-1/python_B
conda create -n rc_vision_b python=3.12 -y
conda activate rc_vision_b
```

### 4.2 Python 版本与路径

```bash
python --version
which python
```

```text
Python 3.12.14
/home/zhy/miniconda3/envs/rc_vision_b/bin/python
```

### 4.3 安装依赖

```bash
pip install -r requirements.txt
```

检查依赖：

```bash
python -c "import numpy, imageio, imageio_ffmpeg, skimage; print('Project B dependencies OK')"
```

输出：

```text
Project B dependencies OK
```

### 4.4 运行

```bash
python analyze_video.py \
  --input ../python_A/raw_capture.mp4 \
  --output advanced_analysis.mp4
```

Project A 使用的 Conda 环境：`rc_vision_a`

Python 版本：`3.10.21`

Project B 使用的 Conda 环境：`rc_vision_b`

Python 版本：`3.12.14`

### 4.5 为什么使用两个独立环境

Project A 要求：

```text
Python >= 3.9, < 3.11
```

Project B 要求：

```text
Python >= 3.12, < 3.14
```

两个项目要求的 Python 版本范围没有交集，因此不能使用同一个 Python 环境完成，需要分别创建 `rc_vision_a` 和 `rc_vision_b` 两个 Conda 环境。

---

## 5. C++ Manual Build

### 5.1 手动编译命令

实际使用的 g++ 编译命令：

```bash
g++ -std=c++17 \
  -Iinclude \
  -I/usr/include/eigen3 \
  $(pkg-config --cflags opencv4) \
  src/main.cpp src/transform.cpp \
  $(pkg-config --libs opencv4) \
  -o cpp_task
```

### 5.2 编译参数说明

`-I` 用于指定头文件的搜索目录。

本项目中：

```text
-Iinclude
```

使编译器能够找到：

```text
include/transform.hpp
```

而：

```text
-I/usr/include/eigen3
```

使编译器能够找到 Eigen 的头文件，例如：

```cpp
#include <Eigen/Dense>
```

### 5.3 为什么 transform.hpp 不单独作为 cpp 文件编译

`transform.hpp` 是头文件，主要用于声明数据结构和函数接口，而不是独立的程序源文件。

本项目中 `transform.hpp` 定义了 `TransformResult`，并声明了：

```cpp
TransformResult transformFrame(...);
cv::Mat composePreview(...);
```

这些函数的具体实现位于：

```text
src/transform.cpp
```

因此不需要把 `transform.hpp` 当作一个 `.cpp` 源文件单独编译。

### 5.4 为什么只写 main.cpp 无法得到完整程序

`main.cpp` 调用了：

```cpp
transformFrame(...)
composePreview(...)
```

但是这两个函数的具体实现位于：

```text
src/transform.cpp
```

因此编译完整程序时还需要把 `transform.cpp` 一起编译并链接。

### 5.5 编译结果

编译成功后产生的可执行文件为：

```text
cpp_task
```

---

## 6. CMake Build

### 6.1 CMakeLists.txt

完整内容：

```cmake
cmake_minimum_required(VERSION 3.16)

project(ROBOCON_Vision_Assignment1_CPP)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Eigen3 REQUIRED)
find_package(OpenCV REQUIRED)

add_executable(cpp_task
    src/main.cpp
    src/transform.cpp
)

target_include_directories(cpp_task PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(cpp_task PRIVATE
    Eigen3::Eigen
    ${OpenCV_LIBS}
)
```

### 6.2 CMake 配置与编译

```bash
cd ~/ROBOCON-Vision-Assignment-1/cpp
cmake -S . -B build
cmake --build build
```

### 6.3 运行

```bash
./build/cpp_task ../python_A/raw_capture.mp4 build/cpp_processed_cmake.mp4
```

运行结果：

```text
Input: ../python_A/raw_capture.mp4
Output: build/cpp_processed_cmake.mp4
Frames: 139
Mean scene luma: 108.51
Panels: original | Otsu binary | Canny edges
```

### 6.4 g++ 与 CMake 的关系

手工 `g++` 是直接指定编译步骤，而 CMake 是把这些步骤写进 `CMakeLists.txt` 后自动管理并调用 g++ 完成编译。

---

## 7. Git / GitHub

### 7.1 Git 初始化与提交

本项目使用 Git 进行版本管理。

主要提交记录：

```text
278504a initial
7644e49 修改以调用realsense
ca26b1f add project b
372c58f task7
9ad4567 add gitignore
cc3ee95 branch task
```

本项目已经有至少 3 个有意义的 commit。

### 7.2 分支操作

本次在 `main` 分支之外创建了 `git-branch` 分支，在该分支完成 README 修改并提交，随后合并回 `main`。

实际执行的关键命令：

```bash
git switch -c git-branch
git switch main
git merge git-branch
```

### 7.3 Git 忽略文件

使用 `.gitignore` 排除不应提交的生成文件：

```text
cpp/build/
.vscode/
__pycache__/
*.pyc
.venv/
```

视频文件较小，因此本项目的以下视频文件保留并提交到 Git：

```text
python_A/raw_capture.mp4
python_B/advanced_analysis.mp4
```

---

## 8. Problems and Notes

### 8.1 VMware 环境

本项目在 VMware 虚拟机中的 Ubuntu 24.04.5 LTS 环境完成。系统识别到的 GPU 为 VMware SVGA II Adapter。

### 8.2 NVIDIA / CUDA

当前环境没有可用的 NVIDIA GPU，`nvidia-smi` 和 `nvcc` 均不可用，因此本项目没有使用 NVIDIA CUDA。

### 8.3 RealSense 摄像头

Project A 使用 Intel RealSense D435i 摄像头，并通过 `pyrealsense2` 进行采集。
