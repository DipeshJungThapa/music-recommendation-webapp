import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from imblearn.over_sampling import SMOTE
from sklearn.decomposition import PCA
import joblib

df = pd.read_csv('./fma_metadata/output/normalized.csv')
target_column = 'track genre_top'


selected_features = [
    col for col in df.columns
    if col.startswith('audio_features') or col.startswith('tfidf_')
]
X = df[selected_features]
y = df[target_column]


print("Original class distribution:")
print(y.value_counts())

class_counts = y.value_counts()
valid_classes = class_counts[class_counts >= 2].index
X_filtered = X[y.isin(valid_classes)]
y_filtered = y[y.isin(valid_classes)]

print("\nFiltered class distribution:")
print(y_filtered.value_counts())


X_train, X_test, y_train, y_test = train_test_split(
    X_filtered, y_filtered, test_size=0.2, random_state=42, stratify=y_filtered
)


smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print("\nClass distribution after SMOTE:")
print(pd.Series(y_train_smote).value_counts())


pca = PCA(n_components=50, random_state=42)
X_train_pca = pca.fit_transform(X_train_smote)
X_test_pca = pca.transform(X_test)

print(f"\nExplained variance by PCA components: {sum(pca.explained_variance_ratio_):.2f}")
print(f"Variance explained by first 5 components: {pca.explained_variance_ratio_[:5]}")


knn = KNeighborsClassifier(
    n_neighbors=5, metric='cosine', algorithm='brute', weights='distance'
)
knn.fit(X_train_pca, y_train_smote)


y_pred = knn.predict(X_test_pca)


accuracy = accuracy_score(y_test, y_pred)
macro_f1 = f1_score(y_test, y_pred, average='macro')

print(f"\nAccuracy: {accuracy * 100:.2f}%")
print(f"Macro F1-Score: {macro_f1:.2f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

joblib.dump(knn, './model/knn.pkl')
joblib.dump(pca, './model/pca.pkl')
