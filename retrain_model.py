import os
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import StackingClassifier

os.makedirs("models", exist_ok=True)

print("Loading dataset...")
df = pd.read_csv("data/dataset.csv")

# Fill missing/NaN values with 0
df = df.fillna(0)

# Check if target label (Disease/prognosis) is the first or last column
# If target is text/string in column 0 or named 'Disease'/'prognosis'
if 'Disease' in df.columns:
    y = df['Disease'].values
    X_df = df.drop(columns=['Disease'])
elif 'prognosis' in df.columns:
    y = df['prognosis'].values
    X_df = df.drop(columns=['prognosis'])
else:
    # First column is target label, rest are binary feature columns
    y = df.iloc[:, 0].values
    X_df = df.iloc[:, 1:]

# Convert feature dataframe explicitly to numeric float array
X = X_df.apply(pd.to_numeric, errors='coerce').fillna(0).values

print(f"Features matrix X shape: {X.shape}, Target array y shape: {y.shape}")

print("Configuring Stacking Ensemble Model...")
level0 = [
    ('lr', LogisticRegression(solver='liblinear', C=0.03)),
    ('knn', KNeighborsClassifier(n_neighbors=6, metric='cosine')),
    ('dctree', DecisionTreeClassifier(splitter='random', max_depth=34)),
    ('svm', SVC(C=0.1)),
]

model = StackingClassifier(estimators=level0, final_estimator=LogisticRegression())

print("Training Stacking Classifier (takes ~10-30 seconds)...")
model.fit(X, y.ravel())

output_pickle = "models/fitted_model.pickle2"
with open(output_pickle, "wb") as f:
    pickle.dump(model, f)

print(f"Successfully retrained and saved model to {output_pickle}!")
