CREATE TABLE Patients (
	id INT  PRIMARY KEY NOT NULL,
	name VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL
);

CREATE TABLE Providers (
	id INT  PRIMARY KEY NOT NULL,
	name VARCHAR(255) NOT NULL
);

CREATE TABLE PatientProviders (
	patient_id INT NOT NULL,
	provider_id INT NOT NULL,
	PRIMARY KEY (patient_id, provider_id),
	FOREIGN KEY (patient_id) REFERENCES Patients(id),
	FOREIGN KEY (provider_id) REFERENCES Providers(id)
);