import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from imblearn.over_sampling import SMOTE
from sklearn.decomposition import PCA
import joblib
import os
from dotenv import load_dotenv

def load_data(path):
    return pd.read_csv(path)

def select_features(df, target_column):
    selected_features = [
        col for col in df.columns
        if col.startswith('chroma_cens mean') or col.startswith('mfcc mean') or
           col.startswith('tonnetz mean') or col.startswith('spectral_contrast mean') or
           col.startswith('spectral_centroid mean') or col.startswith('spectral_rolloff mean') or
           col.startswith('tfidf_')  
    ]
    selected_features.append('audio_features tempo')

    X = df[selected_features]
    y = df[target_column]
    return X, y

def filter_classes(X, y, min_samples_required=6):
    class_counts = y.value_counts()
    valid_classes = class_counts[class_counts >= min_samples_required].index
    X_filtered = X[y.isin(valid_classes)]
    y_filtered = y[y.isin(valid_classes)]
    return X_filtered, y_filtered

def split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

def apply_smote(X_train, y_train, k_neighbors=5):
    smote = SMOTE(k_neighbors=k_neighbors, random_state=42)
    return smote.fit_resample(X_train, y_train)

def apply_pca(X_train, X_test, n_components=50):
    pca = PCA(n_components=n_components, random_state=42)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)
    return X_train_pca, X_test_pca, pca

def train_knn(X_train, y_train):
    knn = KNeighborsClassifier(n_neighbors=5, metric='cosine', algorithm='brute', weights='distance')
    knn.fit(X_train, y_train)
    return knn

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    
    print(f"\nAccuracy: {accuracy * 100:.2f}%")
    print(f"Macro F1-Score: {macro_f1:.2f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

def save_model_and_pca(model, pca, model_path='./model/knn.pkl', pca_path='./model/pca.pkl'):
    joblib.dump(model, model_path)
    joblib.dump(pca, pca_path)
    print("\nModel and PCA saved successfully!")

def main():
    
    load_dotenv()
    normalized_path = os.getenv('NORMALIZED_PATH')

    df = load_data(normalized_path)
    target_column = 'track genre_top'
    X, y = select_features(df, target_column)

    
    print("Original class distribution:")
    print(y.value_counts())

    X_filtered, y_filtered = filter_classes(X, y)

    print("\nFiltered class distribution:")
    print(y_filtered.value_counts())

    X_train, X_test, y_train, y_test = split_data(X_filtered, y_filtered)

    min_class_samples = y_train.value_counts().min()
    k_neighbors_smote = min(5, min_class_samples - 1)  
    
    X_train_smote, y_train_smote = apply_smote(X_train, y_train, k_neighbors_smote)
    
    print("\nClass distribution after SMOTE:")
    print(pd.Series(y_train_smote).value_counts())
    
    X_train_pca, X_test_pca, pca = apply_pca(X_train_smote, X_test)
    
    print(f"\nExplained variance by PCA components: {sum(pca.explained_variance_ratio_):.2f}")
    print(f"Variance explained by first 5 components: {pca.explained_variance_ratio_[:5]}")

    knn = train_knn(X_train_pca, y_train_smote)
    
    evaluate_model(knn, X_test_pca, y_test)
    
    save_model_and_pca(knn, pca)

if __name__ == "__main__":
    main()