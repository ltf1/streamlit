#!pip install streamlit
#!pip install seaborn
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import seaborn as sns

#df=pd.read_csv("active_users.csv")
#df['ds'] = pd.to_datetime(df['ds'])



st.title("İzle Weekly Trends")

active_users_df = pd.read_csv("active_users.csv")
installs_df = pd.read_csv("installs.csv")
playback_duration_df = pd.read_csv("play.csv")

# Create a dictionary to map the dataset names to their corresponding DataFrames
data_dict = {"Active Users": active_users_df, "Installs": installs_df, "Play": playback_duration_df}

# Define colors for each day of the week
dayofweek_colors = {'Monday': 'blue', 'Tuesday': 'green', 'Wednesday': 'orange', 'Thursday': 'red', 'Friday': 'purple', 'Saturday': 'brown', 'Sunday': 'pink'}

year_colors = {2020: 'blue', 2021: 'green', 2022: 'orange', 2023: 'purple'}

# Create a dropdown widget to allow the user to select which dataset to display
selected_dataset = st.selectbox("Select dataset", list(data_dict.keys()), key="multiselect2")



# Create a multi-select widget to allow the user to select which days to plot
selected_days = st.multiselect('Select days to plot', list(dayofweek_colors.keys()), default=list(dayofweek_colors.keys()), key="dasdas")




# Get the DataFrame for the selected dataset
df = data_dict[selected_dataset]
df['ds'] = pd.to_datetime(df['ds'])


# Plot that shows the historical data by day of the week
def plot_data(df, selected_days, selected_dataset):
    plt.close()
    fig, ax = plt.subplots(figsize=(12,6))
    if selected_days:
        df_selected = df[df['ds'].dt.day_name().isin(selected_days)]
        for day in selected_days:
            df_day = df_selected[df_selected['ds'].dt.day_name() == day]
            ax.scatter(df_day['ds'], df_day['y'], c=dayofweek_colors[day], label=day)
        ax.legend()
    #else:
    #    ax.scatter(df['ds'], df['y'], c=df['ds'].dt.dayofweek.map(dayofweek_colors))
    #    handles = [mpatches.Patch(color=v, label=k) for v, k in zip(dayofweek_colors.values(), dayofweek_colors.keys())]
    #    legend = ax.legend(handles=handles, bbox_to_anchor=(1, 0.5), title="Day of the week")
    #    ax.add_artist(legend)
    plt.xlabel('Date')
    plt.ylabel(selected_dataset)
    plt.title(f"{selected_dataset} by day of the week")
    #plt.suptitle("İzle Weekly Trends", fontsize=20)
    st.pyplot(fig)



def plot_monthly(df, selected_dataset, selected_years):
    df_selected = df[df["ds"].dt.year.isin(selected_years)]
    fig, ax = plt.subplots(figsize=(12, 6))
    for year in selected_years:
        by_years = df_selected[df_selected['ds'].dt.year == year]
        by_years['year'] = by_years.ds.dt.year
        by_years['month'] = by_years.ds.dt.month
        by_years = by_years.groupby(['year', 'month']).sum().reset_index()
        sns_data = by_years.pivot(index='month', columns='year', values='y')
        color = year_colors.get(year, 'blue') # get the color from the year_colors dictionary
        sns.lineplot(data=sns_data, palette=[color], linewidth=2.5, ax=ax, label=str(year), legend=False)
    plt.xlabel('Month')
    plt.ylabel(selected_dataset)
    plt.title(f"{selected_dataset} by Month")
    plt.legend()
    st.pyplot(fig)




# Call the plot_data function to create the plot
#plt.ylabel(selected_dataset)
# Add title for section

plot_data(df, selected_days, selected_dataset)

st.title("İzle Monthly Trends")

selected_years = st.multiselect('Select years to plot', list(year_colors.keys()), default=list(year_colors.keys()), key="dfsdaa")


plot_monthly(df, selected_dataset, selected_years)

