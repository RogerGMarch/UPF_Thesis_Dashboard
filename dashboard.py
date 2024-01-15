import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import os

# Load the data

@st.cache



# Function to read an Excel data file
def read_excel_data(filename):
    # If the script is run from the directory containing the 'scr' and 'data' directories:
    data_file_path = os.path.join('data', filename)

    # Read the Excel file
    data = pd.read_excel(data_file_path,header=0)

    # Print the data or process it as needed
    return data


data = read_excel_data('TFM_TFM_Clean.xlsx')
print(data.columns.tolist())

# Streamlit app layout
st.title('TFG and TFM Dashboard')

# Filters
year = st.sidebar.multiselect('Select Year', options=data['YEAR'].unique(), default=data['YEAR'].unique())
language = st.sidebar.multiselect('Select Language', options=data['LANGUAGE'].unique(), default=data['LANGUAGE'].unique())

selected_types = st.multiselect('Select the type of work to display', 
                                options=data['TYPE'].unique(), 
                                default=data['TYPE'].unique())



# Apply filters
filtered_data = data[data['YEAR'].isin(year) & data['LANGUAGE'].isin(language) & data['TYPE'].isin(selected_types)]

# Display total count of TFG and TFM
st.header('Total Count')
st.write(f"Total TFG: {len(filtered_data[filtered_data['TYPE'] == 'TFG'])}")
st.write(f"Total TFM: {len(filtered_data[filtered_data['TYPE'] == 'TFM'])}")

st.header('Top N by Degree')

# Slider for the user to select the top N degrees
top_n = st.slider('Select the number of top degrees to display', min_value=1, max_value=200, value=10)

# Get the counts for each degree
degree_counts = filtered_data['Estudi'].value_counts()

# Select the top N degrees
top_degrees = degree_counts.head(top_n)

# Create a DataFrame
top_degrees_df = pd.DataFrame({'Degree': top_degrees.index, 'Count': top_degrees.values})

# Sort the DataFrame by 'Count' in descending order
top_degrees_df.sort_values('Count', ascending=False, inplace=True)

# Create a bar plot using Matplotlib
fig, ax = plt.subplots()
ax.bar(top_degrees_df['Degree'], top_degrees_df['Count'])
ax.set_xticklabels(top_degrees_df['Degree'], rotation=45, ha='right')
ax.set_ylabel('Count')
ax.set_title(f'Top {top_n} Degrees by Count')

# Display the plot in Streamlit
st.pyplot(fig)



st.header('Publications by Year')
publications_by_year = filtered_data['YEAR'].value_counts().sort_index()
# Check if there is any data to plot
if not publications_by_year.empty:
    plt.figure()
    # Plotting, assuming 'DATEISSUED' contains the year information
    plt.bar(publications_by_year.index.astype(str), publications_by_year.values)
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.xticks(rotation=45)  # Rotate the x-axis labels if needed
    st.pyplot(plt.gcf())
else:
    st.write("No data to display for the selected filters.")
