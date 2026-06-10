#include "../src/grid.h"
#include <iostream>
#include <cassert>

// Simple standalone test for Grid::ClearFullRows functionality
void testGridClearFullRows() {
    std::cout << "Testing Grid::ClearFullRows...\n";
    
    // Create a grid and fill some rows
    Grid grid;
    
    // Fill row 5 completely
    for(int col = 0; col < 10; col++) {
        grid.grid[5][col] = 1;
    }
    
    // Fill row 8 completely  
    for(int col = 0; col < 10; col++) {
        grid.grid[8][col] = 2;
    }
    
    // Fill row 15 completely
    for(int col = 0; col < 10; col++) {
        grid.grid[15][col] = 3;
    }
    
    // Fill row 2 with only one empty cell (should NOT be cleared)
    for(int col = 0; col < 10; col++) {
        grid.grid[2][col] = 4;
    }
    grid.grid[2][5] = 0; // Make one cell empty
    
    int cleared = grid.ClearFullRows();
    
    std::cout << "Cleared " << cleared << " rows (expected 3)\n";
    assert(cleared == 3);
    
    // Verify the full rows are now empty
    for(int col = 0; col < 10; col++) {
        assert(grid.grid[5][col] == 0);
        assert(grid.grid[8][col] == 0);
        assert(grid.grid[15][col] == 0);
    }
    
    // Verify the partial row is still intact
    for(int col = 0; col < 10; col++) {
        if(col == 5) {
            assert(grid.grid[2][col] == 0);
        } else {
            assert(grid.grid[2][col] == 4);
        }
    }
    
    std::cout << "All tests passed!\n";
}

void testGridIsCellOutside() {
    std::cout << "Testing Grid::IsCellOutside...\n";
    
    Grid grid;
    
    // Test valid positions
    assert(grid.IsCellOutside(0, 0) == false);
    assert(grid.IsCellOutside(19, 9) == false);
    assert(grid.IsCellOutside(10, 5) == false);
    
    // Test invalid positions
    assert(grid.IsCellOutside(-1, 5) == true);
    assert(grid.IsCellOutside(20, 5) == true);
    assert(grid.IsCellOutside(10, -1) == true);
    assert(grid.IsCellOutside(10, 10) == true);
    
    std::cout << "All boundary tests passed!\n";
}

void testGridIsCellEmpty() {
    std::cout << "Testing Grid::IsCellEmpty...\n";
    
    Grid grid;
    
    // Test empty cells initially
    assert(grid.IsCellEmpty(0, 0) == true);
    assert(grid.IsCellEmpty(10, 5) == true);
    assert(grid.IsCellEmpty(19, 9) == true);
    
    // Fill some cells and test
    grid.grid[5][5] = 1;
    grid.grid[10][3] = 2;
    
    assert(grid.IsCellEmpty(5, 5) == false);
    assert(grid.IsCellEmpty(10, 3) == false);
    assert(grid.IsCellEmpty(0, 0) == true); // Still empty
    
    std::cout << "All cell status tests passed!\n";
}

int main() {
    std::cout << "=== Running Grid Tests ===\n\n";
    
    testGridIsCellEmpty();
    testGridIsCellOutside();
    testGridClearFullRows();
    
    std::cout << "\n=== All Tests Passed Successfully! ===\n";
    return 0;
}
