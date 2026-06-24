import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

# =====================================
# EXTRACT
# =====================================

df = pd.read_csv(
    "health_dataset_1000_rows.csv"
)

print("\n==============================")
print("ORIGINAL DATASET")
print("==============================")

print("Shape :", df.shape)

# =====================================
# NULL VALUE REPORT
# =====================================

print("\nNULL VALUES")

print(df.isnull().sum())

# =====================================
# DUPLICATE REPORT
# =====================================

print("\nDUPLICATE ROWS")

print(df.duplicated().sum())

# =====================================
# TRANSFORM
# =====================================

print("\nRemoving Duplicates...")

df.drop_duplicates(
    inplace=True
)

print(
    "Shape After Removing Duplicates:",
    df.shape
)

# Fill Missing Values

df["glucose"] = df["glucose"].fillna(
    df["glucose"].median()
)

df["haemoglobin"] = df["haemoglobin"].fillna(
    df["haemoglobin"].median()
)

df["cholesterol"] = df["cholesterol"].fillna(
    df["cholesterol"].median()
)

df["email"] = df["email"].fillna(
    "unknown@gmail.com"
)

print("\nNULL VALUES AFTER CLEANING")

print(df.isnull().sum())

# =====================================
# FEATURE SELECTION
# =====================================

X = df[
    [
        "glucose",
        "haemoglobin",
        "cholesterol"
    ]
]

y = df["remarks"]

# =====================================
# LABEL ENCODING
# =====================================

encoder = LabelEncoder()

y_encoded = encoder.fit_transform(y)

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)

# =====================================
# MODELS
# =====================================

models = {

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        max_depth=8,
        min_samples_split=10,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=42
    ),

    "Logistic Regression": LogisticRegression(
        max_iter=2000
    ),

    "KNN": KNeighborsClassifier(
        n_neighbors=7,
        weights="distance"
    ),

    "SVM": SVC(
        kernel="rbf",
        probability=True
    ),

    "Naive Bayes": GaussianNB()
}

# =====================================
# TRAINING
# =====================================

best_model = None
best_precision = 0

print("\n==============================")
print("MODEL COMPARISON")
print("==============================")

for name, model in models.items():

    model.fit(
        X_train,
        y_train
    )

    y_pred = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    print("\n" + "=" * 50)

    print(name)

    print("=" * 50)

    print(
        f"Accuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1 Score : {f1:.4f}"
    )

    print("\nClassification Report\n")

    print(
        classification_report(
            y_test,
            y_pred,
            target_names=encoder.classes_,
            zero_division=0
        )
    )

    if precision > best_precision:

        best_precision = precision

        best_model = model

# =====================================
# SAVE BEST MODEL
# =====================================

joblib.dump(
    best_model,
    "health_model.pkl"
)

joblib.dump(
    encoder,
    "label_encoder.pkl"
)

print("\n==============================")
print("BEST MODEL SAVED")
print("==============================")

print(
    f"Best Precision: {best_precision:.4f}"
)