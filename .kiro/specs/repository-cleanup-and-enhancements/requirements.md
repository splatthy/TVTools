# Repository Cleanup and High Change Symbols Enhancement

## Introduction

The TVTools repository has accumulated redundant files, outdated scripts, and has a broken high change symbols generator that only processes a small subset of symbols instead of the full Blofin watchlist. This spec addresses cleaning up the codebase and fixing the high change symbols functionality to work properly with the complete symbol set.

## Requirements

### Requirement 1: Repository Cleanup

**User Story:** As a developer maintaining TVTools, I want a clean, organized repository structure so that I can easily find and maintain the correct files without confusion from duplicates or outdated artifacts.

#### Acceptance Criteria

1. WHEN reviewing the repository structure THEN all duplicate scripts and outdated artifacts SHALL be identified and removed
2. WHEN examining files outside the tvtools/ directory THEN only essential scripts (main entry points, documentation, configuration) SHALL remain
3. WHEN looking at the project structure THEN it SHALL be clear which files are the canonical versions vs test/debug files
4. IF test files are kept THEN they SHALL be organized in a dedicated testing directory
5. WHEN the cleanup is complete THEN the repository SHALL have a clear separation between:
   - Core library code (tvtools/)
   - Main entry points (root level scripts)
   - Documentation (README, etc.)
   - Configuration files
   - Test utilities (organized separately)

### Requirement 2: High Change Symbols Generator Fix

**User Story:** As a trader using TVTools, I want the high change symbols generator to analyze the complete Blofin watchlist so that I don't miss high-volatility trading opportunities due to incomplete data processing.

#### Acceptance Criteria

1. WHEN generating high change symbols THEN the system SHALL start with the complete Blofin watchlist (~490 symbols)
2. WHEN processing symbols for change detection THEN ALL symbols from the Blofin watchlist SHALL be analyzed for price changes
3. WHEN filtering for high change symbols THEN the system SHALL correctly match watchlist symbols with screener data
4. WHEN no matches are found THEN the system SHALL log detailed information about why symbols aren't matching
5. WHEN generating the high change file THEN it SHALL contain symbols sorted by highest change percentage first
6. WHEN the process completes THEN the user SHALL see clear statistics about:
   - Total symbols in base watchlist
   - Total symbols with screener data matches
   - Total symbols meeting change threshold
   - Any symbols that couldn't be matched

### Requirement 3: Improved Error Handling and Debugging

**User Story:** As a user troubleshooting TVTools, I want clear error messages and debugging information so that I can understand why the high change detection might not be working as expected.

#### Acceptance Criteria

1. WHEN symbol matching fails THEN the system SHALL log specific details about mismatched symbols
2. WHEN screener data is incomplete THEN the system SHALL report which symbols are missing data
3. WHEN change thresholds filter out symbols THEN the system SHALL show statistics about the filtering process
4. WHEN debugging is enabled THEN the system SHALL show sample symbol matching attempts
5. WHEN the process completes THEN summary statistics SHALL be displayed showing the data pipeline flow

### Requirement 4: Consolidated and Verified Entry Points

**User Story:** As a user of TVTools, I want clear, non-redundant entry points for generating watchlists that actually work, so that I know which script to use without confusion or encountering broken functionality.

#### Acceptance Criteria

1. WHEN testing all entry point scripts THEN each script SHALL be verified to work correctly
2. WHEN scripts are found to be broken or outdated THEN they SHALL be either fixed or removed
3. WHEN looking for watchlist generation THEN there SHALL be one primary recommended script that is guaranteed to work
4. WHEN advanced options are needed THEN there SHALL be one CLI script with comprehensive options
5. WHEN simple usage is desired THEN there SHALL be one simple script for basic functionality
6. WHEN all scripts are updated THEN they SHALL use the same underlying logic and produce consistent output
7. WHEN documentation is updated THEN it SHALL clearly indicate which script to use for which purpose and confirm they have been tested

### Requirement 5: Script Verification and Testing

**User Story:** As a developer maintaining TVTools, I want to verify that all entry point scripts actually work before keeping them in the repository, so that users don't encounter broken functionality.

#### Acceptance Criteria

1. WHEN cleaning up the repository THEN each remaining script SHALL be tested to ensure it works
2. WHEN a script fails to work THEN it SHALL either be fixed or moved to archive
3. WHEN scripts are verified THEN the testing process SHALL be documented
4. WHEN multiple scripts provide similar functionality THEN only the working versions SHALL be kept
5. WHEN the cleanup is complete THEN all remaining scripts SHALL have verified functionality

## Success Criteria

- Repository has clean, organized structure with no duplicate functionality
- High change symbols generator processes the complete Blofin watchlist
- Clear debugging information helps users understand the data processing pipeline
- Consolidated, consistent entry points for all watchlist generation functionality
- All generated files are properly formatted for TradingView import