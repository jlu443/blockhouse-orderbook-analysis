"""
Generate charts from C++ order book analysis results
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_cpp_charts():
    """Create charts from C++ generated CSV files"""
    
    symbols = ['CRWV', 'FROG', 'SOUN']
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Temporary Price Impact Analysis (C++ Results)', fontsize=16, fontweight='bold')
    
    for i, symbol in enumerate(symbols):
        try:
            # Load C++ generated CSV files
            buy_impact = pd.read_csv(f'{symbol}_buy_impact.csv')
            sell_impact = pd.read_csv(f'{symbol}_sell_impact.csv')
            
            # Plot buy side impact
            axes[0, i].plot(buy_impact['order_size'], buy_impact['impact_bps'], 
                           'b-', linewidth=2.5, marker='o', markersize=4, 
                           label=f'{symbol} Buy Impact')
            axes[0, i].set_title(f'{symbol} - Buy Side Impact\\n(C++ Analysis)', fontweight='bold')
            axes[0, i].set_xlabel('Order Size (Shares)')
            axes[0, i].set_ylabel('Impact (bps)')
            axes[0, i].grid(True, alpha=0.3)
            axes[0, i].legend()
            
            # Add statistics text
            min_impact = buy_impact['impact_bps'].min()
            max_impact = buy_impact['impact_bps'].max()
            axes[0, i].text(0.05, 0.95, f'Range: {min_impact:.1f}-{max_impact:.1f} bps', 
                           transform=axes[0, i].transAxes, fontsize=10, 
                           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7),
                           verticalalignment='top')
            
            # Plot sell side impact
            axes[1, i].plot(sell_impact['order_size'], sell_impact['impact_bps'], 
                           'r-', linewidth=2.5, marker='s', markersize=4,
                           label=f'{symbol} Sell Impact')
            axes[1, i].set_title(f'{symbol} - Sell Side Impact\\n(C++ Analysis)', fontweight='bold')
            axes[1, i].set_xlabel('Order Size (Shares)')
            axes[1, i].set_ylabel('Impact (bps)')
            axes[1, i].grid(True, alpha=0.3)
            axes[1, i].legend()
            
            # Add statistics text
            min_impact = sell_impact['impact_bps'].min()
            max_impact = sell_impact['impact_bps'].max()
            axes[1, i].text(0.05, 0.95, f'Range: {min_impact:.1f}-{max_impact:.1f} bps', 
                           transform=axes[1, i].transAxes, fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7),
                           verticalalignment='top')
            
        except FileNotFoundError:
            axes[0, i].text(0.5, 0.5, f'No data for {symbol}', 
                           transform=axes[0, i].transAxes, ha='center', va='center')
            axes[1, i].text(0.5, 0.5, f'No data for {symbol}', 
                           transform=axes[1, i].transAxes, ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig('cpp_price_impact_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ Chart saved as 'cpp_price_impact_analysis.png'")
    
    # Also create a comparison chart
    create_comparison_chart(symbols)

def create_comparison_chart(symbols):
    """Create a comparison chart showing all symbols together"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Price Impact Comparison Across Symbols (C++ Results)', fontsize=16, fontweight='bold')
    
    colors = ['blue', 'green', 'orange']
    
    for i, symbol in enumerate(symbols):
        try:
            buy_impact = pd.read_csv(f'{symbol}_buy_impact.csv')
            sell_impact = pd.read_csv(f'{symbol}_sell_impact.csv')
            
            # Buy side comparison
            ax1.plot(buy_impact['order_size'], buy_impact['impact_bps'], 
                    color=colors[i], linewidth=2, marker='o', markersize=3,
                    label=f'{symbol}')
            
            # Sell side comparison  
            ax2.plot(sell_impact['order_size'], sell_impact['impact_bps'],
                    color=colors[i], linewidth=2, marker='s', markersize=3,
                    label=f'{symbol}')
            
        except FileNotFoundError:
            continue
    
    ax1.set_title('Buy Side Impact Comparison', fontweight='bold')
    ax1.set_xlabel('Order Size (Shares)')
    ax1.set_ylabel('Impact (bps)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    ax2.set_title('Sell Side Impact Comparison', fontweight='bold') 
    ax2.set_xlabel('Order Size (Shares)')
    ax2.set_ylabel('Impact (bps)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('cpp_impact_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Comparison chart saved as 'cpp_impact_comparison.png'")

if __name__ == "__main__":
    print("🎨 Creating charts from C++ analysis results...")
    create_cpp_charts()
    print("📊 Chart generation complete!")
