import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Climate Equity Valuation Engine", layout="wide")

st.title("Serverless Accounting Measurement Pipeline")
st.caption("Real-Time Log-Linear Equity Valuation & Climate Risk Elasticity Modeling")

st.sidebar.header("Market-Accounting Configuration")
selected_sector = st.sidebar.selectbox("Simulated Industrial Sector", ["Global Agricultural Conglomerates", "Coastal Real Estate Investment Trusts", "Energy & Utilities Sector"])
climate_severity = st.sidebar.slider("Simulate Climate Anomaly Severity", 1.0, 5.0, 3.5)
run_simulation = st.sidebar.button("Initialize Log-Linear Valuation Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: Climate API -> Log-Linear Normalization -> Elasticity Inference")

if run_simulation:
    st.subheader(f"Active Market-Accounting Monitor: {selected_sector}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_climate = col1.empty()
    metric_earnings = col2.empty()
    metric_book = col3.empty()
    metric_equity = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(2424)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    equity_values = []
    climate_risks = []
    
    base_equity = 1500.0 
    base_climate = 10.0
    base_earnings_elasticity = 0.8
    base_book_elasticity = 0.5
    
    for i in range(100):
        if i < 30:
            current_climate = base_climate + np.random.uniform(-1.0, 1.0)
            earn_elast = base_earnings_elasticity + np.random.uniform(-0.02, 0.02)
            book_elast = base_book_elasticity + np.random.uniform(-0.02, 0.02)
            status = "MARKET STABLE"
        elif i >= 30 and i < 70:
            current_climate = base_climate + (i - 30) * (1.5 * climate_severity) + np.random.uniform(-3.0, 3.0)
            earn_elast = max(0.1, base_earnings_elasticity - (i - 30) * (0.01 * climate_severity))
            book_elast = min(1.2, base_book_elasticity + (i - 30) * (0.01 * climate_severity))
            status = "CLIMATE SHOCK PRICED IN"
        else:
            current_climate = current_climate + np.random.uniform(-2.0, 2.0)
            earn_elast = earn_elast + np.random.uniform(-0.01, 0.01) 
            book_elast = book_elast + np.random.uniform(-0.01, 0.01)
            status = "LONG-RUN ADJUSTMENT"
            
        current_climate = max(0.0, current_climate)
        
        # Simulated Log-Linear Equity Adjustment
        log_equity = np.log(base_equity) + (book_elast * 0.05) - (earn_elast * 0.1 * (current_climate/100))
        current_equity = np.exp(log_equity) * (1 + np.random.uniform(-0.005, 0.005))
            
        equity_values.append(current_equity)
        climate_risks.append(current_climate)
        
        metric_climate.metric("Global Climate Risk Index", f"{current_climate:.1f} pts", f"+{(current_climate - base_climate):.1f} Shift")
        metric_earnings.metric("Elasticity of Earnings (Negative Assoc)", f"{earn_elast:.2f}", f"{(earn_elast - base_earnings_elasticity):.2f}")
        metric_book.metric("Elasticity of Book Value (Positive Assoc)", f"{book_elast:.2f}", f"+{(book_elast - base_book_elasticity):.2f}")
        
        if status == "CLIMATE SHOCK PRICED IN":
            metric_equity.metric("Adjusted Equity Valuation", f"${current_equity:,.2f}", f"${(current_equity - base_equity):,.2f}")
        else:
            metric_equity.metric("Adjusted Equity Valuation", f"${current_equity:,.2f}", "Stable")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=equity_values, mode='lines', name='Firm Equity Valuation (USD)', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=climate_risks, mode='lines', name='Climate Risk Anomaly Index', yaxis='y2', line=dict(color='red', dash='dot')))
        
        fig.update_layout(
            title="Log-Linear Accounting Measurement: Equity Valuation vs Climate Risk Elasticity",
            xaxis=dict(title="High-Frequency Market Timeline"),
            yaxis=dict(title="Equity Value (USD)", range=[min(1000, current_equity - 200), 1600]),
            yaxis2=dict(title="Climate Risk Index (Pts)", overlaying='y', side='right', range=[0, max(100, current_climate + 10)]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if status == "CLIMATE SHOCK PRICED IN" and i == 30:
            log_placeholder.error(f"CLIMATE ALERT: Severe environmental anomaly metrics ingested at {time_steps[i].strftime('%H:%M:%S')}. Machine learning inference engine dynamically increasing elasticity of book value and discounting elasticity of earnings.")
        elif status == "LONG-RUN ADJUSTMENT" and i == 70:
            log_placeholder.warning(f"MARKET ADJUSTMENT: Log-linear valuation model stabilized at new climate-adjusted equity baseline. Investors heavily discounting future earnings potential.")
        elif status == "MARKET STABLE" and i % 5 == 0:
            log_placeholder.success(f"Log: Financial and meteorological telemetry tick {i} ingested via serverless API. Market-accounting relation operating at historical equilibrium.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The serverless cloud architecture successfully mapped the power-law relation between market data, accounting variables, and severe climate risk.")
else:
    st.info("Click 'Initialize Log-Linear Valuation Engine' in the sidebar to simulate high-frequency accounting data ingestion.")