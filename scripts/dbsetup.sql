DROP TABLE IF EXISTS Patients CASCADE;
DROP TABLE IF EXISTS Providers CASCADE;
DROP TABLE IF EXISTS PatientProviders CASCADE;

CREATE TABLE Patients (
	id SERIAL PRIMARY KEY,
	name VARCHAR(255) UNIQUE NOT NULL,
	password VARCHAR(1023) NOT NULL
);

CREATE TABLE Providers (
	id SERIAL PRIMARY KEY,
	name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE PatientProviders (
	patient_id INT NOT NULL,
	provider_id INT NOT NULL,
	PRIMARY KEY (patient_id, provider_id),
	FOREIGN KEY (patient_id) REFERENCES Patients(id),
	FOREIGN KEY (provider_id) REFERENCES Providers(id)
);

INSERT INTO Patients (name, password) VALUES
	('Jone Doe','D0pNC0ZGeQPhKAeWzlHyUsWtG3fW0peHcaXTzaPXz5Bh2WydUXVup1T3Oqvl9DPeAYlY9nLuM07hI4CiVNMGPsfXmJCjzXuu6rJ_N9kL1GJki1fPpi0LmlheUPsy0O0zQOFOXiAOg5TbDmzeJvAbQqKuRIz5q9kH4759VT-W3n7NPbBkkGmNbFhTUjaMjc6P_mnMo5oJ50JdbBr8R_8b08z3QLdmSg5DaJ2j7pY8kcJhjDZ7yW9430lrXCZTGXibxE1Vp3qjwklcfKDJjWWBnkSuXXYxGjCGD65vaiFrGg3RsXl5JViOg8Q5zAJjkJ2x_udH9Uo17AJL0KXbXyThv-T5ybrqu7vuW3uotuIB1H6DV4XdbPWNhD8VL1OoqPNU');

INSERT INTO Providers (name) VALUES
	('Health Primary'),
	('Health Secondary');

INSERT INTO PatientProviders (patient_id, provider_id)
SELECT Patients.id, Providers.id
FROM Patients, Providers
WHERE Patients.name = 'Jone Doe'
	AND Providers.name = 'Health Secondary';
