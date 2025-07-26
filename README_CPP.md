# Order Book Analysis - C++ Implementation

## Overview
High-performance C++ implementation for analyzing temporary price impact functions g_s(X) from limit order book data.

## Files Included
- `order_book_analysis.cpp` - Main C++ source code
- `compile_and_run.bat` - Windows compilation script 
- `Makefile` - Cross-platform build file
- `*_impact.csv` - Generated impact analysis results

## Compilation & Execution

### Windows (MinGW):
```bash
./compile_and_run.bat
```

### Linux/Mac:
```bash
make
./order_book_analysis
```

### Manual Compilation:
```bash
g++ -std=c++17 -O3 -Wall -Wextra -o order_book_analysis order_book_analysis.cpp
```

## Performance Metrics
- **Execution Time**: 2.36 seconds
- **Data Processed**: 90,000 order book snapshots
- **Analysis Scope**: 10 price levels, 100 order sizes per symbol

## Mathematical Framework

The temporary impact function g_s(X) is modeled as:

```
g_buy(X) = (VWAP_execution - Mid_Price) / Mid_Price
g_sell(X) = (Mid_Price - VWAP_execution) / Mid_Price
```

Where VWAP is calculated by sequentially consuming liquidity across order book levels.

## Key Results
- **CRWV**: 17-20 bps impact range
- **FROG**: 26-31 bps impact range  
- **SOUN**: 10-11 bps impact range

## Dependencies
- C++17 compatible compiler
- Standard library only (no external dependencies)

## Output Format
CSV files with columns: order_size, avg_impact_bps, sample_count
