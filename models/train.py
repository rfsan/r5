# db connection
import psycopg2
import pandas.io.sql as sqlio

# ml
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

# utils
import os
import joblib
import gzip
import warnings
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings('ignore')


if __name__ == "__main__":
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    # DATABASE CONNECTION
    print('Connecting to the database...')
    connection = psycopg2.connect(
        host="db.kowllitbpmdnyshbtbzn.supabase.co",
        database="postgres",
        port="5432",
        user="postgres",
        password=DB_PASSWORD,
    )
    cursor = connection.cursor()
    print('Connected to the database!')

    # FETCHING DATA
    print('Fetching the fraud data from the database')
    sql = """
        SELECT *
        FROM public.fraudes
    """
    df = sqlio.read_sql_query(sql, connection)
    print('First 5 rows of the data')
    print(df.head(5))

    # MODEL TRAINING
    target = 'FraudFound_P'
    cat_nominal_features = [
        # 'Monthh',
        # 'DayOfWeek',
        # 'Make',
        'AccidentArea',
        # 'DayOfWeekClaimed',
        # 'MonthClaimed',
        'Sex',
        # 'MaritalStatus',
        # 'Fault',
        # 'PolicyType',
        'VehicleCategory',
        # 'PoliceReportFiled',
        # 'WitnessPresent',
        # 'AgentType',
        'BasePolicy'
    ]
    num_discrete_features = [
        # 'WeekOfMonth',
        # 'WeekOfMonthClaimed',
        # "RepNumber",
        # "Deductible",
        # 'DriverRating',
        'Yearr'
    ]
    cat_ordinal_features = [
        'AgeOfPolicyHolder',
        # 'VehiclePrice',
        # 'Days_Policy_Accident',
        # 'Days_Policy_Claim',
        # 'PastNumberOfClaims',
        # 'AgeOfVehicle',
        # 'NumberOfSuppliments',
        # 'AddressChange_Claim', 
        # 'NumberOfCars'
    ]

    features = cat_nominal_features + num_discrete_features + cat_ordinal_features
    print("Features to be used to train the model", features)
    X = df[features].copy()
    y = df[target].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, 
        y, 
        stratify=y, 
        random_state=42, 
        test_size=0.2
    )

    cat_nominal_pipe = Pipeline([
        ('impute', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(drop='first', handle_unknown="ignore")),
    ])

    num_discrete_pipe = Pipeline([
        ('impute', SimpleImputer(strategy='most_frequent')),
        ("scaler", MinMaxScaler())
    ])

    cat_ordinal_pipe = Pipeline([
        ('encoder', OrdinalEncoder(categories=[
            ['16 to 17', '18 to 20', '21 to 25', '26 to 30', '31 to 35', '36 to 40', '41 to 50', '51 to 65',  'over 65'],
            # ['less than 20000', '20000 to 29000', '30000 to 39000',  '40000 to 59000', '60000 to 69000', 'more than 69000'],
            # ['none', '1 to 7', '8 to 15', '15 to 30', 'more than 30'],
            # ['8 to 15', '15 to 30', 'more than 30'],
            # ['none', '1', '2 to 4', 'more than 4'],
            # ['new', '2 years', '3 years',  '4 years', '5 years', '6 years', '7 years', 'more than 7'],
            # ['none', '1 to 2', '3 to 5', 'more than 5'],
            # ['under 6 months', '1 year', '2 to 3 years', '4 to 8 years', 'no change'],
            # ['1 vehicle', '2 vehicles', '3 to 4', '5 to 8', 'more than 8'],
        ])),
        ("scaler", MinMaxScaler())
    ])

    full_processor = ColumnTransformer(transformers=[
        ('cat_nominal', cat_nominal_pipe, cat_nominal_features),
        ('num_discrete', num_discrete_pipe, num_discrete_features),
        ('cat_ordinal_pipe', cat_ordinal_pipe, cat_ordinal_features)
    ])

    ensemble = VotingClassifier([
        # ('logistic', LogisticRegression()),
        # ('dt', DecisionTreeClassifier()),
        # ('svm', SVC(probability=True)),
        ('rf', RandomForestClassifier(max_depth=2, class_weight='balanced'))
        ],
        voting='soft'
    )

    pipe = Pipeline([
        ('preprocess', full_processor),
        ('ensemble', ensemble) 
    ])

    print('Training the model')

    pipe.fit(X_train, y_train)

    print('Model trained')

    print('Classification Report')
    print(classification_report(y_test, pipe.predict(X_test)))

    # EXPORT THE MODEL
    print('Exporting the model')
    joblib.dump(pipe, gzip.open('./models/model_binary.dat.gz', "wb"))