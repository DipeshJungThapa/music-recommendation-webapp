import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

df = pd.read_csv('./fma_metadata/output/normalized.csv')
#print(df.columns)
target_column = 'track genre_top'

selected_features = [
    col for col in df.columns
    if col.startswith('audio_features') or col.startswith('tfidf_')
]
X = df[selected_features]
y = df[target_column]

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train,y_train)

y_pred = knn.predict(X_test)

accuracy = accuracy_score(y_test,y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

print("\nClassification Report:")
print(classification_report(y_test, y_pred))
