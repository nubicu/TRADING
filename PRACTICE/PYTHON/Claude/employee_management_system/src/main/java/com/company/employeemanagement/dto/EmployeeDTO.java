package com.company.employeemanagement.dto;

import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * DTO pentru Employee - folosit pentru transferul de date între client și server
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class EmployeeDTO {
    
    private Long employeeId;
    
    @NotBlank(message = "Prenumele este obligatoriu")
    @Size(min = 2, max = 50, message = "Prenumele trebuie să aibă între 2 și 50 de caractere")
    private String firstName;
    
    @NotBlank(message = "Numele este obligatoriu")
    @Size(min = 2, max = 50, message = "Numele trebuie să aibă între 2 și 50 de caractere")
    private String lastName;
    
    @NotBlank(message = "Email-ul este obligatoriu")
    @Email(message = "Email-ul nu este valid")
    private String email;
    
    @Pattern(regexp = "^(\\+4|0)[0-9]{9}$", message = "Numărul de telefon nu este valid (ex: 0721234567)")
    private String phoneNumber;
    
    @NotNull(message = "Data angajării este obligatorie")
    @PastOrPresent(message = "Data angajării nu poate fi în viitor")
    private LocalDate hireDate;
    
    @NotNull(message = "Salariul este obligatoriu")
    @DecimalMin(value = "0.0", inclusive = false, message = "Salariul trebuie să fie pozitiv")
    private BigDecimal salary;
    
    @NotNull(message = "ID-ul funcției este obligatoriu")
    private Long jobId;
    
    private Long departmentId;
    
    private Long managerId;
    
    private Integer isActive;
    
    // Câmpuri pentru afișare (nu pentru input)
    private String jobTitle;
    private String departmentName;
    private String managerName;
    private String fullName;
    
    public String getFullName() {
        return firstName + " " + lastName;
    }
}
