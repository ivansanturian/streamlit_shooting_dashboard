import streamlit as st
import pandas as pd

# Import the data 
df = pd.read_excel('fbref_top5leagues_player_shooting_stats.xlsx')
# And ensure connection works (check terminal)
print(df.head())

# Create titles for the streamlit page
st.title('Player Shooting dashboard')
st.markdown("""
**Welcome to my web-app!**  
Open the sidebar by clicking on » icon in the top left of this browser.
\nUse the filters in the sidebar to create a profile of players you'd like to see.
- FBRef data from 2024-2025 season  
- Only includes players from the Top 5 European leagues:
    - Premier League, La Liga, Bundesliga, Ligue 1, Serie A
- This version only supports shot data. 
\nMore extensive data will be built into this tool soon.
\nLast updated: 6/22/2025
""")

# Data changes/cleaning for intuitiveness
# Mapping full position names to their abbreviations
position_map = {
    "Goalkeeper": "GK",
    "Defender": "DF",
    "Midfielder": "MF",
    "Forward": "FW"
}
# Metric dictionary
# Mapping backend stat names to human-readable names
sort_column_map = {
    "90s": "Games Played (90s)",
    "Gls": "Goals",
    "Sh": "Shots",
    "SoT": "Shots on Target",
    "SoT%": "Shot on Target (%)",
    "Sh/90": "Shots per 90",
    "SoT/90": "Shots on Target per 90",
    "G/Sh": "Goals per Shot",
    "G/SoT": "Goals per Shot on Target",
    "Dist": "Average Shot Distance",
    "FK": "Free Kick Goals",
    "PK": "Penalty Goals",
    "PKatt": "Penalty Attempts",
    "xG": "Expected Goals (xG)",
    "npxG": "Non-Penalty xG",
    "npxG/Sh": "npxG per Shot",
    "G-xG": "Goals minus xG",
    "np:G-xG": "Non-Penalty Goals minus xG"
}


# Sidebar work
st.sidebar.header("Necessary Filters")

# Position: drop-down menu
position_options = ['Select...'] + list(position_map.keys())
selected_position = st.sidebar.selectbox("Select Position", position_options)

# Sort column selector
sortable_columns = [
    col for col in df.columns
    if col in sort_column_map and df[col].dtype in ['int64', 'float64']
]
# Build display options for the dropdown
sortable_options = ['Select...'] + [sort_column_map[col] for col in sortable_columns]
# Show dropdown using display names
selected_sort_display = st.sidebar.selectbox("Sort by", sortable_options)
# Convert back to backend column name
sort_by = None if selected_sort_display == 'Select...' else {
    v: k for k, v in sort_column_map.items()
}[selected_sort_display]

# Organize values in descending order
descending = st.sidebar.checkbox("Sort Descending", value=True)

st.sidebar.header("Optional Filters")

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
if selected_position != 'Select...' and sort_by is not None:
    # Get the actual abbreviation from the full name
    position_abbr = position_map.get(selected_position)
    filtered_df = df[
        (df['Age'] >= selected_age[0]) &
        (df['Age'] <= selected_age[1]) &
        (df['Pos'].fillna('').str.contains(position_abbr))
    ]

    # Apply the min_90s filter only if > 0
    if min_90s > 0:
        filtered_df = filtered_df[filtered_df['90s'] >= min_90s]
    # Apply the min_90s filter only if > 0
    if min_shots > 0:
        filtered_df = filtered_df[filtered_df['Sh'] >= min_shots]

    filtered_df = filtered_df.sort_values(by=sort_by, ascending=not descending).reset_index(drop=True)
    # Columns to always show
    base_columns = ['Player', 'Age', 'Born', 'Nation', 'Pos', '90s', 'Sh']

    # Add the sort_by column if it's not already included
    columns_to_display = base_columns + ([sort_by] if sort_by not in base_columns else [])

    # Limit dataframe to these columns only (and avoid errors if any missing)
    filtered_df_display = filtered_df[columns_to_display]

    # Show the table
    st.dataframe(filtered_df_display, use_container_width=True)

else:
    st.info("Please select a Position and a Sort option to view the data.")
