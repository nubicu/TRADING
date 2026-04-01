# API Test Examples for Employee Management System

## BASE URL
http://localhost:8080/api

---

## 1. DEPARTMENTS

### Create Department
POST http://localhost:8080/api/departments
Content-Type: application/json

{
  "departmentName": "Marketing",
  "location": "Cluj-Napoca"
}

### Get All Departments
GET http://localhost:8080/api/departments

### Get Department by ID
GET http://localhost:8080/api/departments/1

### Update Department
PUT http://localhost:8080/api/departments/1
Content-Type: application/json

{
  "departmentName": "Marketing Digital",
  "location": "Cluj-Napoca"
}

### Delete Department
DELETE http://localhost:8080/api/departments/1

---

## 2. JOB ROLES

### Create Job Role
POST http://localhost:8080/api/job-roles
Content-Type: application/json

{
  "jobTitle": "QA Engineer",
  "minSalary": 4500,
  "maxSalary": 10000
}

### Get All Job Roles
GET http://localhost:8080/api/job-roles

### Get Job Role by ID
GET http://localhost:8080/api/job-roles/1

### Update Job Role
PUT http://localhost:8080/api/job-roles/1
Content-Type: application/json

{
  "jobTitle": "Senior QA Engineer",
  "minSalary": 6000,
  "maxSalary": 13000
}

### Delete Job Role
DELETE http://localhost:8080/api/job-roles/1

---

## 3. EMPLOYEES

### Create Employee
POST http://localhost:8080/api/employees
Content-Type: application/json

{
  "firstName": "Maria",
  "lastName": "Ionescu",
  "email": "maria.ionescu@company.com",
  "phoneNumber": "0722345678",
  "hireDate": "2024-01-15",
  "salary": 7500,
  "jobId": 1,
  "departmentId": 1,
  "managerId": null
}

### Create Employee with Manager
POST http://localhost:8080/api/employees
Content-Type: application/json

{
  "firstName": "Andrei",
  "lastName": "Georgescu",
  "email": "andrei.georgescu@company.com",
  "phoneNumber": "0723456789",
  "hireDate": "2024-02-01",
  "salary": 5500,
  "jobId": 1,
  "departmentId": 1,
  "managerId": 1
}

### Get All Employees
GET http://localhost:8080/api/employees

### Get Active Employees Only
GET http://localhost:8080/api/employees/active

### Get Employee by ID
GET http://localhost:8080/api/employees/1

### Get Employees by Department
GET http://localhost:8080/api/employees/department/1

### Search Employees by Name
GET http://localhost:8080/api/employees/search?name=Ion

### Update Employee
PUT http://localhost:8080/api/employees/1
Content-Type: application/json

{
  "firstName": "Maria",
  "lastName": "Ionescu-Popescu",
  "email": "maria.ionescu@company.com",
  "phoneNumber": "0722345678",
  "hireDate": "2024-01-15",
  "salary": 8000,
  "jobId": 1,
  "departmentId": 1,
  "managerId": null,
  "isActive": 1
}

### Update Employee Salary
PATCH http://localhost:8080/api/employees/1/salary
Content-Type: application/json

{
  "newSalary": 9500
}

### Delete (Deactivate) Employee
DELETE http://localhost:8080/api/employees/1

---

## 4. VALIDATION TESTS

### Test Invalid Email
POST http://localhost:8080/api/employees
Content-Type: application/json

{
  "firstName": "Test",
  "lastName": "User",
  "email": "invalid-email",
  "phoneNumber": "0721234567",
  "hireDate": "2024-01-15",
  "salary": 5000,
  "jobId": 1
}
# Expected: 400 Bad Request with validation error

### Test Duplicate Email
POST http://localhost:8080/api/employees
Content-Type: application/json

{
  "firstName": "Another",
  "lastName": "Person",
  "email": "maria.ionescu@company.com",
  "phoneNumber": "0721234567",
  "hireDate": "2024-01-15",
  "salary": 5000,
  "jobId": 1
}
# Expected: 400 Bad Request - email already exists

### Test Invalid Phone Number
POST http://localhost:8080/api/employees
Content-Type: application/json

{
  "firstName": "Test",
  "lastName": "User",
  "email": "test@company.com",
  "phoneNumber": "123",
  "hireDate": "2024-01-15",
  "salary": 5000,
  "jobId": 1
}
# Expected: 400 Bad Request with phone validation error

### Test Salary Below Minimum
POST http://localhost:8080/api/employees
Content-Type: application/json

{
  "firstName": "Test",
  "lastName": "User",
  "email": "test2@company.com",
  "phoneNumber": "0721234567",
  "hireDate": "2024-01-15",
  "salary": 2000,
  "jobId": 1
}
# Expected: 400 Bad Request - salary below job minimum

### Test Salary Above Maximum
PATCH http://localhost:8080/api/employees/1/salary
Content-Type: application/json

{
  "newSalary": 50000
}
# Expected: 400 Bad Request - salary above job maximum

---

## 5. BUSINESS LOGIC TESTS

### Test Delete Department with Employees
# First create a department and employee
# Then try to delete the department
DELETE http://localhost:8080/api/departments/1
# Expected: 400 Bad Request - cannot delete department with employees

### Test Delete Job Role with Employees
DELETE http://localhost:8080/api/job-roles/1
# Expected: 400 Bad Request - cannot delete job role with employees

### Test Get Non-Existent Resource
GET http://localhost:8080/api/employees/99999
# Expected: 404 Not Found

---

## 6. COMPLETE WORKFLOW EXAMPLE

# Step 1: Create Department
POST http://localhost:8080/api/departments
Content-Type: application/json

{
  "departmentName": "Engineering",
  "location": "București"
}

# Step 2: Create Job Role
POST http://localhost:8080/api/job-roles
Content-Type: application/json

{
  "jobTitle": "Full Stack Developer",
  "minSalary": 5000,
  "maxSalary": 15000
}

# Step 3: Create Manager
POST http://localhost:8080/api/employees
Content-Type: application/json

{
  "firstName": "Alexandru",
  "lastName": "Manolescu",
  "email": "alexandru.manolescu@company.com",
  "phoneNumber": "0721111111",
  "hireDate": "2020-01-01",
  "salary": 14000,
  "jobId": 1,
  "departmentId": 1
}

# Step 4: Create Employee under Manager
POST http://localhost:8080/api/employees
Content-Type: application/json

{
  "firstName": "Diana",
  "lastName": "Popa",
  "email": "diana.popa@company.com",
  "phoneNumber": "0722222222",
  "hireDate": "2024-03-01",
  "salary": 6500,
  "jobId": 1,
  "departmentId": 1,
  "managerId": 1
}

# Step 5: Get all employees from department
GET http://localhost:8080/api/employees/department/1

# Step 6: Update employee salary
PATCH http://localhost:8080/api/employees/2/salary
Content-Type: application/json

{
  "newSalary": 7500
}

# Step 7: Search for employee
GET http://localhost:8080/api/employees/search?name=Diana

---

## NOTES:
- Replace IDs (1, 2, etc.) with actual IDs from your database
- All timestamps are in ISO 8601 format
- Phone numbers must match Romanian format: 0XXXXXXXXX or +4XXXXXXXXX
- Salaries must be within job role min/max ranges
