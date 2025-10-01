import streamlit as st
import plotly.graph_objects as go
from prediction_helper import predict

# --- Page Configuration ---
st.set_page_config(
    page_title="Dwarkesh Finance: Credit Risk Analysis",
    page_icon="🏦",
    layout="wide"
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    /* General Styles */
    .stApp {
        background-color: #f0f2f6;
    }
    .main-title {
        color: #1E3A8A; /* Dark Blue */
        text-align: center;
        font-weight: bold;
        padding-top: 20px;
        font-size: 2.75rem; /* Increased font size */
    }
    .sub-header {
        text-align: center;
        color: #4B5563; /* Gray */
        margin-bottom: 30px;
        font-size: 1.2rem; /* Increased font size */
    }

    /* Input Cards */
    .card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        height: 100%; /* Make cards in a row have the same height */
    }
    .card-title {
        font-size: 1.5rem; /* Increased font size */
        font-weight: bold;
        color: #374151; /* Dark Gray */
        margin-bottom: 20px;
    }

    /* Increase font size for widget labels */
    .st-emotion-cache-1q8dd3e {
        font-size: 1.1rem;
    }

    /* Main Button */
    div.stButton > button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 10px;
        height: 3.5em;
        width: 100%;
        font-size: 1.1rem;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #2563EB; /* Lighter Blue */
        color: white;
    }

    /* Results Display */
    .result-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%; /* Make result cards in a row have the same height */
    }
    .rating-box {
        padding: 12px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        font-size: 1.75rem;
        margin-top: 15px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .rating-Excellent { background: linear-gradient(45deg, #10B981, #34D399); } /* Green */
    .rating-Good { background: linear-gradient(45deg, #3B82F6, #60A5FA); }      /* Blue */
    .rating-Average { background: linear-gradient(45deg, #F59E0B, #FBBF24); }   /* Amber */
    .rating-Poor { background: linear-gradient(45deg, #EF4444, #F87171); }       /* Red */

</style>
""", unsafe_allow_html=True)

# --- Main Page ---
st.markdown('<h1 class="main-title">Dwarkesh Finance Credit Risk Analysis</h1>', unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Enter applicant details to assess credit risk and get a score.</p>",
            unsafe_allow_html=True)

# Using st.form to group inputs and have a single submission button
with st.form(key='credit_risk_form'):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">Applicant & Loan Details</p>', unsafe_allow_html=True)
        age = st.slider('Age', min_value=18, max_value=100, value=28, key='age_slider')
        income = st.number_input('Annual Income (in ₹)', min_value=0, value=1200000, step=10000, key='income_input')
        loan_amount = st.number_input('Loan Amount (in ₹)', min_value=0, value=2560000, step=10000,
                                      key='loan_amount_input')
        loan_tenure_months = st.slider('Loan Tenure (months)', min_value=6, max_value=120, value=36,
                                       key='tenure_slider')
        residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])
        loan_purpose = st.selectbox('Loan Purpose', ['Personal', 'Home', 'Education', 'Auto'])
        loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="card-title">Credit History</p>', unsafe_allow_html=True)
        num_open_accounts = st.slider('Number of Open Loan Accounts', min_value=0, max_value=10, value=2,
                                      key='open_accounts_slider')
        delinquency_ratio = st.slider('Delinquency Ratio (%)', min_value=0, max_value=100, value=30,
                                      key='delinquency_slider')
        credit_utilization_ratio = st.slider('Credit Utilization Ratio (%)', min_value=0, max_value=100, value=30,
                                             key='utilization_slider')
        avg_dpd_per_delinquency = st.number_input('Average Days Past Due', min_value=0, value=20, key='dpd_input')
        st.markdown('</div>', unsafe_allow_html=True)

    # Submit button for the form
    submit_button = st.form_submit_button(label='Calculate Risk Score')

# --- Results Display ---
if submit_button:
    with st.spinner('Analyzing risk profile...'):
        probability, credit_score, rating = predict(
            age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type
        )

    st.write("")  # Add a little space before showing the result

    col_res1, col_res2 = st.columns([2, 1.5])  # Give more space to the gauge

    with col_res1:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        # Create the gauge chart
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=credit_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Credit Score", 'font': {'size': 24, 'color': '#1E3A8A'}},
            gauge={
                'axis': {'range': [300, 900], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#1E3A8A"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [300, 500], 'color': '#F87171'},  # Red
                    {'range': [500, 650], 'color': '#FBBF24'},  # Amber
                    {'range': [650, 750], 'color': '#60A5FA'},  # Blue
                    {'range': [750, 900], 'color': '#34D399'}  # Green
                ],
            }))
        gauge_fig.update_layout(height=300, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(gauge_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_res2:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #1E3A8A; font-weight: bold;'>Risk Assessment</h3>", unsafe_allow_html=True)
        # Display the colored rating box and default probability
        st.markdown(f'<div class="rating-box rating-{rating}">Rating: {rating}</div>', unsafe_allow_html=True)
        st.markdown(f"<p style='margin-top: 30px; font-size: 1.2rem; color: #4B5563;'>Default Probability</p>",
                    unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 2.5rem; color: #1E3A8A; font-weight: bold;'>{probability:.2%}</p>",
                    unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<hr style='border: 1px solid #E5E7EB; margin-top: 50px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9CA3AF;'>© Dwarkesh Finance | Machine Learning Project</p>",
            unsafe_allow_html=True)

