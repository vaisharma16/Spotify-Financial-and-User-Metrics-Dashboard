import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Load dataset
file_path = 'Spotify Quarterly.csv'  # Ensure this file is in the correct location
spotify_data = pd.read_csv(file_path)

# Preprocessing
data = spotify_data.copy()
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')  # Convert Date to datetime

# Sidebar Filters
st.sidebar.header("Filters")
st.sidebar.markdown("<span style='color:white; font-size:16px;'>Use the filters below to customize the dashboard view.</span>", unsafe_allow_html=True)
selected_start_date = st.sidebar.date_input("Start Date", data['Date'].min())
selected_end_date = st.sidebar.date_input("End Date", data['Date'].max())

if selected_start_date > selected_end_date:
    st.sidebar.error("Start date must be before end date.")
data_filtered = data[(data['Date'] >= pd.to_datetime(selected_start_date)) &
                     (data['Date'] <= pd.to_datetime(selected_end_date))]

# App Layout
st.markdown("<h1 style='color:white; text-align:center;'>Spotify Financial Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:white; font-size:22px;'>An advanced dashboard to explore Spotify's financial and user metrics interactively.</p>", unsafe_allow_html=True)

# Overview Section
st.markdown("<h2 style='color:white;'>Overview</h2>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue (M EUR)", f"{data_filtered['Total Revenue'].sum():,.2f}")
col2.metric("Gross Profit (M EUR)", f"{data_filtered['Gross Profit'].sum():,.2f}")
st.markdown("<p style='color:white; font-size:18px;'>NOTE : ARPU is Average Revenue Per User", unsafe_allow_html=True)
col3.metric("Average Premium ARPU (EUR)", f"{data_filtered['Premium ARPU'].mean():.2f}")
col4.metric("Average MAUs (M)", f"{data_filtered['MAUs'].mean():,.2f}")
st.markdown("<p style='color:white;font-size:22px'>These metrics provide a snapshot of Spotify's overall financial health and user engagement.</p>", unsafe_allow_html=True)

# Revenue Analysis
st.markdown("<h2 style='color:white;'>Revenue Analysis</h2>", unsafe_allow_html=True)
revenue_fig = go.Figure()
revenue_fig.add_trace(go.Scatter(x=data_filtered['Date'], y=data_filtered['Premium Revenue'], 
                                 mode='lines+markers', name='Premium Revenue',
                                 line=dict(color='purple')))
revenue_fig.add_trace(go.Scatter(x=data_filtered['Date'], y=data_filtered['Ad Revenue'], 
                                 mode='lines+markers', name='Ad Revenue',
                                 line=dict(color='orange')))
revenue_fig.update_layout(title="Revenue Breakdown Over Time", 
                          xaxis_title="Date", yaxis_title="Revenue (M EUR)",
                          legend_title="Revenue Type",
                          template="plotly_white",
                          plot_bgcolor="black",
                          paper_bgcolor="black")
st.plotly_chart(revenue_fig)
st.markdown("<p style='color:white; font-size:22px'>The visualization shows Premium Revenue consistently surpassing Ad Revenue, highlighting the importance of premium users in Spotify's revenue model.</p>", unsafe_allow_html=True)

# User Trends
st.markdown("<h2 style='color:white;'>User Trends</h2>", unsafe_allow_html=True)
users_fig = go.Figure()
users_fig.add_trace(go.Scatter(x=data_filtered['Date'], y=data_filtered['MAUs'],
                               mode='lines+markers', name='Total MAUs',
                               line=dict(color='blue')))
users_fig.add_trace(go.Scatter(x=data_filtered['Date'], y=data_filtered['Premium MAUs'],
                               mode='lines+markers', name='Premium MAUs',
                               line=dict(color='gold')))
users_fig.add_trace(go.Scatter(x=data_filtered['Date'], y=data_filtered['Ad MAUs'],
                               mode='lines+markers', name='Ad MAUs',
                               line=dict(color='cyan')))
users_fig.update_layout(title="Monthly Active Users (MAUs) Over Time",
                        xaxis_title="Date", yaxis_title="Users (M)",
                        legend_title="User Type",
                        template="plotly_white",
                        plot_bgcolor="black",
                        paper_bgcolor="black")
st.plotly_chart(users_fig)
st.markdown("<p style='color:white; font-size:22px'>The trend highlights steady growth in total MAUs, with a significant portion coming from Ad-supported users, indicating strong engagement from non-premium users.</p>", unsafe_allow_html=True)

# ARPU Analysis
st.markdown("<h2 style='color:white;font-size:22px'>ARPU (Average Revenue Per User)</h2>", unsafe_allow_html=True)
arpu_fig = px.line(data_filtered, x='Date', y='Premium ARPU', 
                   title="Premium ARPU Over Time", 
                   labels={'Premium ARPU': 'ARPU (EUR)'},
                   color_discrete_sequence=px.colors.sequential.Viridis)
arpu_fig.update_layout(template="plotly_white",
                        plot_bgcolor="black",
                        paper_bgcolor="black")
st.plotly_chart(arpu_fig)
st.markdown("<p style='color:white;font-size:22px'>Premium ARPU has shown slight fluctuations, indicating variations in user spending habits or pricing strategies.</p>", unsafe_allow_html=True)

# Expense Analysis
st.markdown("<h2 style='color:white;font-size:22px'>Expense Distribution</h2>", unsafe_allow_html=True)
expenses = data_filtered[['Sales and Marketing Cost', 'Research and Development Cost', 'Genreal and Adminstraive Cost']].sum()
expense_fig = px.pie(values=expenses.values, names=expenses.index, 
                     title="Total Expenses Distribution",
                     color_discrete_sequence=px.colors.sequential.Viridis)
expense_fig.update_layout(template="plotly_white",
                           plot_bgcolor="black",
                           paper_bgcolor="black")
st.plotly_chart(expense_fig)
st.markdown("<p style='color:white; font-size:22px'>Research and Development costs dominate, showcasing Spotify's focus on innovation and platform improvement.</p>", unsafe_allow_html=True)
# Advanced Insights: Profitability Over Time
st.markdown("<h2 style='color:white;'>Profitability Over Time</h2>", unsafe_allow_html=True)
profitability_fig = go.Figure()
profitability_fig.add_trace(go.Bar(x=data_filtered['Date'], y=data_filtered['Gross Profit'],
                                   name='Gross Profit', marker_color="#ffff00"))
profitability_fig.add_trace(go.Scatter(x=data_filtered['Date'], y=data_filtered['Total Revenue'],
                                       mode='lines+markers', name='Total Revenue',
                                       line=dict(color='blue', dash='dot')))
profitability_fig.update_layout(title="Profitability Trends",
                                 xaxis_title="Date", yaxis_title="Amount (M EUR)",
                                 legend_title="Metric",
                                 template="plotly_white",
                                 plot_bgcolor="black",
                                 paper_bgcolor="black")
st.plotly_chart(profitability_fig)
st.markdown("<p style='color:white; font-size:22px'>This visualization illustrates the positive correlation between revenue and profitability, affirming the effectiveness of Spotify's revenue strategies.</p>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='color:white; text-align:center;'>Created by Vaibhav Sharma. A showcase of advanced data visualization using Streamlit and Plotly.</p>", unsafe_allow_html=True)