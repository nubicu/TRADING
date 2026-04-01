package com.company.employeemanagement.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO pentru Department
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class DepartmentDTO {
    
    private Long departmentId;
    
    @NotBlank(message = "Numele departamentului este obligatoriu")
    @Size(min = 2, max = 100, message = "Numele trebuie să aibă între 2 și 100 de caractere")
    private String departmentName;
    
    @Size(max = 100, message = "Locația nu poate depăși 100 de caractere")
    private String location;
    
    private Integer employeeCount;
}
