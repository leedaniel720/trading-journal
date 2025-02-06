import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load CSV file
st.title("Trading Journal")
uploaded_file = st.file_uploader("Upload your trades CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['tradeDate'], errors='coerce')
    df['Net PnL'] = pd.to_numeric(df['NetProfit'], errors='coerce')
    df = df.dropna(subset=['Net PnL', 'Date'])
    df = df.sort_values(by='Date')
    df['Cumulative PnL'] = df['Net PnL'].cumsum()

    # Calculate trading stats
    total_trades = len(df)
    winning_trades = len(df[df['Net PnL'] > 0])
    losing_trades = len(df[df['Net PnL'] < 0])
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    avg_win = df[df['Net PnL'] > 0]['Net PnL'].mean()
    avg_loss = df[df['Net PnL'] < 0]['Net PnL'].mean()
    risk_reward_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else None
    max_drawdown = df['Cumulative PnL'].min()
    total_profit = df['Net PnL'].sum()

    # Display stats
    st.subheader("Trading Performance Stats")
    stats = {
        'Total Trades': total_trades,
        'Winning Trades': winning_trades,
        'Losing Trades': losing_trades,
        'Win Rate (%)': win_rate,
        'Avg Win': avg_win,
        'Avg Loss': avg_loss,
        'Risk-Reward Ratio': risk_reward_ratio,
        'Max Drawdown': max_drawdown,
        'Total Profit': total_profit
    }
    st.write(pd.DataFrame(stats, index=[0]))

    # Plot cumulative PnL
    st.subheader("Cumulative PnL Over Time")
    fig, ax = plt.subplots()
    ax.plot(df['Date'], df['Cumulative PnL'], marker='o', linestyle='-', color='b')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative PnL ($)')
    ax.set_title('Cumulative PnL Over Time')
    ax.grid()
    st.pyplot(fig)
