--creating database
CREATE DATABASE Hospital;

--go to database
\c Hospital;

-- Changing datestyle
SHOW DATESTYLE;
SET DATESTYLE TO 'DMY';

--Creating the table
DROP TABLE IF EXISTS Details;

CREATE TABLE Details(
					hospital_id SERIAL PRIMARY KEY,
					Hospital_Name VARCHAR(60),
					Hospital_Location VARCHAR(20),
					Department VARCHAR(20),
					Doctors_Count INTEGER,
					Patients_Count INTEGER,
					Admission_Date DATE,
					Discharge_Date DATE,
					Medical_Expenses NUMERIC(10,2)
);

--Checking the data
SELECT * FROM Details;

--Importing Data
COPY Details(Hospital_Name,	Hospital_Location,	Department,	Doctors_Count,	Patients_Count,	Admission_Date,	Discharge_Date,	Medical_Expenses)
FROM 'D:\PROGRAMMING\DATA SCIENCE\DATA ANALYTICS\SQL\Project\Hospital\Hospital_Data.csv'
CSV HEADER;

--QUERY QUESTIONS
-- 1. Total Number of Patients 
SELECT SUM(patients_count) AS total_patients
FROM Details;

-- 2. Average Number of Doctors per Hospital 
SELECT AVG(doctors_count) AS avg_doctors
FROM Details;

-- 3. Top 3 Departments with the Highest Number of Patients 
SELECT department, SUM(patients_count) AS patients
FROM Details
GROUP BY department
ORDER BY patients DESC
LIMIT 3;

-- 4. Hospital with the Maximum Medical Expenses
SELECT hospital_id, hospital_name, SUM(medical_expenses) AS max_medical_expense
FROM Details
GROUP BY hospital_id
ORDER BY max_medical_expense DESC
LIMIT 1;

-- 5. Daily Average Medical Expenses 
SELECT admission_date,AVG(medical_expenses) AS avg_expense
FROM Details
GROUP BY admission_date
ORDER BY admission_date;

-- 6. Longest Hospital Stay 
SELECT admission_date, discharge_date, AGE(discharge_date, admission_date) AS longest_stay
FROM Details
ORDER BY longest_stay DESC
LIMIT 100;

-- 7. Total Patients Treated Per City 
SELECT hospital_location, SUM(patients_count) AS total_patients
FROM Details
GROUP BY hospital_location;

-- 8. Average Length of Stay Per Department
SELECT department, AVG(AGE(discharge_date ,admission_date))
FROM Details
GROUP BY department;

-- 9. Identify the Department with the Lowest Number of Patients
SELECT department, SUM(patients_count) AS patients
FROM Details
GROUP BY department
ORDER BY patients
LIMIT 1;

-- 10.Monthly Medical Expenses Report
SELECT admission_date, EXTRACT(MONTH FROM admission_date) AS extracted_month, SUM(medical_expenses) AS avg_expense
FROM Details
GROUP BY admission_date
ORDER BY extracted_month;

SELECT EXTRACT(MONTH FROM admission_date) AS extracted_month, SUM(medical_expenses) AS avg_expense
FROM Details
GROUP BY extracted_month
ORDER BY extracted_month;

-- Created by VIEVK SAHU
-- Project link:- "https://github.com/VIVEKSAHU-06/Data-Analysis/tree/3c2866b411b403fed58f40ada68ad126e4cd29cb/SQL/Hospital%20Analysis"
