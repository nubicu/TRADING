package com.company.employeemanagement.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Entitatea Employee reprezintă un angajat din companie
 */
@Entity
@Table(name = "EMPLOYEES")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Employee {
    
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "emp_seq")
    @SequenceGenerator(name = "emp_seq", sequenceName = "EMP_SEQ", allocationSize = 1)
    @Column(name = "EMPLOYEE_ID")
    private Long employeeId;
    
    @Column(name = "FIRST_NAME", nullable = false, length = 50)
    private String firstName;
    
    @Column(name = "LAST_NAME", nullable = false, length = 50)
    private String lastName;
    
    @Column(name = "EMAIL", nullable = false, unique = true, length = 100)
    private String email;
    
    @Column(name = "PHONE_NUMBER", length = 20)
    private String phoneNumber;
    
    @Column(name = "HIRE_DATE", nullable = false)
    private LocalDate hireDate;
    
    @Column(name = "SALARY", nullable = false, precision = 10, scale = 2)
    private BigDecimal salary;
    
    @Column(name = "IS_ACTIVE")
    private Integer isActive = 1;
    
    @Column(name = "CREATED_DATE", nullable = false, updatable = false)
    private LocalDateTime createdDate;
    
    @Column(name = "UPDATED_DATE")
    private LocalDateTime updatedDate;
    
    // Relație Many-to-One cu JobRole
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "JOB_ID", nullable = false)
    private JobRole jobRole;
    
    // Relație Many-to-One cu Department
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "DEPARTMENT_ID")
    private Department department;
    
    // Relație self-referencing pentru manager
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "MANAGER_ID")
    private Employee manager;
    
    // Relație One-to-Many pentru subordonați
    @OneToMany(mappedBy = "manager", fetch = FetchType.LAZY)
    private List<Employee> subordinates;
    
    @PrePersist
    protected void onCreate() {
        createdDate = LocalDateTime.now();
        updatedDate = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedDate = LocalDateTime.now();
    }
    
    // Metode helper
    public String getFullName() {
        return firstName + " " + lastName;
    }
    
    public boolean isActive() {
        return isActive != null && isActive == 1;
    }
}
