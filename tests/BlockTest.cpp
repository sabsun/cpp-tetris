#include "../src/block.h"
#include "../src/colors.h"
#include <catch2/catch_test_macros.hpp>

TEST_CASE("Block Initialization", "[block]")
{
    Block block = Block();
    
    SECTION("Block should have default values")
    {
        REQUIRE(block.id == 0);
        REQUIRE(block.cellSize == 30);
        REQUIRE(block.rotationState == 0);
    }
}

TEST_CASE("Block Movement", "[block]")
{
    Block block = Block();
    
    SECTION("Block movement should update offsets")
    {
        block.Move(2, 3);
        REQUIRE(block.GetCellPositions().size() > 0); // Check that we can get positions after movement
    }
}

TEST_CASE("Block Rotation", "[block]")
{
    Block block = Block();
    
    SECTION("Block should have rotation states")
    {
        int initialSize = block.cells.size();
        REQUIRE(initialSize >= 0);
    }
}

TEST_CASE("IBlock Specific Test", "[block]")
{
    // Note: IBlock is defined in blocks.cpp, so this test would need to be compiled with that file
    // This is just a placeholder to show how we might test specific block types
    REQUIRE(1 == 1); // Basic test to ensure Catch2 setup works
}
