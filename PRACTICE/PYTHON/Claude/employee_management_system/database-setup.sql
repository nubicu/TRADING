-- ============================================
-- Employee Management System - Oracle Database Schema
-- ============================================

-- Crearea tabelei pentru departamente
CREATE TABLE departments (
    department_id NUMBER(10) PRIMARY KEY,
    department_name VARCHAR2(100) NOT NULL,
    location VARCHAR2(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_dept_name UNIQUE (department_name)
);

-- Crearea secvenței pentru department_id
CREATE SEQUENCE dept_seq START WITH 1 INCREMENT BY 1;

-- Crearea tabelei pentru funcții/roluri
CREATE TABLE job_roles (
    job_id NUMBER(10) PRIMARY KEY,
    job_title VARCHAR2(100) NOT NULL,
    min_salary NUMBER(10,2),
    max_salary NUMBER(10,2),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_job_title UNIQUE (job_title)
);

-- Crearea secvenței pentru job_id
CREATE SEQUENCE job_seq START WITH 1 INCREMENT BY 1;

-- Crearea tabelei pentru angajați
CREATE TABLE employees (
    employee_id NUMBER(10) PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) NOT NULL,
    phone_number VARCHAR2(20),
    hire_date DATE NOT NULL,
    job_id NUMBER(10) NOT NULL,
    salary NUMBER(10,2) NOT NULL,
    department_id NUMBER(10),
    manager_id NUMBER(10),
    is_active NUMBER(1) DEFAULT 1,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_emp_email UNIQUE (email),
    CONSTRAINT fk_emp_job FOREIGN KEY (job_id) REFERENCES job_roles(job_id),
    CONSTRAINT fk_emp_dept FOREIGN KEY (department_id) REFERENCES departments(department_id),
    CONSTRAINT fk_emp_manager FOREIGN KEY (manager_id) REFERENCES employees(employee_id),
    CONSTRAINT chk_salary_positive CHECK (salary > 0),
    CONSTRAINT chk_is_active CHECK (is_active IN (0, 1))
);

-- Crearea secvenței pentru employee_id
CREATE SEQUENCE emp_seq START WITH 1 INCREMENT BY 1;

-- Crearea indexurilor pentru performanță
CREATE INDEX idx_emp_dept ON employees(department_id);
CREATE INDEX idx_emp_job ON employees(job_id);
CREATE INDEX idx_emp_manager ON employees(manager_id);
CREATE INDEX idx_emp_email ON employees(email);
CREATE INDEX idx_emp_name ON employees(last_name, first_name);

-- ============================================
-- Triggers pentru actualizare automată
-- ============================================

-- Trigger pentru actualizarea updated_date
CREATE OR REPLACE TRIGGER trg_emp_update_date
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    :NEW.updated_date := CURRENT_TIMESTAMP;
END;
/

-- ============================================
-- Proceduri stocate (PL/SQL)
-- ============================================

-- Procedură pentru adăugarea unui angajat
CREATE OR REPLACE PROCEDURE sp_add_employee (
    p_first_name IN VARCHAR2,
    p_last_name IN VARCHAR2,
    p_email IN VARCHAR2,
    p_phone_number IN VARCHAR2,
    p_hire_date IN DATE,
    p_job_id IN NUMBER,
    p_salary IN NUMBER,
    p_department_id IN NUMBER,
    p_manager_id IN NUMBER,
    p_employee_id OUT NUMBER
) AS
BEGIN
    INSERT INTO employees (
        employee_id, first_name, last_name, email, phone_number,
        hire_date, job_id, salary, department_id, manager_id
    ) VALUES (
        emp_seq.NEXTVAL, p_first_name, p_last_name, p_email, p_phone_number,
        p_hire_date, p_job_id, p_salary, p_department_id, p_manager_id
    ) RETURNING employee_id INTO p_employee_id;
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- Procedură pentru actualizarea salariului
CREATE OR REPLACE PROCEDURE sp_update_salary (
    p_employee_id IN NUMBER,
    p_new_salary IN NUMBER
) AS
    v_job_id NUMBER;
    v_min_salary NUMBER;
    v_max_salary NUMBER;
BEGIN
    -- Verifică dacă angajatul există și obține job_id
    SELECT job_id INTO v_job_id
    FROM employees
    WHERE employee_id = p_employee_id;
    
    -- Verifică limitele salariale pentru funcție
    SELECT min_salary, max_salary INTO v_min_salary, v_max_salary
    FROM job_roles
    WHERE job_id = v_job_id;
    
    -- Validează salariul
    IF p_new_salary < v_min_salary OR p_new_salary > v_max_salary THEN
        RAISE_APPLICATION_ERROR(-20001, 
            'Salariul trebuie să fie între ' || v_min_salary || ' și ' || v_max_salary);
    END IF;
    
    -- Actualizează salariul
    UPDATE employees
    SET salary = p_new_salary
    WHERE employee_id = p_employee_id;
    
    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20002, 'Angajatul nu există');
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- Funcție pentru calculul numărului de angajați per departament
CREATE OR REPLACE FUNCTION fn_count_employees_by_dept (
    p_department_id IN NUMBER
) RETURN NUMBER AS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM employees
    WHERE department_id = p_department_id
    AND is_active = 1;
    
    RETURN v_count;
END;
/

-- View pentru raportare
CREATE OR REPLACE VIEW vw_employee_details AS
SELECT 
    e.employee_id,
    e.first_name,
    e.last_name,
    e.email,
    e.phone_number,
    e.hire_date,
    e.salary,
    e.is_active,
    j.job_title,
    d.department_name,
    d.location,
    m.first_name || ' ' || m.last_name AS manager_name,
    TRUNC(MONTHS_BETWEEN(SYSDATE, e.hire_date) / 12, 1) AS years_of_service
FROM employees e
LEFT JOIN job_roles j ON e.job_id = j.job_id
LEFT JOIN departments d ON e.department_id = d.department_id
LEFT JOIN employees m ON e.manager_id = m.employee_id;

-- ============================================
-- Date de test
-- ============================================

-- Inserare departamente
INSERT INTO departments (department_id, department_name, location) 
VALUES (dept_seq.NEXTVAL, 'IT', 'București');
INSERT INTO departments (department_id, department_name, location) 
VALUES (dept_seq.NEXTVAL, 'HR', 'Cluj-Napoca');
INSERT INTO departments (department_id, department_name, location) 
VALUES (dept_seq.NEXTVAL, 'Financiar', 'Timișoara');
INSERT INTO departments (department_id, department_name, location) 
VALUES (dept_seq.NEXTVAL, 'Vânzări', 'Iași');

-- Inserare funcții
INSERT INTO job_roles (job_id, job_title, min_salary, max_salary) 
VALUES (job_seq.NEXTVAL, 'Software Developer', 4000, 12000);
INSERT INTO job_roles (job_id, job_title, min_salary, max_salary) 
VALUES (job_seq.NEXTVAL, 'Senior Developer', 8000, 18000);
INSERT INTO job_roles (job_id, job_title, min_salary, max_salary) 
VALUES (job_seq.NEXTVAL, 'HR Manager', 5000, 10000);
INSERT INTO job_roles (job_id, job_title, min_salary, max_salary) 
VALUES (job_seq.NEXTVAL, 'Contabil', 3500, 8000);
INSERT INTO job_roles (job_id, job_title, min_salary, max_salary) 
VALUES (job_seq.NEXTVAL, 'Sales Representative', 3000, 9000);

-- Inserare angajați
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id, manager_id)
VALUES (emp_seq.NEXTVAL, 'Ion', 'Popescu', 'ion.popescu@company.com', '0721234567', TO_DATE('2020-01-15', 'YYYY-MM-DD'), 2, 15000, 1, NULL);

INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id, manager_id)
VALUES (emp_seq.NEXTVAL, 'Maria', 'Ionescu', 'maria.ionescu@company.com', '0722345678', TO_DATE('2021-03-20', 'YYYY-MM-DD'), 1, 7000, 1, 1);

INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id, manager_id)
VALUES (emp_seq.NEXTVAL, 'Andrei', 'Georgescu', 'andrei.georgescu@company.com', '0723456789', TO_DATE('2019-06-10', 'YYYY-MM-DD'), 3, 8000, 2, NULL);

INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id, manager_id)
VALUES (emp_seq.NEXTVAL, 'Elena', 'Vasilescu', 'elena.vasilescu@company.com', '0724567890', TO_DATE('2022-02-14', 'YYYY-MM-DD'), 4, 5500, 3, NULL);

COMMIT;
