import streamlit as st
import pandas as pd
import plotly.express as px
import base64 

st.set_page_config(layout="wide") 

# --- FUNCTION TO SET BACKGROUND IMAGE ---
def set_background(image_file="guinea pig pic.webp"):
    try:
        with open(image_file, "rb") as f:
            img_bytes = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/webp;base64,{img_bytes}"); 
                background-size: cover; 
                background-attachment: fixed; 
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Background image file not found. Running without background image.")

# --- CALL THE FUNCTION TO SET THE BACKGROUND ---
set_background() 

st.title("Guinea Pig Dashboard 🐹")

# --- CREATE TABS ---
tab1, tab2 = st.tabs(["📊 Breed Analysis", "🍎 Diet Analysis"])

# --- TAB 1: BREED ANALYSIS ---
with tab1:
    st.header("Guinea Pig Breed Data")
    try:
        df_breeds = pd.read_csv("guinea_pig_breeds.csv", sep=",") 
    except FileNotFoundError:
        st.error("Error: The breeds data file was not found.")
        st.stop() 

    # Sidebar Filter for Tab 1
    st.sidebar.header("Filter Breeds")
    all_grooming = ['All'] + list(df_breeds['Grooming Needs'].unique())
    selected_grooming = st.sidebar.selectbox("Select Grooming Needs Level", all_grooming)

    if selected_grooming == 'All':
        filtered_df_breeds = df_breeds
    else:
        filtered_df_breeds = df_breeds[df_breeds['Grooming Needs'] == selected_grooming]

    st.subheader(f"Available Breeds with '{selected_grooming}' Grooming Needs")
    st.dataframe(filtered_df_breeds) 

    # Visualizations
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Average Weight Distribution by Breed (grams)")
        fig_weight = px.bar(filtered_df_breeds, x='Breed', y='Average Weight (g)', color='Coat Type')
        st.plotly_chart(fig_weight, use_container_width=True)

    with col2:
        st.subheader("Breeds by Origin Country")
        origin_counts = df_breeds['Origin'].value_counts()
        fig_origin = px.pie(origin_counts, values='count', names=origin_counts.index, title='Origin Country Distribution')
        st.plotly_chart(fig_origin, use_container_width=True)

# --- TAB 2: DIET ANALYSIS ---
with tab2:
    st.header("Guinea Pig Diet & Nutrition Data")
    try:
        df_diet = pd.read_csv("guinea_pig_diet.csv", sep=",")
    except FileNotFoundError:
        st.error("Error: The diet data file was not found.")
        st.stop()

    st.subheader("Nutritional Breakdown of Common Foods")
    st.dataframe(df_diet)

    st.subheader("Calcium vs. Phosphorus in Diet (Ca:P Ratio)")
    st.write("A healthy ratio for guinea pigs is generally 1.5:1 to 2:1. Higher values mean high calcium.")
    
    # Create a scatter plot for Calcium and Phosphorus
    fig_diet = px.scatter(df_diet, x="Calcium (mg)", y="Phosphorus (mg)", text="Food Item", 
                          color="Category", size="Serving Size (g)",
                          hover_name="Food Item", title="Calcium vs Phosphorus Content")
    fig_diet.update_traces(textposition='top center')
    st.plotly_chart(fig_diet, use_container_width=True)

