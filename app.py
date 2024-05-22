import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Set up the Streamlit page configuration
st.set_page_config(page_title='Data Visualizer',
                   layout='centered',
                   page_icon='📊')

# Author name
author_name = "Ramlavan"
# Current date
current_date = date.today().strftime("%B %d, %Y")

# Author name and current date above the title
st.write(f"Author: {author_name}")
st.write(f"Date: {current_date}")

# Title of the app
st.title('📊 Data Visualizer')

# Dropdown to select a file
github_url = "https://raw.githubusercontent.com/Ramlavn/Data-viz/master/Brain_Stroke_Analysis.csv"
csv_file_name = "Brain_Stroke_Analysis.csv"  # Name of the CSV file
selected_file = st.selectbox('Select a file', ['Choose a file', csv_file_name])

# Check if a file is selected
if selected_file != 'Choose a file':
    # Load the CSV file
    if selected_file == csv_file_name:
        df = pd.read_csv(github_url)
    else:
        st.error("Invalid file selected.")
        st.stop()

   # Display the first few rows of the DataFrame
    st.write(df.head())

    # Get the list of columns from the DataFrame
    columns = df.columns.tolist()

    # Layout with two columns for selecting X-axis, Y-axis, and plot type
    col1, col2 = st.columns(2)
    with col1:
        # Dropdown for selecting X-axis
        x_axis = st.selectbox('Select the X-axis', options=["None"] + columns, key='x_axis')
        # Dropdown for selecting Y-axis
        y_axis = st.selectbox('Select the Y-axis', options=["None"] + columns, key='y_axis')

    with col2:
        # Dropdown for selecting the type of plot
        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        plot_type = st.selectbox('Select the type of plot', options=plot_list, key='plot_type')

    # Button to generate the plot
    if st.button('Generate Plot'):
        # Function to generate the selected plot
        def generate_plot(df, x_axis, y_axis, plot_type):
            fig, ax = plt.subplots(figsize=(6, 4))

            if plot_type == 'Line Plot':
                sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Bar Chart':
                sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Scatter Plot':
                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Distribution Plot':
                if x_axis != "None":
                    sns.histplot(df[x_axis], kde=True, ax=ax)
                else:
                    st.error("Please select a column for the X-axis.")
                    return
            elif plot_type == 'Count Plot':
                if x_axis != "None":
                    sns.countplot(x=df[x_axis], ax=ax)
                    plt.xlabel(x_axis, fontsize=10)
                elif y_axis != "None":
                    sns.countplot(y=df[y_axis], ax=ax)
                    plt.ylabel(y_axis, fontsize=10)
                else:
                    st.error("Please select a column for either the X-axis or Y-axis.")
                    return
                plt.ylabel('Count', fontsize=10)

            # Adjust plot settings
            ax.tick_params(axis='x', labelsize=10)  # Adjust x-axis label size
            ax.tick_params(axis='y', labelsize=10)  # Adjust y-axis label size

            # Set the title and axis labels
            if plot_type != 'Count Plot':
                plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
                plt.xlabel(x_axis, fontsize=10)
                plt.ylabel(y_axis, fontsize=10)

            # Display the plot
            st.pyplot(fig)

        # Generate the plot based on user selection
        generate_plot(df, x_axis, y_axis, plot_type)
