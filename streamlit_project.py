import streamlit as st
import pandas as pd

# Import the data and ensure connection works
df = pd.read_excel('fbref_top5leagues_player_stats.xlsx')
print(df.head())

# Create titles for the streamlit page
st.title ('2024-2025 Player Shooting Scouting Dashboard')
st.subheader('Edit the sidebar filters to find players that fit your profile.')
st.sidebar.header("Necessary Filters")

# Position: drop-down menu
position_options = ['Select...'] + ['GK', 'DF', 'MF', 'FW']
selected_position = st.sidebar.selectbox("Select Position", position_options)

# Sort column selector
sortable_columns = [
    col for col in df.columns
    if df[col].dtype in ['int64', 'float64'] and col not in ['Age', 'Born']
]
sortable_options = ['Select...'] + sortable_columns
sort_by = st.sidebar.selectbox("Sort by", sortable_options)
descending = st.sidebar.checkbox("Sort Descending", value=True)

st.sidebar.subheader("Optional Filters")

# Age: slider
min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
selected_age = st.sidebar.slider("Select Age Range", min_age, max_age, (min_age, max_age))

# 90s: slider
min_90s = st.sidebar.slider(
    "Minimum 90s played",
    min_value=0,
    max_value=int(df['90s'].max()),
    value=0,
    step=1
)

# Shots: slider
min_shots = st.sidebar.slider(
    "Minimum Shots taken",
    min_value=0,
    max_value=int(df['Sh'].max()),
    value=0,
    step=1
)

# Display
if selected_position != 'Select...' and sort_by != 'Select...':
    filtered_df = df[
        (df['Age'] >= selected_age[0]) &
        (df['Age'] <= selected_age[1]) &
        (df['Pos'].fillna('').str.contains(selected_position))
    ]

    # Apply the min_90s filter only if > 0
    if min_90s > 0:
        filtered_df = filtered_df[filtered_df['90s'] >= min_90s]
    # Apply the min_90s filter only if > 0
    if min_shots > 0:
        filtered_df = filtered_df[filtered_df['Sh'] >= min_shots]

    filtered_df = filtered_df.sort_values(by=sort_by, ascending=not descending).reset_index(drop=True)
    # Columns to always show
    base_columns = ['Player', 'Age', 'Nation', 'Pos', '90s', 'Sh']

    # Add the sort_by column if it's not already included
    columns_to_display = base_columns + ([sort_by] if sort_by not in base_columns else [])

    # Limit dataframe to these columns only (and avoid errors if any missing)
    filtered_df_display = filtered_df[columns_to_display]

    # Show the table
    st.dataframe(filtered_df_display, use_container_width=True)

else:
    st.info("Please select a Position and a Sort option to view the data.")
