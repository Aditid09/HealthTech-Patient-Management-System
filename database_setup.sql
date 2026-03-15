-- 1. CLEAN START: This deletes the old messy data and starts fresh
DROP DATABASE IF EXISTS HealthTechDB;
CREATE DATABASE HealthTechDB;
USE HealthTechDB;

-- 2. CREATE PATIENTS TABLE
-- DBA Note: 'UNIQUE' on Contact ensures no duplicate registrations
CREATE TABLE Patients (
    PatientID INT PRIMARY KEY AUTO_INCREMENT,
    FullName VARCHAR(100) NOT NULL,
    Age INT NOT NULL CHECK (Age >= 0),
    Gender ENUM('Male', 'Female', 'Other'),
    Contact VARCHAR(15) UNIQUE, 
    RegistrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. CREATE MEDICAL RECORDS TABLE
-- DBA Note: Linking to Patients via Foreign Key
CREATE TABLE MedicalRecords (
    RecordID INT PRIMARY KEY AUTO_INCREMENT,
    PatientID INT,
    Diagnosis TEXT NOT NULL,
    Prescription TEXT,
    DoctorName VARCHAR(100),
    VisitDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) ON DELETE CASCADE
);

-- 4. CREATE INDEX FOR PERFORMANCE
-- DBA Note: Optimizes searches by patient name
CREATE INDEX idx_patient_name ON Patients(FullName);

-- 5. INSERT 10 UNIQUE PATIENTS (Demo Data)
INSERT INTO Patients (FullName, Age, Gender, Contact) 
VALUES 
('Aditi Dahiwade', 21, 'Female', '9876543210'),
('Rahul Sharma', 35, 'Male', '9123456789'),
('Priya Patil', 28, 'Female', '9766554433'),
('Suresh Raina', 40, 'Male', '9822113344'),
('Anjali Gupta', 24, 'Female', '9111222333'),
('Vikram Singh', 52, 'Male', '9000888777'),
('Meera Deshmukh', 29, 'Female', '9366778899'),
('Amit Verma', 31, 'Male', '9633445566'),
('Kavita Rao', 48, 'Female', '9544556677'),
('Ishaan Malhotra', 20, 'Male', '9455667788');

-- 6. INSERT SAMPLE MEDICAL RECORDS
INSERT INTO MedicalRecords (PatientID, Diagnosis, Prescription, DoctorName)
VALUES 
(1, 'Viral Fever', 'Paracetamol 500mg', 'Dr. Mehta'),
(2, 'Back Pain', 'Physiotherapy & Rest', 'Dr. Kulkarni'),
(3, 'Iron Deficiency', 'Iron Supplements', 'Dr. Mehta');

-- 7. VERIFY
SELECT * FROM Patients;