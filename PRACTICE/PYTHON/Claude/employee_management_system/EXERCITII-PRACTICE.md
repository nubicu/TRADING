# 🎯 Exerciții Practice - Employee Management System

Exerciții pentru a învăța și exersa Java Spring Boot și Oracle DB

## 📋 Nivel Beginner

### Exercițiul 1: Înțelege Flow-ul CRUD

**Obiectiv**: Urmărește cum funcționează o operațiune CRUD completă

**Task-uri**:
1. Creează un departament nou prin API
2. Pune breakpoint în `DepartmentController.createDepartment()`
3. Rulează în debug mode și urmărește:
   - Cum ajunge request-ul la controller
   - Cum se apelează service-ul
   - Cum se salvează în repository
   - Cum se returnează răspunsul

**Ce vei învăța**: Request flow, Layered Architecture, Spring DI

---

### Exercițiul 2: Testează Validările

**Obiectiv**: Înțelege cum funcționează Jakarta Validation

**Task-uri**:
1. Creează un angajat cu email invalid → vezi eroarea
2. Creează angajat cu telefon greșit → vezi eroarea
3. Încearcă să creezi angajat cu email duplicat
4. Pune salariu 0 sau negativ

**Ce vei învăța**: Data validation, Exception handling

---

### Exercițiul 3: Explorează JPA Relations

**Obiectiv**: Înțelege relațiile între entități

**Task-uri**:
1. Creează 3 angajați în același departament
2. Obține departamentul și vezi lista de angajați
3. Creează angajat cu manager
4. Obține managerul și vezi lista de subordonați

**SQL pentru verificare**:
```sql
-- Vezi ierarhia manager-subordonați
SELECT 
    e.employee_id,
    e.first_name || ' ' || e.last_name as employee_name,
    m.first_name || ' ' || m.last_name as manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;
```

**Ce vei învăța**: JPA relations, Lazy loading, FetchType

---

## 📚 Nivel Intermediate

### Exercițiul 4: Adaugă un nou Endpoint

**Obiectiv**: Creează funcționalitate nouă

**Task**: Adaugă endpoint pentru calculul salariului mediu per departament

**Pași**:

1. Creează metoda în Repository:
```java
@Query("SELECT AVG(e.salary) FROM Employee e WHERE e.department.departmentId = :deptId")
BigDecimal getAverageSalaryByDepartment(@Param("deptId") Long deptId);
```

2. Adaugă metoda în Service:
```java
public BigDecimal getAverageSalary(Long departmentId) {
    return employeeRepository.getAverageSalaryByDepartment(departmentId);
}
```

3. Adaugă endpoint în Controller:
```java
@GetMapping("/department/{deptId}/average-salary")
public ResponseEntity<SalaryResponse> getAverageSalary(@PathVariable Long deptId) {
    BigDecimal avg = employeeService.getAverageSalary(deptId);
    return ResponseEntity.ok(new SalaryResponse(avg));
}
```

**Testează**:
```bash
curl http://localhost:8080/api/employees/department/1/average-salary
```

**Ce vei învăța**: Custom queries, JPQL, Endpoint creation

---

### Exercițiul 5: Implementează Paginare

**Obiectiv**: Adaugă paginare pentru lista de angajați

**Task**: Modifică endpoint-ul GET /employees să suporte paginare

**Pași**:

1. Schimbă Repository să extends `PagingAndSortingRepository`:
```java
public interface EmployeeRepository extends JpaRepository<Employee, Long> {
    Page<Employee> findByIsActive(Integer isActive, Pageable pageable);
}
```

2. Actualizează Service:
```java
public Page<EmployeeDTO> getActiveEmployees(int page, int size) {
    Pageable pageable = PageRequest.of(page, size, Sort.by("lastName").ascending());
    Page<Employee> employees = employeeRepository.findByIsActive(1, pageable);
    return employees.map(this::mapEntityToDto);
}
```

3. Actualizează Controller:
```java
@GetMapping("/active")
public ResponseEntity<Page<EmployeeDTO>> getActiveEmployees(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size) {
    return ResponseEntity.ok(employeeService.getActiveEmployees(page, size));
}
```

**Testează**:
```bash
curl "http://localhost:8080/api/employees/active?page=0&size=5"
```

**Ce vei învăța**: Pagination, Sorting, Query parameters

---

### Exercițiul 6: Adaugă Logging Personalizat

**Obiectiv**: Implementează logging pentru audit

**Task**: Creează un interceptor care loghează toate operațiunile

**Pași**:

1. Creează clasa `AuditInterceptor`:
```java
@Aspect
@Component
@Slf4j
public class AuditAspect {
    
    @Around("execution(* com.company.employeemanagement.service.*.*(..))")
    public Object logAudit(ProceedingJoinPoint joinPoint) throws Throwable {
        String methodName = joinPoint.getSignature().getName();
        String className = joinPoint.getTarget().getClass().getSimpleName();
        
        log.info("AUDIT: Calling {}.{}", className, methodName);
        long startTime = System.currentTimeMillis();
        
        Object result = joinPoint.proceed();
        
        long executionTime = System.currentTimeMillis() - startTime;
        log.info("AUDIT: {}.{} completed in {}ms", className, methodName, executionTime);
        
        return result;
    }
}
```

2. Adaugă dependency în pom.xml:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

**Ce vei învăța**: AOP, Logging, Performance monitoring

---

## 🚀 Nivel Advanced

### Exercițiul 7: Creează Stored Procedure Complexă

**Obiectiv**: Folosește PL/SQL pentru logică complexă

**Task**: Creează procedură pentru promovarea automată a angajatului

**Oracle PL/SQL**:
```sql
CREATE OR REPLACE PROCEDURE sp_promote_employee (
    p_employee_id IN NUMBER,
    p_new_job_id IN NUMBER,
    p_salary_increase_percent IN NUMBER DEFAULT 10
) AS
    v_current_salary NUMBER;
    v_new_salary NUMBER;
    v_max_salary NUMBER;
BEGIN
    -- Obține salariul curent
    SELECT salary INTO v_current_salary
    FROM employees
    WHERE employee_id = p_employee_id;
    
    -- Calculează noul salariu
    v_new_salary := v_current_salary * (1 + p_salary_increase_percent/100);
    
    -- Verifică maximul pentru noua funcție
    SELECT max_salary INTO v_max_salary
    FROM job_roles
    WHERE job_id = p_new_job_id;
    
    -- Validează
    IF v_new_salary > v_max_salary THEN
        v_new_salary := v_max_salary;
    END IF;
    
    -- Actualizează angajatul
    UPDATE employees
    SET job_id = p_new_job_id,
        salary = v_new_salary
    WHERE employee_id = p_employee_id;
    
    COMMIT;
    
    DBMS_OUTPUT.PUT_LINE('Employee promoted successfully. New salary: ' || v_new_salary);
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/
```

**Apelează din Java**:
```java
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {
    
    @Procedure(procedureName = "sp_promote_employee")
    void promoteEmployee(
        @Param("p_employee_id") Long employeeId,
        @Param("p_new_job_id") Long newJobId,
        @Param("p_salary_increase_percent") BigDecimal increasePercent
    );
}
```

**Ce vei învăța**: Stored procedures, Transaction management, PL/SQL

---

### Exercițiul 8: Implementează Soft Delete Complet

**Obiectiv**: Îmbunătățește mecanismul de soft delete

**Task**: Adaugă funcționalitate completă de soft delete cu audit

**Pași**:

1. Adaugă câmpuri în Entity:
```java
@Column(name = "DELETED_DATE")
private LocalDateTime deletedDate;

@Column(name = "DELETED_BY")
private String deletedBy;
```

2. Creează clasa `SoftDeleteListener`:
```java
@Component
public class SoftDeleteListener {
    
    @PreRemove
    public void preRemove(Employee employee) {
        employee.setIsActive(0);
        employee.setDeletedDate(LocalDateTime.now());
        // In real app, get from SecurityContext
        employee.setDeletedBy("SYSTEM");
    }
}
```

3. Adaugă filtrare globală:
```java
@Entity
@Table(name = "EMPLOYEES")
@Where(clause = "is_active = 1")
public class Employee { ... }
```

**Ce vei învăța**: Entity listeners, Soft delete patterns, Audit trails

---

### Exercițiul 9: Adaugă Caching

**Obiectiv**: Implementează caching pentru performanță

**Task**: Adaugă Redis cache pentru operațiuni read

**Pași**:

1. Adaugă dependencies:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

2. Enable caching:
```java
@SpringBootApplication
@EnableCaching
public class EmployeeManagementApplication { ... }
```

3. Adaugă anotări de cache:
```java
@Service
public class EmployeeService {
    
    @Cacheable(value = "employees", key = "#id")
    public EmployeeDTO getEmployeeById(Long id) { ... }
    
    @CacheEvict(value = "employees", key = "#id")
    public void deleteEmployee(Long id) { ... }
    
    @CachePut(value = "employees", key = "#result.employeeId")
    public EmployeeDTO updateEmployee(Long id, EmployeeDTO dto) { ... }
}
```

**Ce vei învăța**: Caching strategies, Redis, Performance optimization

---

### Exercițiul 10: Implementează API Versioning

**Obiectiv**: Suportă multiple versiuni de API

**Task**: Creează API v2 cu structură diferită

**Pași**:

1. Creează pachet nou: `controller.v2`

2. Creează DTO v2:
```java
public class EmployeeDTOV2 extends EmployeeDTO {
    private String address;
    private String emergencyContact;
    private List<String> skills;
}
```

3. Creează Controller v2:
```java
@RestController
@RequestMapping("/v2/employees")
public class EmployeeControllerV2 {
    // Implementare cu noul DTO
}
```

4. Sau folosește Header versioning:
```java
@GetMapping(value = "/employees/{id}", headers = "API-Version=2")
public ResponseEntity<EmployeeDTOV2> getEmployeeV2(@PathVariable Long id) { ... }
```

**Ce vei învăța**: API versioning strategies, Backward compatibility

---

## 🎓 Exerciții Bonus: Oracle DB

### Bonus 1: Creează un Trigger Complex

**Task**: Creează trigger care trimite notificare când salariul crește cu >20%

```sql
CREATE OR REPLACE TRIGGER trg_salary_change_notification
BEFORE UPDATE OF salary ON employees
FOR EACH ROW
DECLARE
    v_increase_percent NUMBER;
BEGIN
    IF :NEW.salary != :OLD.salary THEN
        v_increase_percent := ((:NEW.salary - :OLD.salary) / :OLD.salary) * 100;
        
        IF v_increase_percent > 20 THEN
            -- Log the notification (în practică ai trimite email/notificare)
            INSERT INTO salary_change_audit (
                employee_id,
                old_salary,
                new_salary,
                increase_percent,
                change_date
            ) VALUES (
                :NEW.employee_id,
                :OLD.salary,
                :NEW.salary,
                v_increase_percent,
                SYSDATE
            );
        END IF;
    END IF;
END;
/
```

---

### Bonus 2: Creează Raport Complex cu Analitice

**Task**: Raport cu statistici detaliate per departament

```sql
CREATE OR REPLACE VIEW vw_department_analytics AS
SELECT 
    d.department_id,
    d.department_name,
    d.location,
    COUNT(e.employee_id) as total_employees,
    COUNT(CASE WHEN e.is_active = 1 THEN 1 END) as active_employees,
    AVG(e.salary) as avg_salary,
    MIN(e.salary) as min_salary,
    MAX(e.salary) as max_salary,
    SUM(e.salary) as total_payroll,
    AVG(TRUNC(MONTHS_BETWEEN(SYSDATE, e.hire_date) / 12, 1)) as avg_tenure_years
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name, d.location;
```

---

## 📊 Checklist de Învățare

După ce finalizezi exercițiile, ar trebui să înțelegi:

### Java & Spring Boot
- [ ] Layered Architecture (Controller → Service → Repository)
- [ ] Dependency Injection cu Spring
- [ ] JPA Entities și Relationships
- [ ] Repository pattern cu Spring Data JPA
- [ ] Custom queries cu JPQL
- [ ] Data validation cu Jakarta Validation
- [ ] Exception handling centralizat
- [ ] REST API design
- [ ] DTO pattern
- [ ] Logging cu SLF4J

### Oracle Database
- [ ] DDL (CREATE TABLE, ALTER, DROP)
- [ ] DML (INSERT, UPDATE, DELETE, SELECT)
- [ ] Constraints (PK, FK, UNIQUE, CHECK)
- [ ] Sequences pentru auto-increment
- [ ] Indexes pentru performanță
- [ ] Views pentru raportare
- [ ] Stored Procedures
- [ ] Functions
- [ ] Triggers
- [ ] PL/SQL basics

### Best Practices
- [ ] Separarea concerns în layers
- [ ] DTO pentru transfer de date
- [ ] Validare la nivel de API
- [ ] Gestionarea erorilor
- [ ] Logging și monitoring
- [ ] Tranzacții database
- [ ] Soft delete pattern
- [ ] RESTful conventions

---

**Succes cu exercițiile! 🚀**
