package com.company.employeemanagement.controller;

import com.company.employeemanagement.dto.JobRoleDTO;
import com.company.employeemanagement.service.JobRoleService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST Controller pentru operațiuni cu funcții/roluri
 * Base URL: /api/job-roles
 */
@RestController
@RequestMapping("/job-roles")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "*")
public class JobRoleController {
    
    private final JobRoleService jobRoleService;
    
    /**
     * POST /api/job-roles - Creează o funcție nouă
     */
    @PostMapping
    public ResponseEntity<JobRoleDTO> createJobRole(@Valid @RequestBody JobRoleDTO jobRoleDTO) {
        log.info("REST request to create job role: {}", jobRoleDTO.getJobTitle());
        JobRoleDTO created = jobRoleService.createJobRole(jobRoleDTO);
        return new ResponseEntity<>(created, HttpStatus.CREATED);
    }
    
    /**
     * PUT /api/job-roles/{id} - Actualizează o funcție
     */
    @PutMapping("/{id}")
    public ResponseEntity<JobRoleDTO> updateJobRole(
            @PathVariable Long id,
            @Valid @RequestBody JobRoleDTO jobRoleDTO) {
        log.info("REST request to update job role: {}", id);
        JobRoleDTO updated = jobRoleService.updateJobRole(id, jobRoleDTO);
        return ResponseEntity.ok(updated);
    }
    
    /**
     * GET /api/job-roles/{id} - Găsește o funcție după ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<JobRoleDTO> getJobRoleById(@PathVariable Long id) {
        log.info("REST request to get job role: {}", id);
        JobRoleDTO jobRole = jobRoleService.getJobRoleById(id);
        return ResponseEntity.ok(jobRole);
    }
    
    /**
     * GET /api/job-roles - Găsește toate funcțiile
     */
    @GetMapping
    public ResponseEntity<List<JobRoleDTO>> getAllJobRoles() {
        log.info("REST request to get all job roles");
        List<JobRoleDTO> jobRoles = jobRoleService.getAllJobRoles();
        return ResponseEntity.ok(jobRoles);
    }
    
    /**
     * DELETE /api/job-roles/{id} - Șterge o funcție
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteJobRole(@PathVariable Long id) {
        log.info("REST request to delete job role: {}", id);
        jobRoleService.deleteJobRole(id);
        return ResponseEntity.noContent().build();
    }
}
