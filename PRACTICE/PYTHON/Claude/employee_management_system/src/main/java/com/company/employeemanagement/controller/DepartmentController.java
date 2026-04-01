package com.company.employeemanagement.controller;

import com.company.employeemanagement.dto.DepartmentDTO;
import com.company.employeemanagement.service.DepartmentService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST Controller pentru operațiuni cu departamente
 * Base URL: /api/departments
 */
@RestController
@RequestMapping("/departments")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "*")
public class DepartmentController {
    
    private final DepartmentService departmentService;
    
    /**
     * POST /api/departments - Creează un departament nou
     */
    @PostMapping
    public ResponseEntity<DepartmentDTO> createDepartment(@Valid @RequestBody DepartmentDTO departmentDTO) {
        log.info("REST request to create department: {}", departmentDTO.getDepartmentName());
        DepartmentDTO created = departmentService.createDepartment(departmentDTO);
        return new ResponseEntity<>(created, HttpStatus.CREATED);
    }
    
    /**
     * PUT /api/departments/{id} - Actualizează un departament
     */
    @PutMapping("/{id}")
    public ResponseEntity<DepartmentDTO> updateDepartment(
            @PathVariable Long id,
            @Valid @RequestBody DepartmentDTO departmentDTO) {
        log.info("REST request to update department: {}", id);
        DepartmentDTO updated = departmentService.updateDepartment(id, departmentDTO);
        return ResponseEntity.ok(updated);
    }
    
    /**
     * GET /api/departments/{id} - Găsește un departament după ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<DepartmentDTO> getDepartmentById(@PathVariable Long id) {
        log.info("REST request to get department: {}", id);
        DepartmentDTO department = departmentService.getDepartmentById(id);
        return ResponseEntity.ok(department);
    }
    
    /**
     * GET /api/departments - Găsește toate departamentele
     */
    @GetMapping
    public ResponseEntity<List<DepartmentDTO>> getAllDepartments() {
        log.info("REST request to get all departments");
        List<DepartmentDTO> departments = departmentService.getAllDepartments();
        return ResponseEntity.ok(departments);
    }
    
    /**
     * DELETE /api/departments/{id} - Șterge un departament
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteDepartment(@PathVariable Long id) {
        log.info("REST request to delete department: {}", id);
        departmentService.deleteDepartment(id);
        return ResponseEntity.noContent().build();
    }
}
