package com.company.employeemanagement.repository;

import com.company.employeemanagement.entity.Employee;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

/**
 * Repository pentru Employee - oferă metode pentru operațiuni CRUD
 */
@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {
    
    // Găsește angajați după email
    Optional<Employee> findByEmail(String email);
    
    // Găsește angajați activi
    List<Employee> findByIsActive(Integer isActive);
    
    // Găsește angajați după departament
    List<Employee> findByDepartment_DepartmentId(Long departmentId);
    
    // Găsește angajați după funcție
    List<Employee> findByJobRole_JobId(Long jobId);
    
    // Găsește subordonații unui manager
    List<Employee> findByManager_EmployeeId(Long managerId);
    
    // Căutare după nume sau prenume
    @Query("SELECT e FROM Employee e WHERE " +
           "LOWER(e.firstName) LIKE LOWER(CONCAT('%', :searchTerm, '%')) OR " +
           "LOWER(e.lastName) LIKE LOWER(CONCAT('%', :searchTerm, '%'))")
    List<Employee> searchByName(@Param("searchTerm") String searchTerm);
    
    // Găsește angajați cu salariu în interval
    @Query("SELECT e FROM Employee e WHERE e.salary BETWEEN :minSalary AND :maxSalary")
    List<Employee> findBySalaryRange(@Param("minSalary") java.math.BigDecimal minSalary, 
                                     @Param("maxSalary") java.math.BigDecimal maxSalary);
    
    // Verifică dacă email-ul există deja
    boolean existsByEmail(String email);
    
    // Numără angajații dintr-un departament
    long countByDepartment_DepartmentId(Long departmentId);
}
