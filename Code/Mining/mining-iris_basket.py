import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


def save_plot(fig, filename):
    fig.savefig(filename, bbox_inches='tight')
    plt.close(fig) # Ensures the figure is finalized and saved
    print(f"Plot saved as {filename}")

# --- Necessary Re-execution of Data Prep ---
# Load Data
iris = load_iris(as_frame=True)
df = iris.frame
df = df.rename(columns={'target': 'species_code'})
df['species_name'] = df['species_code'].map(dict(enumerate(iris.target_names)))
feature_cols = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']

# Scale Features
scaler = MinMaxScaler()
df[feature_cols] = scaler.fit_transform(df[feature_cols])

# Encode Target
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['species_encoded'] = le.fit_transform(df['species_name'])

# Split Data (80/20)
X = df[feature_cols]
y = df['species_encoded']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Decision Tree Classifier
print("\n--- Part A: Decision Tree Classification ---")

# Initialize and train the Decision Tree model
dt_classifier = DecisionTreeClassifier(random_state=42)
dt_classifier.fit(X_train, y_train)

# Predict and compute metrics
y_pred_dt = dt_classifier.predict(X_test)

accuracy_dt = accuracy_score(y_test, y_pred_dt)
precision_dt = precision_score(y_test, y_pred_dt, average='weighted', zero_division=0)
recall_dt = recall_score(y_test, y_pred_dt, average='weighted', zero_division=0)
f1_dt = f1_score(y_test, y_pred_dt, average='weighted', zero_division=0)

print(f"Decision Tree Metrics:")
print(f"  Accuracy: {accuracy_dt:.4f}")
print(f"  Precision: {precision_dt:.4f}")
print(f"  Recall: {recall_dt:.4f}")
print(f"  F1-Score: {f1_dt:.4f}")

# Visualize the Decision Tree
target_names = iris.target_names

# Visualize the tree
plt.figure(figsize=(15, 10))
plot_tree(
    dt_classifier,
    feature_names=X_train.columns.tolist(),
    class_names=target_names,
    filled=True,
    rounded=True,
    fontsize=10
)
fig = plt.gcf()
save_plot(fig, 'decision_tree_visualization.png')

print("Decision Tree visualization saved.")

# Comparison with K-Nearest Neighbors Classifier
print("\n--- 2. Comparison with K-Nearest Neighbors (KNN, k=5) ---")

# Initialize and train the KNN model
knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train, y_train)

# Predict and compute metrics for KNN
y_pred_knn = knn_classifier.predict(X_test)

accuracy_knn = accuracy_score(y_test, y_pred_knn)
precision_knn = precision_score(y_test, y_pred_knn, average='weighted', zero_division=0)
recall_knn = recall_score(y_test, y_pred_knn, average='weighted', zero_division=0)
f1_knn = f1_score(y_test, y_pred_knn, average='weighted', zero_division=0)

print(f"KNN (k=5) Metrics:")
print(f"  Accuracy: {accuracy_knn:.4f}")
print(f"  Precision: {precision_knn:.4f}")
print(f"  Recall: {recall_knn:.4f}")
print(f"  F1-Score: {f1_knn:.4f}")

# Comparison Summary
print(f"\nComparison: DT Accuracy ({accuracy_dt:.4f}) vs KNN Accuracy ({accuracy_knn:.4f})")

# --- Part B: Association Rule Mining ---
print("\n--- Part B: Association Rule Mining ---")

# Pool of 20 items
item_pool = ['milk', 'bread', 'beer', 'diapers', 'eggs', 'cheese', 'coffee', 'tea', 
            'sugar', 'butter', 'apples', 'bananas', 'chicken', 'soda', 'chips', 
            'shampoo', 'soap', 'lotion', 'socks', 'magazines']

def generate_transactional_data(num_transactions, item_pool, min_items=3, max_items=8):
    """Generates synthetic transactional data with intentional co-occurrence."""
    transactions = []
    
    # Intentional pattern 1: Diapers and Beer often together
    pattern_1 = ['diapers', 'beer'] 
    
    # Intentional pattern 2: Milk and Bread often together
    pattern_2 = ['milk', 'bread']
    
    for i in range(num_transactions):
        basket = set()
        
        # Determine basket size
        basket_size = np.random.randint(min_items, max_items + 1)
        
        # Introduce patterns in 40% of transactions
        if np.random.rand() < 0.4:
            if np.random.rand() < 0.5:
                basket.update(pattern_1)
            else:
                basket.update(pattern_2)
        
        # Fill the rest of the basket randomly
        remaining_items_to_add = basket_size - len(basket)
        if remaining_items_to_add > 0:
            remaining_items = np.random.choice(item_pool, size=remaining_items_to_add, replace=False)
            basket.update(remaining_items)
        
        # Ensure no empty baskets are added if random choice failed
        if len(basket) > 0:
            transactions.append(list(basket))
        
    return transactions

transactions = generate_transactional_data(num_transactions=40, item_pool=item_pool)
print(f"Generated {len(transactions)} synthetic transactions.")

# Apply Apriori Algorithm
# Convert list of lists to Transactional DataFrame (One-Hot Encoding)
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_basket = pd.DataFrame(te_ary, columns=te.columns_)

print("\n--- Apriori Algorithm Results ---")

# Step 1: Find Frequent Itemsets (min_support=0.2)
frequent_itemsets = apriori(df_basket, min_support=0.2, use_colnames=True)
print(f"Found {len(frequent_itemsets)} frequent itemsets.")

# Step 2: Generate Association Rules (min_confidence=0.5)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)

# Sort by lift and display top 5 rules
rules = rules.sort_values(by=['lift', 'confidence'], ascending=False).reset_index(drop=True)

print("\nTop 5 Association Rules (Sorted by Lift):")
print(rules.head(5)[['antecedents', 'consequents', 'support', 'confidence', 'lift']])