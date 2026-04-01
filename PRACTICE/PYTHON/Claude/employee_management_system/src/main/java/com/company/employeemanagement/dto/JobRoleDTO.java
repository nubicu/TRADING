package com.company.employeemanagement.dto;

import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;

/**
 * DTO pentru JobRole
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class JobRoleDTO {
    
    private Long jobId;
    
    @NotBlank(message = "Titlul funcției este obligatoriu")
    @Size(min = 2, max = 100, message = "Titlul trebuie să aibă între 2 și 100 de caractere")
    private String jobTitle;
    
    @DecimalMin(value = "0.0", inclusive = false, message = "Salariul minim trebuie să fie pozitiv")
    private BigDecimal minSalary;
    
    @DecimalMin(value = "0.0", inclusive = false, message = "Salariul maxim trebuie să fie pozitiv")
    private BigDecimal maxSalary;
    
    private Integer employeeCount;
}
