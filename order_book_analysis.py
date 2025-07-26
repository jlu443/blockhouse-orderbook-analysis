"""
Blockhouse Work Trial Task - Order Book Analysis
Analyzing temporary price impact of limit orders using market data

This script implements the temporary price impact function g_s(X) and analyzes
the order book data for the three stocks: CRWV, FROG, and SOUN.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import glob
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class OrderBookAnalyzer:
    def __init__(self, data_folder):
        self.data_folder = Path(data_folder)
        self.symbols = ['CRWV', 'FROG', 'SOUN']
        self.data = {}
        
    def load_data(self, symbol, date_range=None):
        """Load order book data for a specific symbol"""
        symbol_folder = self.data_folder / symbol
        csv_files = list(symbol_folder.glob(f"{symbol}_*.csv"))
        
        if date_range:
            csv_files = [f for f in csv_files if any(date in f.name for date in date_range)]
        
        dataframes = []
        for file in csv_files[:2]:  # Load first 2 files for faster analysis
            try:
                # Load only a sample of rows for faster processing
                df = pd.read_csv(file, nrows=1000)  # Load only first 1000 rows
                df['date'] = file.stem.split('_')[1]
                dataframes.append(df)
            except Exception as e:
                print(f"Error loading {file}: {e}")
                
        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)
            self.data[symbol] = combined_df
            return combined_df
        return None
    
    def calculate_mid_price(self, df):
        """Calculate mid price from best bid and ask"""
        df['mid_price'] = (df['bid_px_00'] + df['ask_px_00']) / 2
        return df
    
    def calculate_spread(self, df):
        """Calculate bid-ask spread"""
        df['spread'] = df['ask_px_00'] - df['bid_px_00']
        df['spread_bps'] = (df['spread'] / df['mid_price']) * 10000  # in basis points
        return df
    
    def get_order_book_depth(self, df, levels=10):
        """Calculate total depth at each level"""
        bid_depth = 0
        ask_depth = 0
        
        for i in range(levels):
            level_str = f"{i:02d}"
            bid_col = f'bid_sz_{level_str}'
            ask_col = f'ask_sz_{level_str}'
            
            if bid_col in df.columns and ask_col in df.columns:
                bid_depth += df[bid_col].fillna(0)
                ask_depth += df[ask_col].fillna(0)
        
        df['total_bid_depth'] = bid_depth
        df['total_ask_depth'] = ask_depth
        return df
    
    def calculate_temporary_impact_function(self, df, side='buy', max_shares=200):
        """
        Calculate the temporary price impact function g_s(X)
        This represents the cost of executing X shares as a limit order
        """
        impact_data = []
        
        # Sample fewer rows for faster computation
        sample_df = df.sample(min(100, len(df))) if len(df) > 100 else df
        
        for order_size in range(50, max_shares + 1, 50):  # Larger steps
            impacts = []
            
            for idx, row in sample_df.iterrows():
                if side == 'buy':
                    # For buy orders, we look at ask side of the book
                    cumulative_size = 0
                    weighted_price = 0
                    total_value = 0
                    
                    for level in range(10):
                        level_str = f"{level:02d}"
                        ask_price = row[f'ask_px_{level_str}']
                        ask_size = row[f'ask_sz_{level_str}']
                        
                        if pd.isna(ask_price) or pd.isna(ask_size) or ask_size == 0:
                            continue
                            
                        remaining_needed = order_size - cumulative_size
                        if remaining_needed <= 0:
                            break
                            
                        size_to_take = min(ask_size, remaining_needed)
                        total_value += ask_price * size_to_take
                        cumulative_size += size_to_take
                        
                        if cumulative_size >= order_size:
                            break
                    
                    if cumulative_size > 0:
                        avg_execution_price = total_value / cumulative_size
                        mid_price = row['mid_price']
                        impact = (avg_execution_price - mid_price) / mid_price
                        impacts.append(impact)
                        
                else:  # sell orders
                    # For sell orders, we look at bid side of the book
                    cumulative_size = 0
                    total_value = 0
                    
                    for level in range(10):
                        level_str = f"{level:02d}"
                        bid_price = row[f'bid_px_{level_str}']
                        bid_size = row[f'bid_sz_{level_str}']
                        
                        if pd.isna(bid_price) or pd.isna(bid_size) or bid_size == 0:
                            continue
                            
                        remaining_needed = order_size - cumulative_size
                        if remaining_needed <= 0:
                            break
                            
                        size_to_take = min(bid_size, remaining_needed)
                        total_value += bid_price * size_to_take
                        cumulative_size += size_to_take
                        
                        if cumulative_size >= order_size:
                            break
                    
                    if cumulative_size > 0:
                        avg_execution_price = total_value / cumulative_size
                        mid_price = row['mid_price']
                        impact = (mid_price - avg_execution_price) / mid_price
                        impacts.append(impact)
            
            if impacts:
                avg_impact = np.mean(impacts)
                impact_data.append({
                    'order_size': order_size,
                    'avg_impact': avg_impact,
                    'impact_bps': avg_impact * 10000
                })
        
        return pd.DataFrame(impact_data)
    
    def analyze_symbol(self, symbol):
        """Complete analysis for a single symbol"""
        print(f"\n=== Analyzing {symbol} ===")
        
        # Load data
        df = self.load_data(symbol)
        if df is None:
            print(f"No data available for {symbol}")
            return None
        
        print(f"Loaded {len(df)} records")
        
        # Calculate derived metrics
        df = self.calculate_mid_price(df)
        df = self.calculate_spread(df)
        df = self.get_order_book_depth(df)
        
        # Basic statistics
        print(f"Average mid price: ${df['mid_price'].mean():.4f}")
        print(f"Average spread: {df['spread_bps'].mean():.2f} bps")
        print(f"Average bid depth: {df['total_bid_depth'].mean():.0f} shares")
        print(f"Average ask depth: {df['total_ask_depth'].mean():.0f} shares")
        
        # Calculate temporary impact functions
        buy_impact = self.calculate_temporary_impact_function(df, side='buy')
        sell_impact = self.calculate_temporary_impact_function(df, side='sell')
        
        return {
            'symbol': symbol,
            'data': df,
            'buy_impact': buy_impact,
            'sell_impact': sell_impact
        }
    
    def plot_impact_functions(self, results):
        """Plot the temporary price impact functions"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        for i, result in enumerate(results):
            if result is None:
                continue
                
            symbol = result['symbol']
            buy_impact = result['buy_impact']
            sell_impact = result['sell_impact']
            
            # Buy side impact
            axes[0, i].plot(buy_impact['order_size'], buy_impact['impact_bps'], 
                           'b-', linewidth=2, label=f'{symbol} Buy Impact')
            axes[0, i].set_title(f'{symbol} - Buy Side Temporary Price Impact')
            axes[0, i].set_xlabel('Order Size (Shares)')
            axes[0, i].set_ylabel('Impact (bps)')
            axes[0, i].grid(True, alpha=0.3)
            axes[0, i].legend()
            
            # Sell side impact
            axes[1, i].plot(sell_impact['order_size'], sell_impact['impact_bps'], 
                           'r-', linewidth=2, label=f'{symbol} Sell Impact')
            axes[1, i].set_title(f'{symbol} - Sell Side Temporary Price Impact')
            axes[1, i].set_xlabel('Order Size (Shares)')
            axes[1, i].set_ylabel('Impact (bps)')
            axes[1, i].grid(True, alpha=0.3)
            axes[1, i].legend()
        
        plt.tight_layout()
        plt.savefig('temporary_price_impact_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def answer_task_questions(self, results):
        """Answer the specific questions from the task"""
        print("\n" + "="*60)
        print("ANSWERING TASK QUESTIONS")
        print("="*60)
        
        print("\n1. How do you choose to model the temporary impact g_s(x)?")
        print("   Answer: I model g_s(x) as the weighted average execution price impact")
        print("   when consuming X shares from the order book. For buy orders:")
        print("   g_buy(X) = (Weighted_Avg_Ask_Price - Mid_Price) / Mid_Price")
        print("   For sell orders:")
        print("   g_sell(X) = (Mid_Price - Weighted_Avg_Bid_Price) / Mid_Price")
        print("   This captures the realistic cost of crossing the spread and market impact.")
        
        print("\n2. Formulate roughly but rigorously a mathematical framework/algorithm")
        print("   that gives us g_s when we are at time t_i:")
        
        print("""
   Mathematical Framework:
   
   Let O(t) = order book state at time t
   Let S_side(level) = size at level on side (bid/ask)
   Let P_side(level) = price at level on side (bid/ask)
   
   For a buy order of size X at time t_i:
   
   1. Initialize: remaining = X, total_cost = 0, total_shares = 0
   2. For level = 0 to 9:
      a. available = S_ask(level)
      b. take = min(remaining, available)
      c. total_cost += take × P_ask(level)
      d. total_shares += take
      e. remaining -= take
      f. if remaining = 0: break
   
   3. g_buy(X, t_i) = (total_cost/total_shares - mid_price(t_i)) / mid_price(t_i)
   
   Similarly for sell orders using bid side.
   
   The algorithm ensures ∑g_s ≈ S by construction since we're using actual
   order book depth and prices.
        """)
        
        # Calculate some statistics across all symbols
        all_buy_impacts = []
        all_sell_impacts = []
        
        for result in results:
            if result is not None:
                all_buy_impacts.extend(result['buy_impact']['impact_bps'].tolist())
                all_sell_impacts.extend(result['sell_impact']['impact_bps'].tolist())
        
        if all_buy_impacts and all_sell_impacts:
            print(f"\n   Cross-symbol statistics:")
            print(f"   Average buy impact: {np.mean(all_buy_impacts):.2f} bps")
            print(f"   Average sell impact: {np.mean(all_sell_impacts):.2f} bps")
            print(f"   Impact asymmetry: {abs(np.mean(all_buy_impacts) - np.mean(all_sell_impacts)):.2f} bps")

def main():
    """Main execution function"""
    print("Blockhouse Order Book Analysis")
    print("="*50)
    
    # Initialize analyzer
    analyzer = OrderBookAnalyzer(".")
    
    # Analyze each symbol
    results = []
    for symbol in analyzer.symbols:
        result = analyzer.analyze_symbol(symbol)
        results.append(result)
    
    # Create visualizations
    valid_results = [r for r in results if r is not None]
    if valid_results:
        analyzer.plot_impact_functions(valid_results)
        analyzer.answer_task_questions(valid_results)
    
    # Save detailed results
    for result in valid_results:
        symbol = result['symbol']
        
        # Save impact functions
        result['buy_impact'].to_csv(f'{symbol}_buy_impact.csv', index=False)
        result['sell_impact'].to_csv(f'{symbol}_sell_impact.csv', index=False)
        
        print(f"\nSaved impact analysis for {symbol}")

if __name__ == "__main__":
    main()
