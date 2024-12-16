import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)  # Adjust if data is preprocessed differently

# File path (adjust based on your local file setup)
file_path = "data.csv"  # Replace with actual file path
data = load_data(file_path)

# Dashboard title
st.title("Bike Rental Analysis Dashboard")

# Sidebar
st.sidebar.header("Filter Options")
weather_filter = st.sidebar.multiselect(
    "Select Weather Conditions",
    options=data['weathersit'].unique(),
    default=data['weathersit'].unique()
)

user_type = st.sidebar.selectbox(
    "Select User Type",
    options=["Casual", "Registered"]
)

# Filtered Data
filtered_data = data[data['weathersit'].isin(weather_filter)]

# Visualization: Weather Impact on Rentals
st.subheader("Impact of Weather on Bike Rentals")
weather_counts = filtered_data.groupby('weathersit')['cnt'].mean().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(data=weather_counts, x='weathersit', y='cnt', ax=ax1)
ax1.set_title("Average Bike Rentals by Weather Condition")
ax1.set_xlabel("Weather Condition")
ax1.set_ylabel("Average Rentals")
st.pyplot(fig1)

# Visualization: User Segmentation
st.subheader("User Segmentation: Casual vs Registered")
user_counts = filtered_data.groupby(['weathersit', 'user_type'])['cnt'].mean().unstack()

fig2, ax2 = plt.subplots()
user_counts.plot(kind='bar', stacked=True, ax=ax2)
ax2.set_title("Rental Distribution by User Type and Weather")
ax2.set_xlabel("Weather Condition")
ax2.set_ylabel("Average Rentals")
st.pyplot(fig2)

# Hourly Variations
st.subheader("Hourly Rental Variations")
hourly_data = filtered_data.groupby('hour')[['casual', 'registered']].mean()

fig3, ax3 = plt.subplots()
hourly_data.plot(ax=ax3)
ax3.set_title("Hourly Trends for Casual and Registered Users")
ax3.set_xlabel("Hour")
ax3.set_ylabel("Average Rentals")
st.pyplot(fig3)

# Summary
st.write("This dashboard highlights how weather and user segmentation influence bike rental trends.")
