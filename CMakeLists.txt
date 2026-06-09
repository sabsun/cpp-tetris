cmake_minimum_required(VERSION 3.16)

project(cpp_tetris)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

file(GLOB SRC_FILES
    src/*.cpp
)

add_executable(game ${SRC_FILES})

target_link_libraries(game
    raylib
    GL
    m
    pthread
    dl
    rt
    X11
)