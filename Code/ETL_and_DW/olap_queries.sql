-- ROLL-UP QUERY: Total sales aggregated by Country and Quarter
SELECT
    cd.Country,
    td.Year,
    td.Quarter,
    SUM(fs.TotalSales) AS TotalQuarterlySales
FROM
    SalesFact fs
JOIN
    CustomerDim cd ON fs.Customer_Key = cd.Customer_Key
JOIN
    TimeDim td ON fs.Date_Key = td.Date_Key
GROUP BY
    cd.Country,
    td.Year,
    td.Quarter
ORDER BY
    cd.Country,
    td.Year,
    td.Quarter;

-- DRILL-DOWN QUERY: Sales details for 'UK' broken down by Year and Month
SELECT
    td.Year,
    td.Month,
    COUNT(fs.Sale_Key) AS NumberOfSales,
    SUM(fs.TotalSales) AS TotalMonthlySales
FROM
    SalesFact fs
JOIN
    CustomerDim cd ON fs.Customer_Key = cd.Customer_Key
JOIN
    TimeDim td ON fs.Date_Key = td.Date_Key
WHERE
    cd.Country = 'United Kingdom' -- Assuming 'United Kingdom' is a value in your data
GROUP BY
    td.Year,
    td.Month
ORDER BY
    td.Year,
    td.Month;    

-- SLICE QUERY: Total sales filtered for the 'Kitchenware' category
SELECT
    pd.ProductCategory,
    SUM(fs.TotalSales) AS TotalSalesForCategory
FROM
    SalesFact fs
JOIN
    ProductDim pd ON fs.Product_Key = pd.Product_Key
WHERE
    pd.ProductCategory = 'Kitchenware'
GROUP BY
    pd.ProductCategory;