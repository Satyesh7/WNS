# ==============================================================================
#  1. Import Necessary Libraries
# ==============================================================================
import warnings
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib # Import joblib for saving models

# Import the models we will test
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

# Suppress potential warnings for a cleaner output
warnings.filterwarnings('ignore')

# ==============================================================================
#  2. Create a Reusable Class for Model Evaluation
# ==============================================================================
class ModelEvaluator:
    """A class to streamline training and evaluation of regression models."""

    def __init__(self, model_class, model_name, file_path, **model_params):
        """Initializes the ModelEvaluator."""
        self.model_class = model_class
        self.model_name = model_name
        self.model_params = model_params
        self.file_path = file_path
        self.df = None
        self.X_train, self.X_test, self.y1_train, self.y1_test, self.y2_train, self.y2_test = [None] * 6
        self._load_and_prepare_data()

    def _load_and_prepare_data(self):
        """Loads, cleans, renames columns, and prepares the dataset."""
        if not os.path.exists(self.file_path):
            print(f"Error: The file '{self.file_path}' was not found.")
            return
        self.df = pd.read_csv(self.file_path)
        self.df.dropna(inplace=True)
        self.df.rename(columns={
            'X1': 'Relative Compactness', 'X2': 'Surface Area', 'X3': 'Wall Area',
            'X4': 'Roof Area', 'X5': 'Overall Height', 'X6': 'Orientation',
            'X7': 'Glazing Area', 'X8': 'Glazing Area Distribution',
            'Y1': 'Heating Load', 'Y2': 'Cooling Load'
        }, inplace=True)

    def _calculate_adjusted_r2(self, r2, n_samples, n_features):
        """Calculates the Adjusted R-squared score."""
        denominator = (n_samples - n_features - 1)
        if denominator == 0:
            return r2
        return 1 - (1 - r2) * (n_samples - 1) / denominator

    def run_full_evaluation(self):
        """Executes the full evaluation pipeline."""
        if self.df is None:
            return
        print("\n" + "="*60)
        print(f"--- EVALUATING MODEL: {self.model_name} ---")
        print("="*60)
        features = [
            'Relative Compactness', 'Surface Area', 'Wall Area', 'Roof Area',
            'Overall Height', 'Orientation', 'Glazing Area', 'Glazing Area Distribution'
        ]
        X = self.df[features]
        y1 = self.df['Heating Load']
        y2 = self.df['Cooling Load']
        self.X_train, self.X_test, self.y1_train, self.y1_test = train_test_split(X, y1, test_size=0.2, random_state=42)
        _, _, self.y2_train, self.y2_test = train_test_split(X, y2, test_size=0.2, random_state=42)
        self._evaluate_target('Heating Load', self.y1_train, self.y1_test)
        print("\n" + "-"*40 + "\n")
        self._evaluate_target('Cooling Load', self.y2_train, self.y2_test)

    def _evaluate_target(self, target_name, y_train, y_test):
        """Trains, predicts, evaluates, and saves the best model for a target."""
        print(f"--- Training and Evaluating for {target_name} ---")
        model = self.model_class(**self.model_params)
        model.fit(self.X_train, y_train)
        y_pred = model.predict(self.X_test)
        self._print_evaluation_results(y_test, y_pred, target_name)

        # --- ADDED LOGIC: Save the trained XGBoost models ---
        if self.model_name == "XGBoost Regressor":
            model_folder = 'models'
            os.makedirs(model_folder, exist_ok=True) # Create the 'models' directory if it doesn't exist
            if target_name == 'Heating Load':
                filename = os.path.join(model_folder, 'xgb_heating_model.joblib')
            else:
                filename = os.path.join(model_folder, 'xgb_cooling_model.joblib')
            joblib.dump(model, filename)
            print(f"\nModel for {target_name} saved to '{filename}'")

    def _print_evaluation_results(self, y_true, y_pred, target_name):
        """Calculates and prints performance metrics and prediction comparisons."""
        # ... (This function remains unchanged) ...
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        adj_r2 = self._calculate_adjusted_r2(r2, self.X_test.shape[0], self.X_test.shape[1])
        print(f"\nPerformance Metrics for {target_name}:")
        print(f"  Mean Squared Error (MSE):       {mse:.4f}")
        print(f"  Root Mean Squared Error (RMSE): {rmse:.4f}")
        print(f"  Mean Absolute Error (MAE):      {mae:.4f}")
        print(f"  R-squared (R²):                 {r2:.4f}")
        print(f"  Adjusted R-squared:             {adj_r2:.4f}")
        results_df = pd.DataFrame({f'Actual {target_name}': y_true, f'Predicted {target_name}': y_pred})
        print(f"\nComparison of Actual vs. Predicted values (First 15 samples):")
        print(results_df.head(15).to_string(index=False))

# ==============================================================================
#  3. Main Execution Block
# ==============================================================================
def main():
    """Main function to execute the model evaluation and saving script."""
    print("Script execution started: Training and evaluating all models.")
    dataset_file_path = 'energy-efficiency-dataset.csv'
    models_to_test = {
        "Linear Regression": (LinearRegression, {}),
        "Random Forest Regressor": (RandomForestRegressor, {'n_estimators': 100, 'random_state': 42}),
        "XGBoost Regressor": (xgb.XGBRegressor, {'n_estimators': 100, 'learning_rate': 0.1, 'random_state': 42})
    }
    for model_name, (model_class, params) in models_to_test.items():
        evaluator = ModelEvaluator(
            model_class=model_class,
            model_name=model_name,
            file_path=dataset_file_path,
            **params
        )
        evaluator.run_full_evaluation()
    print("\nScript execution finished.")

if __name__ == '__main__':
    main()