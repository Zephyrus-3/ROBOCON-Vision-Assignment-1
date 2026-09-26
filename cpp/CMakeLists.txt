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

//这是一个branch的任务hhh