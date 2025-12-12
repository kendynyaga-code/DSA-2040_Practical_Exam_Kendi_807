import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.decomposition import PCA

# --- Re-execute Data Prep (Essential for a standalone script) ---
iris = load_iris(as_frame=True)
df = iris.frame
df = df.rename(columns={'target': 'species_code'})
df['species_name'] = df['species_code'].map(dict(enumerate(iris.target_names)))

feature_cols = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
scaler = MinMaxScaler()
df[feature_cols] = scaler.fit_transform(df[feature_cols])

# X contains the normalized features
X = df[feature_cols]
# Actual species labels for comparison
y_true = df['species_code'] 

def save_plot(fig, filename):
    fig.savefig(filename, bbox_inches='tight')
    print(f"Plot saved as {filename}")

# -------------------------------------------------------------------
print("--- 1. K-Means Clustering with k=3 ---")

# Initialize and fit the K-Means model
kmeans_3 = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans_3.fit(X)

# Predict the cluster labels
y_pred_3 = kmeans_3.labels_

# Compare predicted clusters (y_pred_3) with actual species (y_true) using ARI
ari_score_3 = adjusted_rand_score(y_true, y_pred_3)

print(f"Adjusted Rand Index (ARI) for k=3: {ari_score_3:.4f}")

# Add the cluster labels to the DataFrame for visualization
df['cluster_k3'] = y_pred_3

print("\n--- 2. Experimentation: Elbow Method ---")
wcss = []
k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_) # inertia_ is the WCSS

# Plot the Elbow Curve
plt.figure(figsize=(8, 5))
plt.plot(k_range, wcss, marker='o')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('WCSS (Inertia)')
plt.grid(True)
fig = plt.gcf()
save_plot(fig, 'clustering_elbow_method.png')

print("Elbow method plot saved.")

# --- Try k=2 and k=4 ---
kmeans_2 = KMeans(n_clusters=2, random_state=42, n_init=10).fit(X)
ari_score_2 = adjusted_rand_score(y_true, kmeans_2.labels_)

kmeans_4 = KMeans(n_clusters=4, random_state=42, n_init=10).fit(X)
ari_score_4 = adjusted_rand_score(y_true, kmeans_4.labels_)

print(f"Adjusted Rand Index (ARI) for k=2: {ari_score_2:.4f}")
print(f"Adjusted Rand Index (ARI) for k=4: {ari_score_4:.4f}")

print("\n--- 3. Visualization of Clusters (k=3) ---")

# Scatter plot of Petal Length vs Petal Width, colored by predicted cluster
plt.figure(figsize=(9, 6))
sns.scatterplot(
    x='petal length (cm)',
    y='petal width (cm)',
    hue='cluster_k3',
    data=df,
    palette='viridis',
    style='species_name', # Use actual species to show overlap
    s=100
)
plt.title('K-Means Clusters (k=3) vs. Actual Species')
plt.legend(title='Cluster/Species')
fig = plt.gcf()
save_plot(fig, 'clustering_k3_visualization.png')


# Visualize using PCA (2 Principal Components)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
df_pca = pd.DataFrame(data=X_pca, columns=['PC1', 'PC2'])
df_pca['cluster_k3'] = df['cluster_k3']
df_pca['species_name'] = df['species_name']

plt.figure(figsize=(9, 6))
sns.scatterplot(
    x='PC1',
    y='PC2',
    hue='cluster_k3',
    data=df_pca,
    palette='viridis',
    style='species_name',
    s=100
)
plt.title('K-Means Clusters (k=3) on 2 Principal Components')
plt.legend(title='Cluster/Species')
fig = plt.gcf()
save_plot(fig, 'clustering_k3_pca_visualization.png')
print("PCA visualization saved.")