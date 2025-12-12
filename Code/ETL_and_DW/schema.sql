---------------------------------
-- Dimension Tables
---------------------------------

-- Dim_Time: Used for time-based analysis
CREATE TABLE Dim_Time (
    Date_Key INTEGER PRIMARY KEY, 
    Full_Date TEXT NOT NULL UNIQUE, -- Natural Key (YYYY-MM-DD)
    Day_Of_Week TEXT,
    Month INTEGER,
    Quarter INTEGER,
    Year INTEGER
);

-- Dim_Customer: Used for demographic analysis
CREATE TABLE Dim_Customer (
    Customer_Key INTEGER PRIMARY KEY, 
    Customer_ID TEXT NOT NULL UNIQUE, -- Natural Key
    Gender TEXT, -- Male/Female
    Age INTEGER
);

-- Dim_Product: Used for product category analysis
CREATE TABLE Dim_Product (
    Product_Key INTEGER PRIMARY KEY, 
    Product_Category TEXT NOT NULL UNIQUE
);

-- Dim_Transaction: Used to track the unique transaction ID
CREATE TABLE Dim_Transaction (
    Transaction_Key INTEGER PRIMARY KEY, 
    Transaction_ID TEXT NOT NULL UNIQUE -- Natural Key
);

-----------------------------------
-- Fact Table
-----------------------------------

-- Fact_Sales: The central table containing measures and FKs
CREATE TABLE Fact_Sales (
    Sale_Key INTEGER PRIMARY KEY,
    
    -- Foreign Keys to Dimensions
    Date_Key INTEGER NOT NULL,
    Customer_Key INTEGER NOT NULL,
    Product_Key INTEGER NOT NULL,
    Transaction_Key INTEGER NOT NULL,
    
    -- Measures
    Quantity INTEGER NOT NULL,
    Price_Per_Unit REAL,
    Total_Amount REAL NOT NULL,

    -- Constraints enforcing the One-to-Many relationships
    FOREIGN KEY (Date_Key) REFERENCES Dim_Time(Date_Key),
    FOREIGN KEY (Customer_Key) REFERENCES Dim_Customer(Customer_Key),
    FOREIGN KEY (Product_Key) REFERENCES Dim_Product(Product_Key),
    FOREIGN KEY (Transaction_Key) REFERENCES Dim_Transaction(Transaction_Key)
);