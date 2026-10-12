import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Muzaffar Developers Portal",
    page_icon="💻",
    layout="centered"
)

# Sidebar Navigation
st.sidebar.title("Muzaffar Developers")
st.sidebar.write("Professional Python & Automation Solutions")
menu = st.sidebar.radio("Navigation", ["Home", "Services", "Project Estimator"])

if menu == "Home":
    st.title("WELCOM TO MUZAFFAR DEVELOPER PAGE")
    st.write("We build custom Python desktop applications, automation scripts, and database-driven solutions.")
    st.info("This application is written in Python and deployed live via Streamlit!")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Completed Projects", "25+", "+3 this month")
    col2.metric("Core Tech", "Python & SQLite", "Expert")
    col3.metric("Support", "24/7", "Available")

elif menu == "Services":
    st.title("Our Core Services")
    st.markdown("""
    * **Python Desktop Apps:** Custom Tkinter GUI solutions with SQLite integration.
    * **Data Automation:** Excel macros, PDF parsers, and OCR text extraction pipelines.
    * **Web Backends:** FastAPI and Flask API developments.
    """)

elif menu == "Project Estimator":
    st.title("Quick Project Estimator")
    st.write("Estimate your software development scope:")
    
    project_type = st.selectbox("Select Project Type", ["Desktop Automation (Python)", "Web Dashboard (Flask/FastAPI)", "Data Scraping / PDF Processing"])
    hours = st.slider("Estimated Complexity (Hours)", 5, 100, 20)
    
    rate_per_hour = 15 # Base rate
    total_cost = hours * rate_per_hour
    
    if st.button("Calculate Estimate"):
        st.success(f"Estimated Cost for {project_type}: **${total_cost} USD** (approx. {hours} hours)")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>© 2026 Muzaffar Developers. Built with Python & Streamlit.</p>", unsafe_allow_html=True)
