#include "../src/grid.h"
#include "../src/colors.h"
#include <catch2/catch_test_macros.hpp>
#include <catch2/matchers/catch_matchers.hpp>

TEST_CASE("Grid Initialization", "[grid]")
{
    Grid grid = Grid();
    
    SECTION("Grid should be initialized with zeros")
    {
        for (int row = 0; row < 20; row++)
        {
            for (int column = 0; column < 10; column++)
            {
                REQUIRE(grid.grid[row][column] == 0);
            }
        }
    }
}

TEST_CASE("Grid IsCellOutside", "[grid]")
{
    Grid grid = Grid();
    
    SECTION("Cells inside grid bounds should not be outside")
    {
        REQUIRE(grid.IsCellOutside(0, 0) == false);
        REQUIRE(grid.IsCellOutside(19, 9) == false);
        REQUIRE(grid.IsCellOutside(10, 5) == false);
    }
    
    SECTION("Cells outside grid bounds should be detected as outside")
    {
        REQUIRE(grid.IsCellOutside(-1, 5) == true);
        REQUIRE(grid.IsCellOutside(20, 5) == true);
        REQUIRE(grid.IsCellOutside(10, -1) == true);
        REQUIRE(grid.IsCellOutside(10, 10) == true);
    }
}

TEST_CASE("Grid IsCellEmpty", "[grid]")
{
    Grid grid = Grid();
    
    SECTION("Cells should be empty initially")
    {
        REQUIRE(grid.IsCellEmpty(0, 0) == true);
        REQUIRE(grid.IsCellEmpty(10, 5) == true);
        REQUIRE(grid.IsCellEmpty(19, 9) == true);
    }
    
    SECTION("Filled cells should not be empty")
    {
        grid.grid[5][5] = 1;
        REQUIRE(grid.IsCellEmpty(5, 5) == false);
        
        grid.grid[10][3] = 2;
        REQUIRE(grid.IsCellEmpty(10, 3) == false);
    }
}

TEST_CASE("Grid ClearFullRows", "[grid]")
{
    Grid grid = Grid();
    
    SECTION("No rows should be cleared when grid is empty")
    {
        int cleared = grid.ClearFullRows();
        REQUIRE(cleared == 0);
    }
    
    SECTION("Clear one full row")
    {
        // Fill row 5 completely
        for (int col = 0; col < 10; col++)
        {
            grid.grid[5][col] = 1;
        }
        
        int cleared = grid.ClearFullRows();
        REQUIRE(cleared == 1);
        
        // Row 5 should now be empty
        for (int col = 0; col < 10; col++)
        {
            REQUIRE(grid.grid[5][col] == 0);
        }
    }
    
    SECTION("Clear multiple full rows")
    {
        // Fill rows 3, 5, and 7 completely
        for (int col = 0; col < 10; col++)
        {
            grid.grid[3][col] = 1;
            grid.grid[5][col] = 2;
            grid.grid[7][col] = 3;
        }
        
        int cleared = grid.ClearFullRows();
        REQUIRE(cleared == 3);
        
        // These rows should now be empty
        for (int col = 0; col < 10; col++)
        {
            REQUIRE(grid.grid[3][col] == 0);
            REQUIRE(grid.grid[5][col] == 0);
            REQUIRE(grid.grid[7][col] == 0);
        }
    }
    
    SECTION("Row with one empty cell should not be cleared")
    {
        // Fill row 5 completely except one cell
        for (int col = 0; col < 10; col++)
        {
            grid.grid[5][col] = 1;
        }
        grid.grid[5][5] = 0; // Make one cell empty
        
        int cleared = grid.ClearFullRows();
        REQUIRE(cleared == 0);
        
        // Row should still be intact
        for (int col = 0; col < 10; col++)
        {
            REQUIRE(grid.grid[5][col] == (col == 5 ? 0 : 1));
        }
    }
}

// TEST_CASE("Grid MoveRowDown", "[grid]")
// {
//     Grid grid = Grid();
    
//     SECTION("Move row down when there are cleared rows above")
//     {
//         // Fill rows 3 and 5 completely
//         for (int col = 0; col < 10; col++)
//         {
//             grid.grid[3][col] = 1;
//             grid.grid[5][col] = 2;
//         }
        
//         // Clear row 5 first (which will shift row 3 down)
//         grid.ClearRow(5);
        
//         // Now row 3 should have moved down by 1 position
//         // Row 3 content should now be at row 4
//         for (int col = 0; col < 10; col++)
//         {
//             REQUIRE(grid.grid[4][col] == 1);
//         }
//     }
// }
