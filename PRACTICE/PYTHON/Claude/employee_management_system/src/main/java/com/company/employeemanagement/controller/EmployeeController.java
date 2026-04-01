package com.company.employeemanagement.controller;

import com.company.employeemanagement.dto.EmployeeDTO;
import com.company.employeemanagement.service.EmployeeService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;

/**
 * REST Controller pentru operațiuni cu angajați
 * Base URL: /api/employees
 */
@RestController
@RequestMapping("/employees")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "*") // Pentru dezvoltare - în producție setează origini specifice
public class EmployeeController {
    
    private final EmployeeService employeeService;
    
    /**
     * POST /api/employees - Creează un angajat nou
     */
    @PostMapping
    public ResponseEntity<EmployeeDTO> createEmployee(@Valid @RequestBody EmployeeDTO employeeDTO) {
        log.info("REST request to create employee: {}", employeeDTO.getEmail());
        EmployeeDTO created = employeeService.createEmployee(employeeDTO);
        return new ResponseEntity<>(created, HttpStatus.CREATED);
    }
    
    /**
     * PUT /api/employees/{id} - Actualizează un angajat
     */
    @PutMapping("/{id}")
    public ResponseEntity<EmployeeDTO> updateEmployee(
            @PathVariable Long id,
            @Valid @RequestBody EmployeeDTO employeeDTO) {
        log.info("REST request to update employee: {}", id);
        EmployeeDTO updated = employeeService.updateEmployee(id, employeeDTO);
        return ResponseEntity.ok(updated);
    }
    
    /**
     * GET /api/employees/{id} - Găsește un angajat după ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<EmployeeDTO> getEmployeeById(@PathVariable Long id) {
        log.info("REST request to get employee: {}", id);
        EmployeeDTO employee = employeeService.getEmployeeById(id);
        return ResponseEntity.ok(employee);
    }
    
    /**
     * GET /api/employees - Găsește toți angajații
     */
    @GetMapping
    public ResponseEntity<List<EmployeeDTO>> getAllEmployees() {
        log.info("REST request to get all employees");
        List<EmployeeDTO> employees = employeeService.getAllEmployees();
        return ResponseEntity.ok(employees);
    }
    
    /**
     * GET /api/employees/active - Găsește angajații activi
     */
    @GetMapping("/active")
    public ResponseEntity<List<EmployeeDTO>> getActiveEmployees() {
        log.info("REST request to get active employees");
        List<EmployeeDTO> employees = employeeService.getActiveEmployees();
        return ResponseEntity.ok(employees);
    }
    
    /**
     * DELETE /api/employees/{id} - Șterge (dezactivează) un angajat
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteEmployee(@PathVariable Long id) {
        log.info("REST request to delete employee: {}", id);
        employeeService.deleteEmployee(id);
        return ResponseEntity.noContent().build();
    }
    
    /**
     * GET /api/employees/department/{departmentId} - Găsește angajați după departament
     */
    @GetMapping("/department/{departmentId}")
    public ResponseEntity<List<EmployeeDTO>> getEmployeesByDepartment(@PathVariable Long departmentId) {
        log.info("REST request to get employees by department: {}", departmentId);
        List<EmployeeDTO> employees = employeeService.getEmployeesByDepartment(departmentId);
        return ResponseEntity.ok(employees);
    }
    
    /**
     * GET /api/employees/search?name=xyz - Caută angajați după nume
     */
    @GetMapping("/search")
    public ResponseEntity<List<EmployeeDTO>> searchEmployees(@RequestParam String name) {
        log.info("REST request to search employees by name: {}", name);
        List<EmployeeDTO> employees = employeeService.searchEmployeesByName(name);
        return ResponseEntity.ok(employees);
    }
    
    /**
     * PATCH /api/employees/{id}/salary - Actualizează salariul
     */
    @PatchMapping("/{id}/salary")
    public ResponseEntity<EmployeeDTO> updateSalary(
            @PathVariable Long id,
            @RequestBody SalaryUpdateRequest request) {
        log.info("REST request to update salary for employee: {}", id);
        EmployeeDTO updated = employeeService.updateSalary(id, request.getNewSalary());
        return ResponseEntity.ok(updated);
    }
    
    /**
     * Clasă helper pentru request-ul de actualizare salariu
     */
    public static class SalaryUpdateRequest {
        private BigDecimal newSalary;
        
        public BigDecimal getNewSalary() {
            return newSalary;
        }
        
        public void setNewSalary(BigDecimal newSalary) {
            this.newSalary = newSalary;
        }
    }
}
