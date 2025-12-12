# 📝 Analysis Report for Task 3  
### Classification & Association Mining
---
## Part A: Classification Comparison

The objective was to compare the performance of an interpretable model (**Decision Tree**) with a non-linear, instance-based model (**K-Nearest Neighbors, KNN**) on the Iris test set.

### **Performance Metrics**

| Metric      | Decision Tree (DT) | KNN (k=5) |
|-------------|--------------------|-----------|
| Accuracy    | 0.9333             | 0.9667    |
| Precision   | 0.9333             | 0.9697    |
| Recall      | 0.9333             | 0.9667    |
| F1-Score    | 0.9333             | 0.9666    |

### **Conclusion on Model Comparison**

The **K-Nearest Neighbors (KNN)** classifier with **k=5** outperformed the Decision Tree across all evaluation metrics, achieving **3.34% higher accuracy**. This advantage is expected for the Iris dataset because the class boundaries—especially between *Iris versicolor* and *Iris virginica*—are smooth and non-linear.  
KNN naturally adapts to these boundaries without needing explicit splitting rules.

However, the **Decision Tree** model offers valuable **interpretability**.  
Its tree visualization shows the exact decision path (e.g., *Petal Length < 0.8*) used to classify a sample. This makes DT useful when explanations are required for human stakeholders.

---

## Part B: Association Rule Analysis

The Apriori algorithm was applied to the synthetic transaction dataset, and it discovered several meaningful association rules.

### **Top 5 Association Rules**

| Rank | Rule                                 | Support | Confidence | Lift |
|------|---------------------------------------|---------|------------|------|
| 1    | {bread} → {milk}                      | 0.225   | 0.69       | 1.54 |
| 2    | {beer} → {diapers}                    | 0.225   | 0.60       | 1.20 |

---

### **Analysis of Rule 1: `{bread} → {milk}`**

**Interpretation:**  
This rule shows that **69%** of customers who buy bread also purchase milk.  
With a **Support of 22.5%**, this pair appears in over one-fifth of all transactions, making it a strongly recurring pattern.

**Lift = 1.54:**  
A lift greater than 1 means the items are bought together more often than by random chance.  
Here, lift = **1.54** suggests a customer is **54% more likely** to buy milk if they have already picked up bread.

**Retail Recommendation:**  
Because this relationship involves essential grocery staples, a retailer can:

- Place **bread and milk close together** to create a faster shopping route.  
- Offer **bundle deals** (e.g., "Buy bread + milk and save 10%").  
- Position a **high-margin item** (cheese, butter, pastries) along the bread–milk path to capitalize on the high traffic flow.

---

This concludes the structured analysis for Task 3.
