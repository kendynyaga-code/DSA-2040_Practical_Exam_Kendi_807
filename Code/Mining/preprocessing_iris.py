import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. LOAD DATASET ---
iris = load_iris(as_frame=True)
df = iris.frame
# Rename the target column for clarity
df = df.rename(columns={'target': 'species_code'})

# Map the numerical target codes to actual species names for better visualization and analysis
df['species_name'] = df['species_code'].map(dict(enumerate(iris.target_names)))

print("--- Data Loading Complete ---")
print(df.head())

# --- 2. PREPROCESSING ---
# Check for missing values
print("\n--- 2a. Checking for Missing Values ---")
print(df.isnull().sum())
# In this dataset, there are no missing values.

# --- Normalize features using Min-Max Scaling ---
print("\n--- 2b. Normalizing Features ---")
# Identify features to scale
feature_cols = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
df_features = df[feature_cols]

# Initialize and apply Min-Max Scaler
scaler = MinMaxScaler()
df_scaled_features = scaler.fit_transform(df_features)

# Convert back to DataFrame and replace original feature columns
df_scaled = pd.DataFrame(df_scaled_features, columns=feature_cols)
df[feature_cols] = df_scaled
print("\n--- 2b. Feature Normalization (Min-Max Scaling) Complete ---")
print(df[feature_cols].head())

# --- Encode class labels ---
print("\n--- 2c. Encoding Class Labels ---")
label_encoder = LabelEncoder()
df['species_encoded'] = label_encoder.fit_transform(df['species_name'])
print("\n--- 2c. Class Label Encoding Complete ---")
print(df[['species_name', 'species_encoded']].head())


# --- 3. EXPLORE AND VISUALIZE DATA ---
print("\n--- 3a. Summary Statistics (After Scaling) ---")
print(df.describe())

# Visualize pairplot and correlation heatmap
# Set up figure saving function
def save_plot(fig, filename):
    fig.savefig(filename, bbox_inches='tight')
    print(f"Plot saved as {filename}")

# --- Pairplot (Relationship between all features) ---
g = sns.pairplot(df, hue='species_name', diag_kind='kde')
save_plot(g.fig, 'iris_pairplot.png')


# --- Correlation Heatmap ---
# Calculate correlation matrix for numerical features
corr_matrix = df[feature_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Heatmap of Iris Features')
fig = plt.gcf() # Get current figure
save_plot(fig, 'iris_correlation_heatmap.png')


print("\n--- 3b. Visualization Complete (Pairplot and Heatmap saved) ---")

# --- Boxplots for Outlier Detection ---
df_melted = df.melt(value_vars=feature_cols, var_name='Feature', value_name='Value')

plt.figure(figsize=(10, 6))
sns.boxplot(x='Feature', y='Value', data=df_melted)
plt.title('Boxplot for Iris Features (Outlier Check)')
plt.ylabel('Normalized Feature Value')
fig = plt.gcf()
save_plot(fig, 'iris_boxplots_outliers.png')


print("\n--- 3c. Outlier Check Complete (Boxplots saved) ---")


# --- 4. Function to Split Data into Train/Test (80/20) ---
def split_data(dataframe, test_size=0.2, random_state=42):
    """Splits the feature and target data into training and testing sets."""
    
    # Features (using the normalized columns)
    X = dataframe[feature_cols] 
    
    # Target (using the encoded label)
    y = dataframe['species_encoded'] 
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print("\n--- Data Split Complete ---")
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test

# Calling the function:
X_train, X_test, y_train, y_test = split_data(df)