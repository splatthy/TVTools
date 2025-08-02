# Design Document

## Overview

The high change symbols functionality needs to be redesigned to properly process the full Blofin watchlist and accurately match symbols with screener data to identify volatile trading opportunities. The current implementation has logic flaws that result in incomplete symbol processing and incorrect filtering.

## Architecture

### Current Issues
1. **Logic Flow Problem**: The sorting and return statement is inside the symbol processing loop, causing early termination
2. **Symbol Matching Issues**: Inconsistent handling of symbol formats between watchlist and screener data
3. **Poor Error Handling**: Missing symbols are not logged, making debugging difficult
4. **Inefficient Processing**: Multiple unnecessary operations within the loop

### Proposed Solution
- Fix the method structure to process all symbols before sorting and returning
- Improve symbol matching logic to handle format variations
- Add comprehensive logging for debugging and monitoring
- Optimize the data processing flow

## Components and Interfaces

### WatchlistBuilder.get_high_change_symbols()

**Input Parameters:**
- `watchlist: Watchlist` - The full Blofin watchlist (optional, will build if not provided)
- `min_change_percent: float` - Minimum absolute change threshold (default: 5.0)

**Output:**
- `List[Dict]` - List of high-change symbols with metadata

**Data Structure:**
```python
{
    "symbol": str,           # Symbol name (e.g., "ETHUSDT.P")
    "change_percent": float, # Percentage change
    "price": float,          # Current price
    "volume": float          # Trading volume
}
```

### Symbol Matching Logic

**Watchlist Symbols Format:** 
- Standard format from screener (e.g., "ETHUSDT.P")

**Screener Data Format:**
- Same format as watchlist symbols
- Contains change percentage data

**Matching Strategy:**
- Direct string matching on symbol names
- Log mismatches for debugging
- Handle null/missing change data gracefully

## Data Models

### High Change Symbol Result
```python
@dataclass
class HighChangeSymbol:
    symbol: str
    change_percent: float
    price: float
    volume: float
    
    def __post_init__(self):
        # Validate that change_percent is not None
        if self.change_percent is None:
            raise ValueError("change_percent cannot be None")
```

### Processing Statistics
```python
@dataclass
class ProcessingStats:
    total_watchlist_symbols: int
    matched_symbols: int
    qualifying_symbols: int
    missing_symbols: List[str]
```

## Error Handling

### Symbol Matching Errors
- **Missing Symbol in Screener**: Log warning and continue processing
- **Null Change Data**: Skip symbol and log debug message
- **Invalid Data Types**: Handle gracefully with type conversion

### Data Processing Errors
- **Empty Watchlist**: Return empty list with warning log
- **Screener API Failure**: Use fallback or return empty list with error log
- **Threshold Validation**: Ensure min_change_percent is valid number

## Testing Strategy

### Unit Tests
1. **Test Symbol Matching**: Verify correct matching between watchlist and screener data
2. **Test Filtering Logic**: Ensure proper threshold filtering
3. **Test Sorting**: Verify results are sorted by absolute change percentage
4. **Test Error Handling**: Validate graceful handling of missing/invalid data

### Integration Tests
1. **Full Workflow Test**: Process complete Blofin watchlist and verify results
2. **Performance Test**: Ensure processing completes within reasonable time
3. **Data Consistency Test**: Verify output format matches expected structure

### Test Data
- Mock watchlist with known symbols
- Mock screener data with various change percentages
- Edge cases: null data, missing symbols, extreme values