# Energy Load Prediction Model Evaluation

This project evaluates and compares three different machine learning models for predicting the heating load (Y1) and cooling load (Y2) of buildings based on their physical characteristics.

The models evaluated are:
1.  Linear Regression (Baseline)
2.  Random Forest Regressor
3.  XGBoost Regressor

The script will output a detailed performance comparison for each model, including metrics like Mean Squared Error (MSE), R-squared, Adjusted R-squared, and a side-by-side view of actual vs. predicted values.

# Energy Load Prediction Model Evaluation and Prediction

This project contains two main scripts:
1.  **`main.py`**: Trains and evaluates three machine learning models (Linear Regression, Random Forest, XGBoost) to find the best one for predicting building energy loads. It saves the best-performing models (XGBoost) to files.
2.  **`predict.py`**: A user-friendly tool that loads the pre-trained XGBoost models and predicts the Heating Load (Y1) and Cooling Load (Y2) based on 8 input features provided by the user.

## Project Structure

```
.
├── main.py                     # The main Python script to run the evaluation
├── requirements.txt            # A list of all necessary Python libraries
├── README.md                   # This instruction file
└── energy-efficiency-dataset.csv # The dataset file
```

## Setup and Installation

Follow these steps to set up a virtual environment and run the project. This ensures that the project's dependencies do not interfere with other Python projects on your system.

### Step 1: Create a Virtual Environment

Open your terminal or command prompt, navigate to the `energy_efficiency` project folder, and run the following command to create a virtual environment named `venv`:

```bash
python -m venv venv
```
*(Note: If you are on an older Python installation, you may need to use `python3` instead of `python`)*

### Step 2: Activate the Virtual Environment

-   **On Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
-   **On macOS and Linux:**
    ```bash
    source venv/bin/activate
    ```
After activation, you will see `(venv)` at the beginning of your command prompt, indicating that the virtual environment is active.

### Step 3: Install the Required Libraries

With the virtual environment active, install all the necessary libraries from the `requirements.txt` file using pip:

```bash
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

This command will automatically download and install pandas, scikit-learn, and xgboost.

### How to Use This Project (Two-Step Process)
Step 1: Train the Models
You must first run the training script. This will evaluate all models and, most importantly, create the xgb_heating_model.joblib and xgb_cooling_model.joblib files inside the models folder.

In your activated terminal, run:
python main.py

Step 2: Make a Prediction
Once the models are saved, you can use the prediction script. This script will prompt you to enter the 8 characteristics of a building.
In your activated terminal, run:
python predict.py
```
Follow the on-screen prompts to enter the feature values, and the script will output the predicted Heating and Cooling Loads.```

## Deactivating the Virtual Environment

When you are finished, you can deactivate the virtual environment by simply running:

```bash
deactivate
```