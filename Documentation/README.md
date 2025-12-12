# Retail Data Warehouse and Data Mining Project  
This document summarizes the full lifecycle of your Data Warehouse and Data Mining project — including design, ETL implementation, OLAP analysis, clustering, classification, and association rule mining.

# **Task 1: Data Warehouse Design**

## Retail Data Warehouse Star Schema Design

This submission fulfills the requirements for designing a data warehouse schema for a retail company, utilizing a publicly available Kaggle dataset that provides transactional, product category, and customer demographic data.

---

## 1. Star Schema Design Overview

The data warehouse is modeled using a **Star Schema** centered on a single fact table (`Fact_Sales`), which measures key business events, and four directly connected dimension tables that provide context.

### Fact Table: `Fact_Sales`

| Role | Attribute Name | Description |
| :--- | :--- | :--- |
| **Primary Key** | `Sale_Key` | Surrogate key for the fact record. |
| **Foreign Keys** | `Date_Key` | Links to `Dim_Time` for temporal analysis. |
| | `Customer_Key` | Links to `Dim_Customer` for demographic analysis. |
| | `Product_Key` | Links to `Dim_Product` for category analysis. |
| | `Transaction_Key` | Links to `Dim_Transaction` for tracking the natural transaction ID. |
| **Measures** | `Total_Amount` | The monetary value of the sale. |
| | `Quantity` | The number of units sold in the transaction. |
| | `Price_Per_Unit` | The price of a single unit. |

### Dimension Tables

| Dimension Table | Key Attributes Included | Supported Analysis |
| :--- | :--- | :--- |
| **Dim_Time** | `Date_Key (PK)`, `Full_Date`, `Year`, `Quarter`, `Month`, `Day_Of_Week` | Sales trends by quarter/month. |
| **Dim_Customer** | `Customer_Key (PK)`, `Customer_ID`, `Gender`, `Age` | Customer demographic analysis. |
| **Dim_Product** | `Product_Key (PK)`, `Product_Category` | Sales by product category. |
| **Dim_Transaction** | `Transaction_Key (PK)`, `Transaction_ID` | Tracking unique transaction instances. |

<img width="907" height="639" alt="star-schema-diagram" src="https://github.com/user-attachments/assets/ab705144-8498-497c-b56f-212f4b4987d5" />
---

## 2. Explanation: Star Schema Choice

We chose the **Star Schema** over the Snowflake Schema because it prioritizes **query performance** and **simplicity** for typical business intelligence (BI) reporting. A Star Schema requires only a **single, direct join** between the central Fact table and any Dimension table, making queries faster and easier to write. The Snowflake Schema, while achieving higher data normalization, complicates queries by necessitating multiple, cascading joins through sub-dimensions, which ultimately slows down the analytical processing critical to a high-performance data warehouse environment.

---

## 3. SQL CREATE TABLE Statements (SQLite)

The SQL statements to create the schema are provided in the `schema.sql` file.

```sql
-- ---------------------------------
-- Dimension Tables
-- ---------------------------------

CREATE TABLE Dim_Time (
    Date_Key INTEGER PRIMARY KEY,
    Full_Date TEXT NOT NULL UNIQUE,
    Day_Of_Week TEXT,
    Month INTEGER,
    Quarter INTEGER,
    Year INTEGER
);

CREATE TABLE Dim_Customer (
    Customer_Key INTEGER PRIMARY KEY,
    Customer_ID TEXT NOT NULL UNIQUE,
    Gender TEXT,
    Age INTEGER
);

CREATE TABLE Dim_Product (
    Product_Key INTEGER PRIMARY KEY,
    Product_Category TEXT NOT NULL UNIQUE
);

CREATE TABLE Dim_Transaction (
    Transaction_Key INTEGER PRIMARY KEY,
    Transaction_ID TEXT NOT NULL UNIQUE
);

-- ---------------------------------
-- Fact Table
-- ---------------------------------

CREATE TABLE Fact_Sales (
    Sale_Key INTEGER PRIMARY KEY,
    
    -- Foreign Keys
    Date_Key INTEGER NOT NULL,
    Customer_Key INTEGER NOT NULL,
    Product_Key INTEGER NOT NULL,
    Transaction_Key INTEGER NOT NULL,
    
    -- Measures
    Quantity INTEGER NOT NULL,
    Price_Per_Unit REAL,
    Total_Amount REAL NOT NULL,

    -- Constraints
    FOREIGN KEY (Date_Key) REFERENCES Dim_Time(Date_Key),
    FOREIGN KEY (Customer_Key) REFERENCES Dim_Customer(Customer_Key),
    FOREIGN KEY (Product_Key) REFERENCES Dim_Product(Product_Key),
    FOREIGN KEY (Transaction_Key) REFERENCES Dim_Transaction(Transaction_Key)
);

```
## **Task 2: ETL Process Implementation**

The ETL process was implemented using Python in the `etl_retail.py` script.

### **ETL Summary Table**

| Stage        | Action                                                                 | Resulting Rows |
|--------------|-------------------------------------------------------------------------|----------------|
| **Extraction** | Loaded raw Excel data and dropped rows with missing `CustomerID`.        | **406,829**    |
| **Transformation** | Calculated `TotalSales`, removed invalid rows, filtered last-year data. | **383,380**    |
| **Loading** | Loaded tables into `retail_dw.db` (3 dimensions + 1 fact).               | **383,380** Fact Rows |

---

### **Key Transformation Details**

#### **Metric Calculation**
- `TotalSales = Quantity × UnitPrice`

#### **Derived Attributes**
- **ProductDim → ProductCategory**  
  Category assigned using keywords from `Description` (e.g., “mug” → *Kitchenware*).

- **CustomerDim → Age**  
  Age was **synthetically generated** due to missing demographics.

- **SalesFact → Degenerate Dimension**  
  `InvoiceNo` stored directly in the fact table for transactional counting.

---
#### 2.4 Data Loading Verification

To confirm the integrity of the ETL process and the resulting Star Schema, screenshots of the critical table contents were captured using a SQLite browser. These images verify the successful loading of all 383,380 fact rows and confirm:
1.  **Dimension Keys:** That the primary keys (`_Key`) were correctly generated.
2.  **Derived Data:** That the calculated (`TotalSales`) and derived (`ProductCategory`, synthetic `Age`) attributes were successfully loaded into the dimension tables.

* [Screenshot: SalesFact Table] (c:\Users\nyaga\OneDrive\Pictures\Screenshots\Screenshot 2025-12-12 194134.png)
* [Screenshot: CustomerDim Table] (c:\Users\nyaga\OneDrive\Pictures\Screenshots\Screenshot 2025-12-12 193756.png)
* [Screenshot: ProductDim Table] (c:\Users\nyaga\OneDrive\Pictures\Screenshots\Screenshot 2025-12-12 194217.png)


## **Task 3: OLAP Queries &  Analysis**

Three OLAP-style SQL queries were implemented to analyze sales performance.

### **OLAP Queries**
- **Roll-up**: Total Sales by *Country → Quarter*
- **Drill-down**: Monthly sales within the *United Kingdom*
- **Slice**: Sales filtered where `ProductCategory = 'Kitchenware'`

### **Analytical Insights**

#### 📊 *Market Concentration*
- The **United Kingdom dominates revenue**, far ahead of other countries.

#### 📈 *Seasonality*
- A strong **Q4 spike (Nov–Dec)** was observed — critical for inventory planning.

#### 🗂️ *Product Category Trends*
- *Kitchenware* provides stable, predictable revenue.

### **Visualization**
*(Include in your report)*  
![Total Sales by Country Bar Chart]("C:\Users\nyaga\OneDrive\Desktop\ENDSEM-DSA2040\sales_by_country_chart.png")

---

# **2. Section 2: Data Mining (Unsupervised & Supervised Learning)**

## **Task 1: Data Preprocessing**
- Used Min-Max Scaling on all numeric features  
- Encoded the target variable  
- Split the dataset into:  
  - 80% Training  
  - 20% Testing  

* **Feature Relationships (Pairplot):** A Pairplot visualization was generated, revealing clear visual separation between the *Iris setosa* species and the other two.
 (![Pairplot of Iris Features](image.png))
 
 * **Correlation Heatmap:** The heatmap confirmed strong positive correlations (e.g., between Petal Length and Petal Width).
![Correlation Heatmap of Iris Features] (image-1.png)

* **Outlier Detection (Boxplots):** Boxplots were used to examine the feature distributions, primarily identifying minor outliers in the **Sepal Width** dimension.
    ![Boxplots for Outlier Check] (image-2.png)
---

## **Task 2: Clustering (K-Means)**

### **Optimal K Determination**
- The **Elbow Method** identified **K = 3**, matching the three real Iris species.

### **Cluster Quality**
- **Adjusted Rand Index (ARI) > 0.9**  
  → Excellent agreement with actual species labels.

### **Real-World Application**
- Ideal for **Customer Segmentation**, enabling:
  - High-spend loyal groups
  - Discount-seekers
  - New customers  
- Helps businesses customize marketing strategies.


---

## **Task 3: Classification & Association Rule Mining**

### **Part A: Classification**

Two models were compared:

| Metric       | Decision Tree (DT) | KNN (k=5) |
|--------------|--------------------|-----------|
| **Accuracy** | 0.9333             | **0.9667** |
| Precision    | 0.9333             | **0.9697** |
| Recall       | 0.9333             | **0.9667** |
| F1-Score     | 0.9333             | **0.9666** |

#### **Conclusion**
- **KNN** performs better overall due to its ability to model smooth, non-linear boundaries.
- **Decision Tree** remains valuable for **interpretability**, showing decision rules clearly.

## Visualizations
* **Optimal K Justification:** The Elbow plot clearly showed an optimal point at **$K=3$**, where the decrease in WCSS (Inertia) began to flatten significantly.
    ![Elbow Method Plot for K-Means](image-3.png)

* **Cluster Visualization (Petal Features):** The scatter plot using Petal Length and Width confirmed the K-Means separation by color.
    ![K-Means Clusters (k=3) vs. Actual Species](image-4.png)

* **PCA Visualization:** The clusters were also mapped onto the two principal components (PC1 and PC2), which captures the maximum variance, further proving the clean separation.
    ![K-Means Clusters (k=3) on 2 Principal Components(image-5.png)
---

### **Part B: Association Rule Mining (Apriori)**

Synthetic basket data was used to uncover frequent item patterns.

#### **Top Example Rule**
- **{bread} → {milk}**  
  - **Support:** 0.225  
  - **Confidence:** 0.69  
  - **Lift:** **1.54**

### **Interpretation**
- Customers who buy bread are **54% more likely** to buy milk than average.
- Suggests:
  - Bundle promotions  
  - Shelf placement optimization  
  - Cross-selling high-margin items nearby  

---

# **✔ Final Deliverables**
This project demonstrated:
- A fully functioning Retail Data Warehouse  
- End-to-end ETL with clean dimensional modeling  
- OLAP insights supporting real business decisions  
- Clustering, classification, and association rule mining  
- Strong alignment between Data Warehouse and Data Mining perspectives  

---
