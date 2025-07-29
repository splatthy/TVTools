/**
 * TVTools Chrome Extension - Popup Script
 */

document.addEventListener('DOMContentLoaded', function() {
    const importBlofinBtn = document.getElementById('import-blofin');
    const importHighChangeBtn = document.getElementById('import-high-change');
    const generateFilesBtn = document.getElementById('generate-files');
    const statusDiv = document.getElementById('status');

    // Check if we're on TradingView
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        const currentTab = tabs[0];
        const isTradingView = currentTab.url.includes('tradingview.com');
        
        if (!isTradingView) {
            showStatus('Please open TradingView to use import features', 'error');
            importBlofinBtn.disabled = true;
            importHighChangeBtn.disabled = true;
        }
    });

    importBlofinBtn.addEventListener('click', function() {
        importWatchlist('blofin');
    });

    importHighChangeBtn.addEventListener('click', function() {
        importWatchlist('high-change');
    });

    generateFilesBtn.addEventListener('click', function() {
        generateFiles();
    });

    function importWatchlist(type) {
        showStatus('Importing watchlist...', 'info');
        
        // Send message to content script
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'importWatchlist',
                type: type
            }, function(response) {
                if (chrome.runtime.lastError) {
                    showStatus('Error: Make sure you\'re on TradingView', 'error');
                } else if (response && response.success) {
                    showStatus(`Successfully imported ${response.count} symbols!`, 'success');
                } else {
                    showStatus('Import failed. Please try again.', 'error');
                }
            });
        });
    }

    function generateFiles() {
        showStatus('Generating files...', 'info');
        
        // This would trigger file generation
        // Could open a new tab with download links
        chrome.tabs.create({
            url: chrome.runtime.getURL('generate.html')
        });
        
        showStatus('File generation started', 'success');
    }

    function showStatus(message, type) {
        statusDiv.textContent = message;
        statusDiv.className = `status ${type}`;
        statusDiv.style.display = 'block';
        
        // Hide after 3 seconds
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 3000);
    }
});