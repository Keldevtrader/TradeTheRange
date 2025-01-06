import streamlit as st

# Function to calculate strategy with remaining 20% and max profit
def calculate_strategy_with_remaining_20_and_max_profit(initial_capital, buy_prices, sell_prices):
    # Buy distribution percentages (20% at 140, 20% at 135, 20% at 130, 40% at 131)
    buy_percentages = [0.20, 0.20, 0.20, 0.40]
    
    # Total amount invested in each level
    investments = [initial_capital * buy_percentages[i] for i in range(3)]
    
    # Calculate returns based on the sell prices (first 80%)
    sell_values = []
    for i, invest in enumerate(investments):
        sell_value = invest * (sell_prices[i] / buy_prices[i])  # Sell at respective sell prices
        sell_values.append(sell_value)
    
    # Total value after selling 80% of the position
    total_sold_value = sum(sell_values)
    
    # Calculate the remaining amount (final 20%) that stays in the market
    remaining_investment = initial_capital * buy_percentages[3]
    
    # 1. Calculate the profits from the 80% sold and the remaining 20% (which is still invested)
    remaining_investment_value = remaining_investment * (sell_prices[2] / buy_prices[2])  # assuming the stock stays at 130

    total_value = total_sold_value + remaining_investment_value
    
    # Profit Calculation
    profit = total_value - initial_capital
    profit_percentage = (profit / initial_capital) * 100
    
    # 2. Breakeven price for the remaining 20%
    breakeven_price = (initial_capital - total_sold_value) / remaining_investment * buy_prices[2]
    
    # 3. Maximum Profit Calculation (full range: buy low at 130 and sell high at 142)
    max_profit = (sell_prices[2] - buy_prices[2]) / buy_prices[2] * 100  # Buy at 130, sell at 142
    
    return total_value, profit, profit_percentage, breakeven_price, max_profit

# Streamlit UI
st.title("Investment Strategy Calculator")

# Input fields for capital, buy levels, and sell levels
initial_capital = st.number_input("Initial Capital ($)", min_value=0.0, value=10000.0, step=100.0)

# Initialize buy and sell prices as empty lists
buy_prices = []
sell_prices = []

# Input fields for buy prices (3 levels)
default_buy_prices = [140, 135, 130]
for i in range(3):
    buy_price = st.number_input(f"Buy Price Level {i+1} ($)", min_value=0.0, value=float(default_buy_prices[i]), step=1.0)
    buy_prices.append(buy_price)

# Input fields for sell prices (3 levels)
default_sell_prices = [135, 140, 142]
for i in range(3):
    sell_price = st.number_input(f"Sell Price Level {i+1} ($)", min_value=0.0, value=float(default_sell_prices[i]), step=1.0)
    sell_prices.append(sell_price)

# Calculate button
if st.button("Calculate"):
    # Run the calculation
    final_capital, profit, profit_percentage, breakeven_price, max_profit = calculate_strategy_with_remaining_20_and_max_profit(
        initial_capital, buy_prices, sell_prices
    )
    
    # Display results in columns
    st.subheader("Results Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Capital", f"${final_capital:.2f}")
    col2.metric("Total Profit", f"${profit:.2f}")
    col3.metric("Profit Percentage", f"{profit_percentage:.2f}%")
    
    # Add breakeven and max profit in separate columns
    col4, col5 = st.columns(2)
    col4.metric("Breakeven Price", f"${breakeven_price:.2f}")
    col5.metric("Maximum Profit %", f"{max_profit:.2f}%")
    
    # Display a summary table
    st.subheader("Detailed Breakdown")
    breakdown_data = {
        "Category": ["Initial Capital", "Total Sold Value", "Remaining Investment", "Final Capital"],
        "Value ($)": [initial_capital, final_capital - profit, initial_capital * 0.40, final_capital],
    }
    st.table(breakdown_data)
