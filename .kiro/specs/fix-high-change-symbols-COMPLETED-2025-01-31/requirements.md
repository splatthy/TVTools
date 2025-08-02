# Requirements Document

## Introduction

The high change symbols watchlist generator is not working correctly. It should process the full Blofin watchlist (~490 symbols) and identify symbols with significant price changes, but currently it's only returning a small subset of symbols due to logic issues in the matching and filtering process.

## Requirements

### Requirement 1

**User Story:** As a trader, I want to get a comprehensive list of high-change symbols from the full Blofin watchlist, so that I can identify all volatile trading opportunities.

#### Acceptance Criteria

1. WHEN I request high change symbols THEN the system SHALL process the complete Blofin watchlist (~490 symbols)
2. WHEN processing symbols THEN the system SHALL match watchlist symbols with screener data containing change percentages
3. WHEN a symbol has change data THEN the system SHALL include it if the absolute change meets the minimum threshold
4. WHEN no minimum threshold is specified THEN the system SHALL default to 5.0% change
5. WHEN sorting results THEN the system SHALL sort by absolute change percentage in descending order

### Requirement 2

**User Story:** As a trader, I want accurate symbol matching between the watchlist and screener data, so that no high-change symbols are missed due to data inconsistencies.

#### Acceptance Criteria

1. WHEN matching symbols THEN the system SHALL handle both formats (with and without .P suffix)
2. WHEN screener data is missing for a symbol THEN the system SHALL log the missing symbol for debugging
3. WHEN change data is null or missing THEN the system SHALL skip that symbol gracefully
4. WHEN processing is complete THEN the system SHALL return all qualifying symbols sorted by change magnitude

### Requirement 3

**User Story:** As a developer, I want clear logging and debugging information, so that I can troubleshoot issues with symbol matching and data processing.

#### Acceptance Criteria

1. WHEN processing starts THEN the system SHALL log the total number of watchlist symbols being processed
2. WHEN symbols are matched THEN the system SHALL log successful matches and missing symbols
3. WHEN filtering by change threshold THEN the system SHALL log how many symbols qualify
4. WHEN processing completes THEN the system SHALL log the final count of high-change symbols returned