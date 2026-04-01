package com.company.employeemanagement;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Clasa principală a aplicației Employee Management System
 * 
 * Această aplicație oferă un sistem complet de management pentru angajați
 * folosind Spring Boot și Oracle Database.
 */
@SpringBootApplication
public class EmployeeManagementApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(EmployeeManagementApplication.class, args);
        System.out.println("\n========================================");
        System.out.println("Employee Management System Started!");
        System.out.println("API disponibil la: http://localhost:8080/api");
        System.out.println("========================================\n");
    }
}
