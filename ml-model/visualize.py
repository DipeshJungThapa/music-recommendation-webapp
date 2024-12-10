import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

merged = pd.read_csv("./fma_metadata/output/merged_data.csv")


def choose_imputation(series):
    skewness = series.skew()
    outliers = series[np.abs(series - series.mean()) > (3 * series.std())]
    
    print(f"Skewness: {skewness}")
    print(f"Outlier percentage: {len(outliers)/len(series)*100:.2f}%")
    
    if abs(skewness) < 0.5 and len(outliers)/len(series) < 5:
        print("Imputing with mean")
        return series.mean()
    else:
        print("Imputing with median")
        return series.median()

print(choose_imputation(merged['track duration']))
plt.figure(figsize=(10, 6))
sns.barplot(x=merged.isnull().mean().index, y=merged.isnull().mean().values * 100)
plt.title('Percentage of Null Values per Column')
plt.xlabel('Columns')
plt.ylabel('Null Percentage')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("./diagrams/null values.png")

# Histogram
plt.figure(figsize=(10,6))
sns.histplot(merged['track duration'], kde=True)
plt.title('Distribution Visualization')
plt.savefig("./diagrams/distribution.png")

# Box plot to identify outliers
plt.figure(figsize=(10,6))
sns.boxplot(x=merged['track duration'])
plt.title('Boxplot to Detect Outliers')
plt.savefig("./diagrams/box plot.png")

missing_values = merged.isnull().sum()
print(missing_values)