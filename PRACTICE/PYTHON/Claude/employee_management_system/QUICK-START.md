# 🚀 Quick Start Guide - Employee Management System

Ghid rapid pentru a porni aplicația în 5 minute!

## Prerequisites Check

Înainte de a începe, verifică că ai instalat:

```bash
# Verifică Java
java -version
# Trebuie să fie 17 sau mai nou

# Verifică Maven
mvn -version
# Trebuie să fie 3.6+ 

# Verifică Oracle DB
# Trebuie să ai acces la o instanță Oracle Database
```

## 🏃 Quick Setup (5 pași)

### Pasul 1: Setup Database (2 min)

1. Conectează-te la Oracle Database:
```bash
sqlplus username/password@localhost:1521/ORCL
```

2. Rulează scriptul de setup:
```sql
@database-setup.sql
```

✅ Aceasta va crea tabele, secvențe, triggere, proceduri și date de test.

### Pasul 2: Configure Connection (1 min)

Editează `src/main/resources/application.properties`:

```properties
spring.datasource.url=jdbc:oracle:thin:@localhost:1521:ORCL
spring.datasource.username=YOUR_USERNAME
spring.datasource.password=YOUR_PASSWORD
```

**Înlocuiește:**
- `YOUR_USERNAME` - username-ul tău Oracle
- `YOUR_PASSWORD` - parola ta Oracle
- `localhost:1521:ORCL` - dacă ai alt host/port/SID

### Pasul 3: Build Project (1 min)

```bash
# În directorul rădăcină al proiectului
mvn clean install
```

### Pasul 4: Run Application (30 sec)

```bash
mvn spring-boot:run
```

SAU, dacă ai un IDE:
- Importă ca proiect Maven
- Rulează clasa `EmployeeManagementApplication`

### Pasul 5: Test API (30 sec)

Deschide browser sau Postman și testează:

```
GET http://localhost:8080/api/employees
```

Ar trebui să vezi datele de test create în database!

## 🎯 First API Calls

### 1. Vezi toți angajații (date de test)

```bash
curl http://localhost:8080/api/employees
```

### 2. Vezi toate departamentele

```bash
curl http://localhost:8080/api/departments
```

### 3. Creează un angajat nou

```bash
curl -X POST http://localhost:8080/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Numele Tău",
    "lastName": "Prenumele Tău",
    "email": "tu@company.com",
    "phoneNumber": "0721234567",
    "hireDate": "2024-03-30",
    "salary": 8000,
    "jobId": 1,
    "departmentId": 1
  }'
```

## 📊 Verifică Datele în Database

Conectează-te la Oracle și rulează:

```sql
-- Vezi angajații
SELECT * FROM vw_employee_details;

-- Numără angajații per departament
SELECT 
    d.department_name,
    fn_count_employees_by_dept(d.department_id) as employee_count
FROM departments d;

-- Vezi toți angajații cu detalii
SELECT 
    e.employee_id,
    e.first_name || ' ' || e.last_name as full_name,
    j.job_title,
    d.department_name,
    e.salary
FROM employees e
LEFT JOIN job_roles j ON e.job_id = j.job_id
LEFT JOIN departments d ON e.department_id = d.department_id
WHERE e.is_active = 1;
```

## 🛠️ Troubleshooting

### Problema: "Cannot establish connection to database"

**Soluție:**
1. Verifică că Oracle DB rulează
2. Verifică credentials în `application.properties`
3. Testează conexiunea:
```bash
sqlplus username/password@localhost:1521/ORCL
```

### Problema: "Table or view does not exist"

**Soluție:**
1. Verifică că ai rulat `database-setup.sql`
2. Verifică schema corectă:
```sql
SELECT table_name FROM user_tables;
```

### Problema: "Port 8080 is already in use"

**Soluție:**
Schimbă portul în `application.properties`:
```properties
server.port=8081
```

### Problema: Maven build fails

**Soluție:**
```bash
# Curăță și rebuild
mvn clean
mvn install -DskipTests
```

## 📱 Testing Tools

### Option 1: cURL (Command Line)

Folosește exemplele din `API-TEST-EXAMPLES.md`

### Option 2: Postman

1. Descarcă [Postman](https://www.postman.com/downloads/)
2. Importează colecție de request-uri din `API-TEST-EXAMPLES.md`
3. Setează base URL: `http://localhost:8080/api`

### Option 3: Browser Extensions

- **REST Client** (VS Code)
- **Thunder Client** (VS Code)
- **Advanced REST Client**

## 🎓 Next Steps

Acum că aplicația rulează, poți:

1. **Explorează API-ul** - vezi toate endpoint-urile în README.md

2. **Studiază codul**:
   - Entities: `src/main/java/.../entity/`
   - Services: `src/main/java/.../service/`
   - Controllers: `src/main/java/.../controller/`

3. **Testează validările**:
   - Încearcă să creezi angajat cu email invalid
   - Încearcă să setezi salariu peste limită
   - Vezi exemplele din `API-TEST-EXAMPLES.md`

4. **Experimentează cu PL/SQL**:
   - Rulează proceduri stocate direct în Oracle
   - Modifică triggere
   - Creează funcții noi

5. **Extinde aplicația**:
   - Adaugă rapoarte
   - Implementează autentificare
   - Creează frontend

## 📚 Resurse Utile

- **README.md** - Documentație completă
- **API-TEST-EXAMPLES.md** - Exemple de request-uri
- **database-setup.sql** - Schema bazei de date
- [Spring Boot Docs](https://spring.io/projects/spring-boot)
- [Oracle PL/SQL Tutorial](https://www.oracletutorial.com/plsql-tutorial/)

## 🆘 Need Help?

Probleme frecvente și soluții:

| Problemă | Soluție |
|----------|---------|
| Connection refused | Verifică că DB rulează și credentials sunt corecte |
| Build errors | Rulează `mvn clean install` |
| Port conflict | Schimbă portul în application.properties |
| Table not found | Rulează din nou database-setup.sql |
| Validation errors | Verifică formatul datelor (email, telefon, etc.) |

---

**Succes cu învățarea Java și Oracle DB! 🎉**

**Timp estimat pentru setup complet: ~5 minute**
