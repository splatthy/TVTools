/**
 * TVTools Chrome Extension - Content Script
 * Runs on TradingView pages and adds watchlist management functionality
 */

class TVToolsWatchlistManager {
    constructor() {
        this.init();
    }

    init() {
        // Wait for TradingView to load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupWatchlistTools());
        } else {
            this.setupWatchlistTools();
        }
    }

    setupWatchlistTools() {
        // Wait a bit for TradingView's dynamic content to load
        setTimeout(() => {
            this.addTVToolsButton();
            this.observeWatchlistChanges();
        }, 3000);
    }

    addTVToolsButton() {
        // Find watchlist panel
        const watchlistPanel = this.findWatchlistPanel();
        if (!watchlistPanel) {
            console.log('TVTools: Watchlist panel not found, retrying...');
            setTimeout(() => this.addTVToolsButton(), 2000);
            return;
        }

        // Check if button already exists
        if (document.getElementById('tvtools-button')) {
            return;
        }

        // Create TVTools button
        const button = document.createElement('button');
        button.id = 'tvtools-button';
        button.className = 'tvtools-import-btn';
        button.innerHTML = '🚀 TVTools';
        button.title = 'Import Blofin watchlists';
        
        // Add click handler
        button.addEventListener('click', () => this.showImportDialog());

        // Insert button into watchlist header
        const watchlistHeader = watchlistPanel.querySelector('[class*="header"], [class*="title"]');
        if (watchlistHeader) {
            watchlistHeader.appendChild(button);
            console.log('TVTools: Button added successfully');
        }
    }

    findWatchlistPanel() {
        // Try multiple selectors to find watchlist panel
        const selectors = [
            '[class*="watchlist"]',
            '[data-name*="watchlist"]',
            '[class*="symbol-list"]',
            '[class*="right-toolbar"]'
        ];

        for (const selector of selectors) {
            const elements = document.querySelectorAll(selector);
            for (const element of elements) {
                if (element.offsetParent !== null) { // Check if visible
                    return element;
                }
            }
        }
        return null;
    }

    showImportDialog() {
        // Create modal dialog
        const modal = document.createElement('div');
        modal.id = 'tvtools-modal';
        modal.className = 'tvtools-modal';
        
        modal.innerHTML = `
            <div class="tvtools-modal-content">
                <div class="tvtools-modal-header">
                    <h3>🚀 TVTools Watchlist Import</h3>
                    <button class="tvtools-close" onclick="this.closest('.tvtools-modal').remove()">&times;</button>
                </div>
                <div class="tvtools-modal-body">
                    <div class="tvtools-option">
                        <button id="import-blofin" class="tvtools-btn tvtools-btn-primary">
                            📊 Import Blofin Perpetuals
                        </button>
                        <p>Import all available Blofin perpetual pairs</p>
                    </div>
                    <div class="tvtools-option">
                        <button id="import-high-change" class="tvtools-btn tvtools-btn-secondary">
                            📈 Import High Change Symbols
                        </button>
                        <p>Import symbols with >5% price change</p>
                    </div>
                    <div class="tvtools-option">
                        <label>
                            <input type="checkbox" id="replace-existing" checked>
                            Replace existing watchlist (recommended)
                        </label>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Add event listeners
        document.getElementById('import-blofin').addEventListener('click', () => {
            this.importWatchlist('blofin');
        });

        document.getElementById('import-high-change').addEventListener('click', () => {
            this.importWatchlist('high-change');
        });
    }

    async importWatchlist(type) {
        try {
            // Show loading
            this.showLoading('Fetching watchlist data...');

            // Fetch data from our API/service
            const symbols = await this.fetchWatchlistData(type);
            
            if (!symbols || symbols.length === 0) {
                this.showError('No symbols found');
                return;
            }

            // Check if user wants to replace existing
            const replaceExisting = document.getElementById('replace-existing').checked;
            
            if (replaceExisting) {
                await this.clearCurrentWatchlist();
            }

            // Import symbols
            await this.addSymbolsToWatchlist(symbols);
            
            this.showSuccess(`Imported ${symbols.length} symbols successfully!`);
            
            // Close modal
            document.getElementById('tvtools-modal').remove();

        } catch (error) {
            console.error('TVTools import error:', error);
            this.showError('Import failed: ' + error.message);
        }
    }

    async fetchWatchlistData(type) {
        // This would connect to your Python backend or use the data directly
        // For now, return mock data
        if (type === 'blofin') {
            return ['BLOFIN:ETHUSDT.P', 'BLOFIN:BTCUSDT.P', 'BLOFIN:XRPUSDT.P'];
        } else {
            return ['BLOFIN:SQDUSDT.P', 'BLOFIN:NEWTUSDT.P'];
        }
    }

    async clearCurrentWatchlist() {
        // Find and click clear/delete functionality
        // This would need to be implemented based on TradingView's current UI
        console.log('TVTools: Clearing current watchlist...');
    }

    async addSymbolsToWatchlist(symbols) {
        // Add symbols one by one to the current watchlist
        // This would interact with TradingView's add symbol functionality
        console.log('TVTools: Adding symbols:', symbols);
        
        for (const symbol of symbols) {
            await this.addSingleSymbol(symbol);
            await this.sleep(100); // Small delay to avoid overwhelming the UI
        }
    }

    async addSingleSymbol(symbol) {
        // Find the add symbol input/button and add the symbol
        // Implementation depends on TradingView's current UI structure
        console.log('TVTools: Adding symbol:', symbol);
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    showLoading(message) {
        // Show loading indicator
        console.log('TVTools Loading:', message);
    }

    showSuccess(message) {
        // Show success message
        console.log('TVTools Success:', message);
    }

    showError(message) {
        // Show error message
        console.log('TVTools Error:', message);
    }

    observeWatchlistChanges() {
        // Monitor for changes in the watchlist panel
        // Re-add button if panel is recreated
        const observer = new MutationObserver(() => {
            if (!document.getElementById('tvtools-button')) {
                this.addTVToolsButton();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
}

// Initialize when script loads
new TVToolsWatchlistManager();

console.log('TVTools Chrome Extension loaded');