# Analysis Report: OLAP Insights and Decision Support

## 1. Data Warehouse Architecture and Support
The Retail Data Warehouse was successfully implemented using a Star Schema with a central **SalesFact** table linked to three dimension tables: **TimeDim**, **CustomerDim**, and **ProductDim**.  
This dimensional model supports OLAP by enabling rapid navigation across different business dimensions (time, customer, product).  
The ETL process ensured data integrity by removing transactions with missing CustomerIDs and filtering out invalid sales (Quantity ≤ 0).

---

## 2. Business Insights and Key Trends

### **Top-Selling Countries (Roll-up)**
The roll-up query confirmed that the **United Kingdom** is the dominant market, responsible for **over 90% of total revenue**.  
Germany and France contribute consistently but remain far smaller markets.  
This indicates the business should maintain strong focus on the UK while cautiously exploring growth in secondary markets.

### **Seasonal Volatility (Drill-down)**
A drill-down analysis of UK sales revealed significant seasonal peaks.  
Revenue accelerates sharply in **Quarter 4**, with **November and December** being the highest-earning months.  
This aligns with typical holiday shopping spikes.

### **Category Performance (Slice)**
A slice on the **Kitchenware** category showed stable, reliable revenue generation.  
This suggests Kitchenware is a steady product line, while categories like Home Decor or Accessories demonstrate more volatility despite high potential.

---

## 3. Support for Decision-Making

### **Inventory Optimization**
Based on seasonal trends, inventory teams should plan higher stock levels beginning in **September/October** to meet Q4 demand and avoid stock-outs.

### **Marketing Allocation**
Marketing budgets should prioritize the UK market and focus on campaigns launched just before the Q4 surge.  
Secondary markets such as Germany and France can be used for smaller experimental campaigns.

### **Product Strategy**
Category slice insights help differentiate between:
- **Stable revenue streams** (e.g., Kitchenware) requiring consistent supply chain management.
- **High-growth but high-risk categories** that need targeted marketing and demand forecasting.

---

## 4. Impact of Source Data Realism
The UCI dataset is transactional and lacks demographic attributes such as Age or Income.  
To build the required CustomerDim, customer age was **synthetically generated**, meaning age-related insights are not fully realistic and should be validated with external data before informing critical decisions.

However, the **historical sales patterns** (time trends, product performance, seasonal peaks) remain realistic because they are based on genuine transaction history.

