CREATE SCHEMA utilitiesenergydb;

SET search_path TO utilitiesenergydb;

-- Dim_Utility (Product Type Dimension)

CREATE TABLE Dim_Utility (
    Utility_Key INT PRIMARY KEY,
    Utility_Type VARCHAR(50) NOT NULL,  -- e.g., 'Electricity', 'Gas'
    Description VARCHAR(100),           -- e.g., 'Standard household power'
    Unit VARCHAR(10)                    -- e.g., 'kWh', 'm3'
);

-- Dim_Calendar (Time Dimension)
CREATE TABLE Dim_Calendar (
    Date_Key INT PRIMARY KEY,
    Date DATE NOT NULL,                 -- e.g., '2025-01-01'
    Year INT NOT NULL,                  -- e.g., 2025
    Month INT NOT NULL,                 -- e.g., 1
    Quarter INT NOT NULL,               -- e.g., 1
    Day INT NOT NULL,                   -- e.g., 1
    Hour INT                            -- e.g., 12 (for granular meter reads)
);

-- Dim_Vendor (Suppliers Dimension)
CREATE TABLE Dim_Vendor (
    Vendor_Key INT PRIMARY KEY,
    Vendor_Name VARCHAR(100) NOT NULL,  -- e.g., 'National Grid'
    Location VARCHAR(100),              -- e.g., 'UK National'
    Reliability_Score INT               -- e.g., 95 (optional metric)
);

-- Dim_Customer (Users Dimension)
CREATE TABLE Dim_Customer (
    Customer_Key INT PRIMARY KEY ,
    Customer_Name VARCHAR(100) NOT NULL, -- e.g., 'Household A'
    Customer_ID VARCHAR(50),             -- e.g., 'C001'
    Location VARCHAR(100),               -- e.g., 'Newcastle'
    Segment VARCHAR(50)                  -- e.g., 'Residential'
);

-- Fact_Consumption (Central Fact Table with FKs to Dims)
CREATE TABLE Fact_Consumption (
    Read_ID INT PRIMARY KEY ,
    Date_Key INT NOT NULL,
    Utility_Key INT NOT NULL,
    Vendor_Key INT NOT NULL,
    Customer_Key INT NOT NULL,
    Consumption_kWh DECIMAL(10,2) NOT NULL,  -- e.g., 10.00
    Cost DECIMAL(10,2),                      -- e.g., 1.00 (calculated)
    Revenue DECIMAL(10,2),                   -- e.g., 1.50 (calculated)
    Profit DECIMAL(10,2),                    -- e.g., 0.50 (Revenue - Cost)
    FOREIGN KEY (Date_Key) REFERENCES Dim_Calendar(Date_Key),
    FOREIGN KEY (Utility_Key) REFERENCES Dim_Utility(Utility_Key),
    FOREIGN KEY (Vendor_Key) REFERENCES Dim_Vendor(Vendor_Key),
    FOREIGN KEY (Customer_Key) REFERENCES Dim_Customer(Customer_Key)
);