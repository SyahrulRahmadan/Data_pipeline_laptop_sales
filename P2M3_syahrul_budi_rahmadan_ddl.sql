-- For Creating Table
CREATE TABLE laptop_sales (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(255),
    processor_brand VARCHAR(255),
    processor_name VARCHAR(255),
    processor_generation VARCHAR(255),
    ram_gb VARCHAR(255),
    ram_type VARCHAR(255),
    ssd VARCHAR(255),
    hdd VARCHAR(255),
    os VARCHAR(255),
    os_bit VARCHAR(255),
    graphic_card_gb VARCHAR(255),
    weight VARCHAR(255),
    warranty VARCHAR(255),
    touchscreen VARCHAR(255),
    msoffice VARCHAR(255),
    price INT,
    rating VARCHAR(255),
    number_of_ratings INT,
    number_of_reviews INT
);

-- For Selecting Table to preview
SELECT * FROM laptop_sales;

-- Note : im importing the table manually at table settings -> import/export