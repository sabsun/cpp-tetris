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

# Add test executable if Catch2 is available
option(ENABLE_TESTS "Enable tests" ON)

if(ENABLE_TESTS)

    enable_testing()

    include(FetchContent)

    FetchContent_Declare(
        Catch2
        GIT_REPOSITORY https://github.com/catchorg/Catch2.git
        GIT_TAG v3.8.1
    )

    FetchContent_MakeAvailable(Catch2)

    include(CTest)
    include(Catch)
    
    # Test source files
    set(TEST_SOURCES
        tests/GridTest.cpp
        src/grid.cpp
        src/position.cpp
        src/colors.cpp
    )
    
    add_executable(GridTests ${TEST_SOURCES})
    target_link_libraries(GridTests PRIVATE Catch2::Catch2WithMain raylib)
    catch_discover_tests(GridTests)
endif()
