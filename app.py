import streamlit as st
import pandas as pd

# Set page title
st.set_page_config(page_title="Placements Analysis App", layout="wide")

# Title
st.title("Placements Analysis")

# Read CSV file
df = pd.read_csv("combined.csv")

# Create columns for filters
col1, col2 = st.columns(2)

with col1:
    # 1. Year selection (multi-select)
    years = sorted(df['Year'].unique())
    selected_years = st.multiselect("Select Years", years, default=[2023])


with col2:
    # 3. Company selection (multi-select)
    companies = sorted(df['Name'].unique())
    selected_companies = st.multiselect("Select Companies", ["All"] + companies, default=["All"])
col1 = st.columns(1)[0]

with col1:
    # 2. Package range
    min_package = st.number_input("Minimum Package (LPA)", min_value=float(df['CTC_LPA'].min()), value=float(7), step=0.1)
    max_package = st.number_input("Maximum Package (LPA)", min_value=float(df['CTC_LPA'].min()), value=float(df['CTC_LPA'].max()), step=0.1)

# Submit button
submit_button = st.button("Apply Filters")

if submit_button:
    # Filter the dataset
    if "All" in selected_companies:
        company_filter = df['Name'].isin(companies)
    else:
        company_filter = df['Name'].isin(selected_companies)

    filtered_df = df[
        (df['Year'].isin(selected_years)) &
        (df['CTC_LPA'] >= min_package) &
        (df['CTC_LPA'] <= max_package) & 
        company_filter
    ]
    sum_row = filtered_df[['CSE', 'CSM', 'ECE', 'EEE', 'IT', 'MECH', 'CIVIL']].sum()
    
    # Create a new row with the sums
    sum_row_df = pd.DataFrame([sum_row], columns=['CSE', 'CSM', 'ECE', 'EEE', 'IT', 'MECH', 'CIVIL'])
    sum_row_df['S.No.'] = 'Total'
    sum_row_df['Year'] = ''
    sum_row_df['Name'] = 'Sum of All Companies'
    sum_row_df['CTC'] = 'Avg CTC for CS (Approx):'
    sum_row_df['CTC_LPA'] = (filtered_df['CTC_LPA'] *( filtered_df['CSE']+filtered_df['CSM'])).sum() / 180
    sum_row_df['Total'] = sum_row.sum()
    sum_row_df=sum_row_df[[ 'S.No.', 'Year', 'Name', 'CTC', 'CTC_LPA',  'CSE', 'CSM', 'IT','ECE', 'EEE', 'MECH', 'CIVIL',"Total"]]
    # Concatenate the sum row to the filtered dataframe
    filtered_df = pd.concat([sum_row_df,filtered_df], ignore_index=True)


    st.subheader("Filtered Data")
    st.write(filtered_df)

    # # Display summary statistics
    # st.subheader("Summary Statistics")
    # st.write(f"Total Records: {len(filtered_df)}")
    # st.write(f"Average CTC: {filtered_df['CTC_LPA'].mean():.2f} LPA")
    # st.write(f"Total Placements: {filtered_df['Total'].sum()}")
else:
    st.write("Please apply filters to see the results.")
