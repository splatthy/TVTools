#!/usr/bin/env python3
"""
Test the full TVTools integration - from data discovery to TradingView automation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tvtools.automation.integration import TradingViewIntegration, sync_all_watchlists
from tvtools.utils import setup_logging, Config

def main():
    setup_logging(level="INFO")
    
    print("🚀 TVTools Full Integration Test")
    print("=" * 50)
    print()
    print("This will test the complete workflow:")
    print("1. 🔍 Discover Blofin perpetual pairs from TradingView")
    print("2. 📊 Build watchlists with market data")
    print("3. 🤖 Automate TradingView to create watchlists")
    print()
    print("⚠️  IMPORTANT:")
    print("   - A Chrome browser window will open")
    print("   - You'll need to manually log in to TradingView")
    print("   - The script will create 2 watchlists:")
    print("     • TVTools - Blofin Pairs (all perpetuals)")
    print("     • TVTools - High Change (top movers)")
    print()
    
    # Get session ID from config
    config = Config()
    session_id = config.TRADINGVIEW_SESSION_ID
    
    if not session_id:
        print("⚠️  No TradingView session ID found in .env file")
        print("   The script will still work, but may be slower")
        print("   To speed up data fetching, add TRADINGVIEW_SESSION_ID to .env")
        print()
    
    input("Press Enter to start the full integration test...")
    
    try:
        print("\n🔨 Initializing integration...")
        integration = TradingViewIntegration(session_id=session_id, headless=False)
        
        print("\n1️⃣ Testing Blofin perpetuals sync...")
        print("   This will:")
        print("   - Fetch all Blofin perpetual pairs from TradingView")
        print("   - Get current market data for each pair")
        print("   - Create a watchlist in TradingView")
        print()
        
        blofin_success = integration.sync_blofin_watchlist_to_tradingview(
            watchlist_name="TVTools - Blofin Test"
        )
        
        if blofin_success:
            print("✅ Blofin watchlist sync completed successfully!")
        else:
            print("❌ Blofin watchlist sync failed")
            print("   Check the logs above for details")
        
        print("\n" + "="*50)
        print("\n2️⃣ Testing high change symbols sync...")
        print("   This will:")
        print("   - Analyze price changes for all symbols")
        print("   - Filter for symbols with >5% change")
        print("   - Create a watchlist with top movers")
        print()
        
        high_change_success = integration.sync_high_change_watchlist_to_tradingview(
            min_change=5.0,
            watchlist_name="TVTools - High Change Test"
        )
        
        if high_change_success:
            print("✅ High change watchlist sync completed successfully!")
        else:
            print("❌ High change watchlist sync failed")
            print("   Check the logs above for details")
        
        print("\n" + "="*50)
        print("\n📊 Test Summary:")
        print(f"   Blofin Pairs: {'✅ Success' if blofin_success else '❌ Failed'}")
        print(f"   High Change: {'✅ Success' if high_change_success else '❌ Failed'}")
        
        if blofin_success and high_change_success:
            print("\n🎉 ALL TESTS PASSED!")
            print("   Check your TradingView account for the new watchlists:")
            print("   • TVTools - Blofin Test")
            print("   • TVTools - High Change Test")
            return True
        else:
            print("\n💥 Some tests failed")
            print("   Check the error messages above for troubleshooting")
            return False
            
    except Exception as e:
        print(f"\n❌ Integration test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sync_all():
    """Test the sync_all_watchlists function"""
    print("\n" + "="*50)
    print("🔄 Testing sync_all_watchlists function...")
    print()
    print("This will create both watchlists in one go:")
    print("• TVTools - Blofin Pairs")
    print("• TVTools - High Change")
    print()
    
    input("Press Enter to test sync_all_watchlists...")
    
    config = Config()
    session_id = config.TRADINGVIEW_SESSION_ID
    
    success = sync_all_watchlists(session_id=session_id, headless=False)
    
    if success:
        print("\n🎉 sync_all_watchlists completed successfully!")
        return True
    else:
        print("\n❌ sync_all_watchlists failed")
        return False

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Individual tests (recommended for first run)")
    print("2. Sync all watchlists at once")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        success = test_sync_all()
    else:
        success = main()
    
    if success:
        print("\n🎯 Integration tests completed successfully!")
        print("   TVTools is working end-to-end! 🚀")
    else:
        print("\n💥 Integration tests failed.")
        print("   Check the error messages for troubleshooting.")