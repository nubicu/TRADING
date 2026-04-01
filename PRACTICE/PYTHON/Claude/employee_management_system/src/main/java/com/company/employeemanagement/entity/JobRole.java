package com.company.employeemanagement.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Entitatea JobRole reprezintă o funcție/rol în companie
 */
@Entity
@Table(name = "JOB_ROLES")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class JobRole {
    
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "job_seq")
    @SequenceGenerator(name = "job_seq", sequenceName = "JOB_SEQ", allocationSize = 1)
    @Column(name = "JOB_ID")
    private Long jobId;
    
    @Column(name = "JOB_TITLE", nullable = false, unique = true, length = 100)
    private String jobTitle;
    
    @Column(name = "MIN_SALARY", precision = 10, scale = 2)
    private BigDecimal minSalary;
    
    @Column(name = "MAX_SALARY", precision = 10, scale = 2)
    private BigDecimal maxSalary;
    
    @Column(name = "CREATED_DATE", nullable = false, updatable = false)
    private LocalDateTime createdDate;
    
    // Relație One-to-Many cu Employee
    @OneToMany(mappedBy = "jobRole", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Employee> employees;
    
    @PrePersist
    protected void onCreate() {
        createdDate = LocalDateTime.now();
    }
}
