# ml-project-credit-risk-modeling

Dwarkesh Finance: Credit Risk Prediction
A deployed, end-to-end machine learning application that predicts the probability of a loan default based on applicant details and credit history. This project transforms a trained Random Forest model into an interactive web application using Streamlit, allowing for real-time risk assessment.

**

📋 Project Overview
This project addresses the critical business need for accurate credit risk assessment. By leveraging historical customer and loan data, a machine learning model was trained to predict the likelihood of a customer defaulting on a loan. This model is served through a user-friendly web interface where a loan officer can input an applicant's information and receive an instant credit score, default probability, and a clear risk rating.

Key Features:
Interactive UI: A clean and professional interface built with Streamlit for easy data entry.

Real-Time Prediction: Uses a trained Random Forest Classifier to provide immediate risk scores.

Dynamic Results Visualization: Displays the credit score on an interactive gauge chart and provides a color-coded risk rating (Excellent, Good, Average, Poor).

End-to-End Workflow: Covers the entire machine learning lifecycle from data preprocessing and model training in a Jupyter Notebook to deployment as a web app.

🛠️ Technology Stack
Backend & Model: Python, Scikit-Learn, Pandas, NumPy

Web Framework: Streamlit

Data Visualization: Plotly, Matplotlib, Seaborn

Deployment: Streamlit Community Cloud (or any other cloud platform)

Code Versioning: Git & GitHub

🚀 How to Run Locally
Follow these steps to set up and run the project on your local machine.

1. Clone the Repository
Open your terminal and clone this repository using Git:

git clone https://github.com/ghulvasu/ml-project-credit-risk-modeling.git
cd your-repo-name

(Replace YourUsername/your-repo-name with your actual GitHub repository URL.)

2. Create a Virtual Environment (Recommended)
It's a best practice to create a virtual environment to keep project dependencies isolated.

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Required Libraries
The requirements.txt file contains all the necessary Python packages. Install them with a single pip command:

pip install -r requirements.txt

4. Run the Streamlit Application
Once the dependencies are installed, you can launch the application:

streamlit run main.py

