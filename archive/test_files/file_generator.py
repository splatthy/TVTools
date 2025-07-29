"""
Generate TradingView-compatible import files
"""

import os
import logging
from typing import List
from ..discovery import WatchlistBuilder

logger = logging.getLogger(__name__)


class TradingViewFileGenerator:
    """Generate TradingView import files"""
    
    def __init__(self, temp_dir: str = "temp"):
        self.temp_dir = temp_dir
        self.ensure_temp_dir()
        
    def ensure_temp_dir(self):
        """Create temp directory if it doesn't exist"""
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
            logger.info(f"📁 Created temp directory: {self.temp_dir}")
    
    def format_symbols_for_tradingview(self, symbols: List[str], exchange: str = "BLOFIN") -> List[str]:
        """Format symbols for TradingView import (EXCHANGE:SYMBOL format)"""
        formatted = []
        for symbol in symbols:
            if not symbol.startswith(f"{exchange}:"):
                formatted.append(f"{exchange}:{symbol}")
            else:
                formatted.append(symbol)
        return formatted
    
    def generate_blofin_watchlist_file(self, filename: str = "blofin_pairs.txt") -> str:
        """Generate Blofin pairs watchlist file"""
        try:
            logger.info("🔨 Building Blofin perpetuals watchlist...")
            
            # Build watchlist using existing builder
            builder = WatchlistBuilder()
            watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)
            
            if not watchlist.symbols:
                logger.error("❌ No symbols found in watchlist")
                return None
                
            # Extract symbol names
            symbols = [symbol.symbol for symbol in watchlist.symbols]
            logger.info(f"📊 Found {len(symbols)} Blofin perpetual symbols")
            
            # Format for TradingView
            formatted_symbols = self.format_symbols_for_tradingview(symbols, "BLOFIN")
            
            # Write to file
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, 'w') as f:
                for symbol in formatted_symbols:
                    f.write(f"{symbol}\n")
            
            logger.info(f"✅ Generated Blofin watchlist file: {filepath}")
            logger.info(f"📝 Contains {len(formatted_symbols)} symbols")
            
            return filepath
            
        except Exception as e:
            logger.error(f"❌ Error generating Blofin watchlist file: {e}")
            return None
    
    def generate_high_change_watchlist_file(self, min_change: float = 5.0, filename: str = "high_change.txt") -> str:
        """Generate high change symbols watchlist file"""
        try:
            logger.info(f"📈 Building high change watchlist (>{min_change}%)...")
            
            # Build high change watchlist
            builder = WatchlistBuilder()
            base_watchlist = builder.build_watchlist_from_tradingview(save_to_file=False)
            high_change = builder.get_high_change_symbols(base_watchlist, min_change)
            
            if not high_change:
                logger.warning("⚠️ No high change symbols found")
                return None
                
            # Extract top movers (limit to 50 for manageable watchlist)
            symbols = [item["symbol"] for item in high_change[:50]]
            logger.info(f"📊 Found {len(symbols)} high change symbols")
            
            # Format for TradingView
            formatted_symbols = self.format_symbols_for_tradingview(symbols, "BLOFIN")
            
            # Write to file
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, 'w') as f:
                for symbol in formatted_symbols:
                    f.write(f"{symbol}\n")
            
            logger.info(f"✅ Generated high change watchlist file: {filepath}")
            logger.info(f"📝 Contains {len(formatted_symbols)} symbols")
            
            return filepath
            
        except Exception as e:
            logger.error(f"❌ Error generating high change watchlist file: {e}")
            return None
    
    def generate_both_files(self) -> tuple:
        """Generate both watchlist files"""
        logger.info("🚀 Generating both TradingView import files...")
        
        blofin_file = self.generate_blofin_watchlist_file()
        high_change_file = self.generate_high_change_watchlist_file()
        
        return blofin_file, high_change_file
    
    def preview_file_contents(self, filepath: str, lines: int = 10):
        """Preview the contents of a generated file"""
        try:
            if not os.path.exists(filepath):
                logger.error(f"❌ File not found: {filepath}")
                return
                
            with open(filepath, 'r') as f:
                content = f.readlines()
            
            logger.info(f"📄 Preview of {filepath} (first {lines} lines):")
            for i, line in enumerate(content[:lines], 1):
                logger.info(f"  {i:2d}. {line.strip()}")
                
            if len(content) > lines:
                logger.info(f"  ... and {len(content) - lines} more lines")
                
        except Exception as e:
            logger.error(f"❌ Error previewing file: {e}")


def generate_tradingview_import_files():
    """Standalone function to generate import files"""
    generator = TradingViewFileGenerator()
    
    print("🚀 Generating TradingView import files...")
    print("=" * 50)
    
    # Generate both files
    blofin_file, high_change_file = generator.generate_both_files()
    
    print("\n📁 Generated Files:")
    if blofin_file:
        print(f"✅ Blofin Pairs: {blofin_file}")
        generator.preview_file_contents(blofin_file, 5)
    else:
        print("❌ Failed to generate Blofin pairs file")
        
    if high_change_file:
        print(f"✅ High Change: {high_change_file}")
        generator.preview_file_contents(high_change_file, 5)
    else:
        print("❌ Failed to generate high change file")
    
    print(f"\n💡 Usage:")
    print(f"1. Go to TradingView chart")
    print(f"2. Open watchlist panel")
    print(f"3. Click import/add watchlist")
    print(f"4. Upload the generated .txt files")
    
    return blofin_file, high_change_file


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    generate_tradingview_import_files()