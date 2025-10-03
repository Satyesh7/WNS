#  1. Import Necessary Libraries
# ==============================================================================
import os
import pandas as pd
import joblib
# ==============================================================================
#  2. Create a Predictor Class
# ==============================================================================

class EnergyLoadPredictor:
    """A class to predict heating and cooling loads using pre-trained models.

    This class loads trained XGBoost models from file and uses them to predict
    energy loads based on user-provided building characteristics.
    """

    def __init__(self, heating_model_path, cooling_model_path):
        """Initializes the predictor by loading the trained models.

        Args:
            heating_model_path (str): The file path for the trained heating load model.
            cooling_model_path (str): The file path for the trained cooling load model.
        """
        self.heating_model = self._load_model(heating_model_path)
        self.cooling_model = self._load_model(cooling_model_path)
        self.feature_names = [
            'Relative Compactness', 'Surface Area', 'Wall Area', 'Roof Area',
            'Overall Height', 'Orientation', 'Glazing Area', 'Glazing Area Distribution'
        ]
        self.feature_prompts = [
            ("Relative Compactness (X1)", "e.g., 0.62 to 0.98"),
            ("Surface Area (X2)", "e.g., 514.5 to 808.5"),
            ("Wall Area (X3)", "e.g., 245.0 to 416.5"),
            ("Roof Area (X4)", "e.g., 110.25 to 220.5"),
            ("Overall Height (X5)", "3.5 or 7.0"),
            ("Orientation (X6)", "2=North, 3=East, 4=South, 5=West"),
            ("Glazing Area (X7)", "0.0, 0.10, 0.25, or 0.40"),
            ("Glazing Area Distribution (X8)", "0 to 5"),
        ]

    def _load_model(self, model_path):
        """Loads a model from a .joblib file.

        Args:
            model_path (str): The path to the model file.

        Returns:
            A trained model object, or None if the file is not found.
        """
        if not os.path.exists(model_path):
            print(f"\n--- FATAL ERROR ---")
            print(f"Error: Model file not found at '{model_path}'.")
            print("Please run 'python main.py' first to train and save the models.")
            return None
        return joblib.load(model_path)

    def _get_user_input(self):
        """Prompts the user to enter the 8 building features with validation.

        Returns:
            list: A list of 8 validated numeric inputs from the user.
        """
        print("\nPlease enter the building's characteristics:")
        user_inputs = []
        for (prompt, example) in self.feature_prompts:
            while True:
                try:
                    value = float(input(f"- {prompt} ({example}): "))
                    user_inputs.append(value)
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")
        return user_inputs

    def make_prediction(self):
        """Orchestrates the user input and prediction process."""
        if self.heating_model is None or self.cooling_model is None:
            return # Stop if models weren't loaded

        # 1. Get input from the user
        input_data = self._get_user_input()

        # 2. Convert input to the format expected by the model
        input_df = pd.DataFrame([input_data], columns=self.feature_names)

        # 3. Make predictions
        predicted_heating_load = self.heating_model.predict(input_df)[0]
        predicted_cooling_load = self.cooling_model.predict(input_df)[0]

        # 4. Display the results
        self._display_predictions(predicted_heating_load, predicted_cooling_load, input_df)

    def _display_predictions(self, heating_load, cooling_load, inputs):
        """Prints the final predictions in a user-friendly format.

        Args:
            heating_load (float): The predicted heating load value.
            cooling_load (float): The predicted cooling load value.
            inputs (pd.DataFrame): The user's input values for reference.
        """
        print("\n" + "="*50)
        print("--- Prediction Results ---")
        print("="*50)
        print("Based on the following inputs:")
        print(inputs.to_string(index=False))
        print("\n" + "-"*50)
        print(f"Predicted Heating Load (Y1): {heating_load:.2f}")
        print(f"Predicted Cooling Load (Y2): {cooling_load:.2f}")
        print("="*50)

# ==============================================================================
#  3. Main Execution Block for Prediction
# ==============================================================================
def main():
    """Main function to run the energy load predictor."""
    print("--- Energy Load Prediction Tool ---")
    print("This tool uses a pre-trained XGBoost model to predict energy loads.")

    # Define the paths to the saved models
    heating_model_file = os.path.join('models', 'xgb_heating_model.joblib')
    cooling_model_file = os.path.join('models', 'xgb_cooling_model.joblib')

    # Create a predictor instance and run it
    predictor = EnergyLoadPredictor(heating_model_file, cooling_model_file)
    predictor.make_prediction()

if __name__ == '__main__':
    main()