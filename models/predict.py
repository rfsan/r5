import pandas as pd

# Utils
import joblib

model = joblib.load('./models/model_binary.dat.gz')

def get_proba(X):
    """
        X: DataFrame
    """
    return model.predict_proba(X)[:,1].round(2).tolist()


if __name__ == "__main__":
    example = [
        {
        "AccidentArea": "Rural",
        "Sex": "Male",
        "VehicleCategory": "Sport",
        "BasePolicy": "Liability",
        "Yearr": 1996,
        "AgeOfPolicyHolder": "51 to 65"
        },
        {
        "AccidentArea": "Urban",
        "Sex": "Female",
        "VehicleCategory": "Utility",
        "BasePolicy": "Collision",
        "Yearr": 1994,
        "AgeOfPolicyHolder": "16 to 17"
        }
    ]
    X = pd.DataFrame(example)
    print(get_proba(X))
