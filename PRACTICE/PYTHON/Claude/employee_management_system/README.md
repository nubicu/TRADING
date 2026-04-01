# Employee Management System

Sistem enterprise de management pentru angajați dezvoltat cu **Java Spring Boot** și **Oracle Database**.

## 📋 Cuprins

- [Tehnologii](#tehnologii)
- [Arhitectura Aplicației](#arhitectura-aplicației)
- [Cerințe](#cerințe)
- [Instalare și Configurare](#instalare-și-configurare)
- [Rularea Aplicației](#rularea-aplicației)
- [API Endpoints](#api-endpoints)
- [Structura Bazei de Date](#structura-bazei-de-date)
- [Exemple de Utilizare](#exemple-de-utilizare)

## 🚀 Tehnologii

### Backend
- **Java 17**
- **Spring Boot 3.2.0**
- **Spring Data JPA** - pentru persistență
- **Hibernate** - ORM
- **Maven** - build tool
- **Lombok** - reducerea boilerplate code

### Database
- **Oracle Database** (11g sau mai nou)
- **JDBC** - conectivitate
- **PL/SQL** - proceduri stocate și funcții

### Validare
- **Jakarta Validation API** - validare date

## 🏗️ Arhitectura Aplicației

Aplicația urmează arhitectura **Layered Architecture** (multi-tier):

```
┌─────────────────────────────────────┐
│      REST Controllers               │ ← Layer 1: Presentation
├─────────────────────────────────────┤
│      Service Layer                  │ ← Layer 2: Business Logic
├─────────────────────────────────────┤
│      Repository Layer (JPA)         │ ← Layer 3: Data Access
├─────────────────────────────────────┤
│      Oracle Database                │ ← Layer 4: Persistence
└─────────────────────────────────────┘
```

### Componentele Principale

1. **Entities** - mapează tabelele din baza de date
   - `Employee.java`
   - `Department.java`
   - `JobRole.java`

2. **DTOs (Data Transfer Objects)** - transferul de date între layers
   - `EmployeeDTO.java`
   - `DepartmentDTO.java`
   - `JobRoleDTO.java`

3. **Repositories** - Spring Data JPA repositories
   - `EmployeeRepository.java`
   - `DepartmentRepository.java`
   - `JobRoleRepository.java`

4. **Services** - logica de business
   - `EmployeeService.java`
   - `DepartmentService.java`
   - `JobRoleService.java`

5. **Controllers** - REST API endpoints
   - `EmployeeController.java`
   - `DepartmentController.java`
   - `JobRoleController.java`

## 📦 Cerințe

- **Java JDK 17** sau mai nou
- **Maven 3.6+**
- **Oracle Database** 11g sau mai nou
- **Oracle JDBC Driver** (inclus în pom.xml)

## ⚙️ Instalare și Configurare

### 1. Clonează sau descarcă proiectul

```bash
# Descarcă fișierele în directorul dorit
```

### 2. Configurează Oracle Database

Rulează scriptul SQL pentru crearea schemei:

```sql
-- Rulează în SQL*Plus sau SQL Developer
@database-setup.sql
```

Acest script va crea:
- 3 tabele: `EMPLOYEES`, `DEPARTMENTS`, `JOB_ROLES`
- Secvențe pentru ID-uri auto-increment
- Indexuri pentru performanță
- Proceduri stocate PL/SQL
- Triggere pentru actualizări automate
- Date de test

### 3. Configurează conexiunea la baza de date

Editează fișierul `application.properties`:

```properties
# Actualizează cu datele tale de conexiune
spring.datasource.url=jdbc:oracle:thin:@localhost:1521:ORCL
spring.datasource.username=your_username
spring.datasource.password=your_password
```

**Notă**: Înlocuiește:
- `localhost:1521:ORCL` - cu adresa și SID-ul bazei tale Oracle
- `your_username` - cu username-ul tău Oracle
- `your_password` - cu parola ta Oracle

## 🏃 Rularea Aplicației

### Opțiunea 1: Cu Maven

```bash
# În directorul rădăcină al proiectului
mvn clean install
mvn spring-boot:run
```

### Opțiunea 2: Cu JAR

```bash
# Build
mvn clean package

# Run
java -jar target/employee-management-1.0.0.jar
```

### Opțiunea 3: Din IDE

Importează proiectul Maven în IntelliJ IDEA sau Eclipse și rulează clasa:
```
com.company.employeemanagement.EmployeeManagementApplication
```

Aplicația va porni pe **http://localhost:8080**

## 📡 API Endpoints

Base URL: `http://localhost:8080/api`

### Employees Endpoints

| Method | Endpoint | Descriere |
|--------|----------|-----------|
| GET | `/employees` | Obține toți angajații |
| GET | `/employees/{id}` | Obține angajat după ID |
| GET | `/employees/active` | Obține angajați activi |
| GET | `/employees/department/{deptId}` | Angajați din departament |
| GET | `/employees/search?name=xyz` | Caută după nume |
| POST | `/employees` | Creează angajat nou |
| PUT | `/employees/{id}` | Actualizează angajat |
| PATCH | `/employees/{id}/salary` | Actualizează salariu |
| DELETE | `/employees/{id}` | Șterge (dezactivează) angajat |

### Departments Endpoints

| Method | Endpoint | Descriere |
|--------|----------|-----------|
| GET | `/departments` | Obține toate departamentele |
| GET | `/departments/{id}` | Obține departament după ID |
| POST | `/departments` | Creează departament nou |
| PUT | `/departments/{id}` | Actualizează departament |
| DELETE | `/departments/{id}` | Șterge departament |

### Job Roles Endpoints

| Method | Endpoint | Descriere |
|--------|----------|-----------|
| GET | `/job-roles` | Obține toate funcțiile |
| GET | `/job-roles/{id}` | Obține funcție după ID |
| POST | `/job-roles` | Creează funcție nouă |
| PUT | `/job-roles/{id}` | Actualizează funcție |
| DELETE | `/job-roles/{id}` | Șterge funcție |

## 🗄️ Structura Bazei de Date

### Tabelul EMPLOYEES

```sql
- employee_id (PK) - NUMBER(10)
- first_name - VARCHAR2(50)
- last_name - VARCHAR2(50)
- email - VARCHAR2(100) UNIQUE
- phone_number - VARCHAR2(20)
- hire_date - DATE
- salary - NUMBER(10,2)
- job_id (FK) - NUMBER(10)
- department_id (FK) - NUMBER(10)
- manager_id (FK) - NUMBER(10)
- is_active - NUMBER(1)
- created_date - TIMESTAMP
- updated_date - TIMESTAMP
```

### Tabelul DEPARTMENTS

```sql
- department_id (PK) - NUMBER(10)
- department_name - VARCHAR2(100) UNIQUE
- location - VARCHAR2(100)
- created_date - TIMESTAMP
```

### Tabelul JOB_ROLES

```sql
- job_id (PK) - NUMBER(10)
- job_title - VARCHAR2(100) UNIQUE
- min_salary - NUMBER(10,2)
- max_salary - NUMBER(10,2)
- created_date - TIMESTAMP
```

### Relații

- `EMPLOYEES.job_id` → `JOB_ROLES.job_id` (Many-to-One)
- `EMPLOYEES.department_id` → `DEPARTMENTS.department_id` (Many-to-One)
- `EMPLOYEES.manager_id` → `EMPLOYEES.employee_id` (Self-referencing)

## 📝 Exemple de Utilizare

### 1. Creează un departament nou

```bash
curl -X POST http://localhost:8080/api/departments \
  -H "Content-Type: application/json" \
  -d '{
    "departmentName": "IT",
    "location": "București"
  }'
```

### 2. Creează o funcție nouă

```bash
curl -X POST http://localhost:8080/api/job-roles \
  -H "Content-Type: application/json" \
  -d '{
    "jobTitle": "Software Developer",
    "minSalary": 4000,
    "maxSalary": 12000
  }'
```

### 3. Creează un angajat nou

```bash
curl -X POST http://localhost:8080/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Ion",
    "lastName": "Popescu",
    "email": "ion.popescu@company.com",
    "phoneNumber": "0721234567",
    "hireDate": "2024-01-15",
    "salary": 8000,
    "jobId": 1,
    "departmentId": 1
  }'
```

### 4. Obține toți angajații

```bash
curl http://localhost:8080/api/employees
```

### 5. Caută angajați după nume

```bash
curl http://localhost:8080/api/employees/search?name=Ion
```

### 6. Actualizează salariul unui angajat

```bash
curl -X PATCH http://localhost:8080/api/employees/1/salary \
  -H "Content-Type: application/json" \
  -d '{
    "newSalary": 9500
  }'
```

### 7. Obține angajații dintr-un departament

```bash
curl http://localhost:8080/api/employees/department/1
```

## 🎯 Caracteristici Implementate

### Backend Features

✅ **CRUD Operations** - pentru toate entitățile
✅ **Validare Date** - cu Jakarta Validation
✅ **Exception Handling** - centralizat cu `@RestControllerAdvice`
✅ **JPA Relations** - Many-to-One, One-to-Many, Self-referencing
✅ **Custom Queries** - cu Spring Data JPA
✅ **Soft Delete** - pentru angajați (is_active flag)
✅ **Business Logic** - validare salarii, verificare email duplicate
✅ **Logging** - cu SLF4J și Logback

### Database Features

✅ **Sequences** - pentru auto-increment IDs
✅ **Constraints** - foreign keys, unique, check
✅ **Indexes** - pentru performanță
✅ **Triggers** - pentru updated_date
✅ **Stored Procedures** - pentru operațiuni complexe
✅ **Functions** - pentru calcule (count employees)
✅ **Views** - pentru raportare (vw_employee_details)

## 🔐 Validări Implementate

### Employee Validation

- ✅ Prenume și nume obligatorii (2-50 caractere)
- ✅ Email valid și unic
- ✅ Telefon în format românesc (0721234567)
- ✅ Data angajării în trecut sau prezent
- ✅ Salariu pozitiv
- ✅ Salariu în limitele funcției (min/max)
- ✅ Email-uri duplicate nu sunt permise

### Department Validation

- ✅ Nume departament unic
- ✅ Nu se poate șterge departament cu angajați

### JobRole Validation

- ✅ Titlu funcție unic
- ✅ Salariu minim < Salariu maxim
- ✅ Nu se poate șterge funcție cu angajați

## 🧪 Testare cu Postman

1. Importează colecția de endpoints în Postman
2. Setează base URL: `http://localhost:8080/api`
3. Testează fiecare endpoint conform exemplelor de mai sus

## 📚 Resurse Suplimentare

### Învățare Java & Spring

- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Spring Data JPA](https://spring.io/projects/spring-data-jpa)
- [Baeldung Spring Tutorials](https://www.baeldung.com/spring-tutorial)

### Oracle Database

- [Oracle SQL Developer](https://www.oracle.com/database/sqldeveloper/)
- [Oracle Live SQL](https://livesql.oracle.com/)
- [PL/SQL Tutorial](https://www.oracletutorial.com/plsql-tutorial/)

## 🤝 Contribuții

Acest proiect este educațional. Sugestii de îmbunătățire:

- [ ] Adaugă Spring Security pentru autentificare
- [ ] Implementează paginare și sortare
- [ ] Adaugă rapoarte PDF/Excel
- [ ] Creează frontend cu React sau Angular
- [ ] Adaugă teste unitare (JUnit, Mockito)
- [ ] Implementează caching cu Redis
- [ ] Adaugă documentație API cu Swagger/OpenAPI

## 📄 Licență

Acest proiect este pentru scopuri educaționale.

---

**Dezvoltat cu ❤️ folosind Java Spring Boot și Oracle Database**
