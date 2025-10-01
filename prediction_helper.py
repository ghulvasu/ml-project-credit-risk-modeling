import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Path to the saved model and its components
MODEL_PATH = 'artifacts/model_data.joblib'

# Load the model and its components
model_data = joblib.load(MODEL_PATH)
model = model_data['model']
scaler = model_data['scaler']
features = model_data['features']
cols_to_scale = model_data['cols_to_scale']


def prepare_input(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                  delinquency_ratio, credit_utilization_ratio, num_open_accounts, residence_type,
                  loan_purpose, loan_type):
    # Create a dictionary of all features the scaler expects
    input_data = {
        # --- These are just examples. You must replace these with the actual 26 column names from your notebook ---
        'age': age, 'income': income, 'loan_amount': loan_amount, 'loan_tenure_months': loan_tenure_months,
        'number_of_open_accounts': num_open_accounts, 'credit_utilization_ratio': credit_utilization_ratio,
        'delinquency_ratio': delinquency_ratio, 'avg_dpd_per_delinquency': avg_dpd_per_delinquency,
        'loan_to_income': loan_amount / income if income > 0 else 0, 'number_of_dependants': 1,
        'years_at_current_address': 1, 'zipcode': 1, 'sanction_amount': 1, 'processing_fee': 1,
        'gst': 1, 'net_disbursement': 1, 'principal_outstanding': 1, 'bank_balance_at_application': 1,
        'number_of_closed_accounts': 1, 'enquiry_count': 1, 'missing_feature_1': 0,
        'missing_feature_2': 0, 'missing_feature_3': 0, 'missing_feature_4': 0,
        'missing_feature_5': 0, 'missing_feature_6': 0
    }

    # Create a DataFrame
    df = pd.DataFrame([input_data])

    # Add one-hot encoded columns after creating the DataFrame
    df['residence_type_Owned'] = 1 if residence_type == 'Owned' else 0
    df['residence_type_Rented'] = 1 if residence_type == 'Rented' else 0
    df['loan_purpose_Education'] = 1 if loan_purpose == 'Education' else 0
    df['loan_purpose_Home'] = 1 if loan_purpose == 'Home' else 0
    df['loan_purpose_Personal'] = 1 if loan_purpose == 'Personal' else 0
    df['loan_type_Unsecured'] = 1 if loan_type == 'Unsecured' else 0

    # Scale the numerical columns
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # Select only the final features the model needs for prediction
    df_final = df[features]

    return df_final


def predict(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type):
    input_df = prepare_input(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                             delinquency_ratio, credit_utilization_ratio, num_open_accounts, residence_type,
                             loan_purpose, loan_type)

    probability, credit_score, rating = calculate_credit_score(input_df)

    return probability, credit_score, rating


def calculate_credit_score(input_df, base_score=300, scale_length=600):
    # --- ERROR FIX STARTS HERE ---
    # This block now correctly handles both Linear Models and Tree-based Models (like RandomForest)
    try:
        # This works for models like Logistic Regression
        x = np.dot(input_df.values, model.coef_.T) + model.intercept_
        default_probability = 1 / (1 + np.exp(-x))
    except AttributeError:
        # This will run for models like RandomForest that don't have .coef_
        # We get the probability of the positive class (class 1, i.e., "default")
        default_probability = model.predict_proba(input_df)[:, 1]
    # --- ERROR FIX ENDS HERE ---

    non_default_probability = 1 - default_probability

    # Convert the probability to a credit score, scaled to fit within 300 to 900
    credit_score = base_score + non_default_probability.flatten() * scale_length

    def get_rating(score):
        if 300 <= score < 500:
            return 'Poor'
        elif 500 <= score < 650:
            return 'Average'
        elif 650 <= score < 750:
            return 'Good'
        elif 750 <= score <= 900:
            return 'Excellent'
        else:
            return 'Undefined'

    rating = get_rating(credit_score[0])

    return default_probability.flatten()[0], int(credit_score[0]), rating

