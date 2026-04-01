package com.company.employeemanagement.service;

import com.company.employeemanagement.dto.JobRoleDTO;
import com.company.employeemanagement.entity.JobRole;
import com.company.employeemanagement.exception.BusinessException;
import com.company.employeemanagement.exception.ResourceNotFoundException;
import com.company.employeemanagement.repository.JobRoleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Service pentru JobRole
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class JobRoleService {
    
    private final JobRoleRepository jobRoleRepository;
    
    public JobRoleDTO createJobRole(JobRoleDTO jobRoleDTO) {
        log.info("Creating job role: {}", jobRoleDTO.getJobTitle());
        
        if (jobRoleRepository.existsByJobTitle(jobRoleDTO.getJobTitle())) {
            throw new BusinessException("Funcția " + jobRoleDTO.getJobTitle() + " există deja");
        }
        
        if (jobRoleDTO.getMinSalary() != null && jobRoleDTO.getMaxSalary() != null &&
            jobRoleDTO.getMinSalary().compareTo(jobRoleDTO.getMaxSalary()) > 0) {
            throw new BusinessException("Salariul minim nu poate fi mai mare decât salariul maxim");
        }
        
        JobRole jobRole = new JobRole();
        jobRole.setJobTitle(jobRoleDTO.getJobTitle());
        jobRole.setMinSalary(jobRoleDTO.getMinSalary());
        jobRole.setMaxSalary(jobRoleDTO.getMaxSalary());
        
        JobRole saved = jobRoleRepository.save(jobRole);
        return mapEntityToDto(saved);
    }
    
    public JobRoleDTO updateJobRole(Long id, JobRoleDTO jobRoleDTO) {
        log.info("Updating job role: {}", id);
        
        JobRole jobRole = jobRoleRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Funcția cu ID " + id + " nu a fost găsită"));
        
        if (!jobRole.getJobTitle().equals(jobRoleDTO.getJobTitle()) &&
            jobRoleRepository.existsByJobTitle(jobRoleDTO.getJobTitle())) {
            throw new BusinessException("Funcția " + jobRoleDTO.getJobTitle() + " există deja");
        }
        
        if (jobRoleDTO.getMinSalary() != null && jobRoleDTO.getMaxSalary() != null &&
            jobRoleDTO.getMinSalary().compareTo(jobRoleDTO.getMaxSalary()) > 0) {
            throw new BusinessException("Salariul minim nu poate fi mai mare decât salariul maxim");
        }
        
        jobRole.setJobTitle(jobRoleDTO.getJobTitle());
        jobRole.setMinSalary(jobRoleDTO.getMinSalary());
        jobRole.setMaxSalary(jobRoleDTO.getMaxSalary());
        
        JobRole updated = jobRoleRepository.save(jobRole);
        return mapEntityToDto(updated);
    }
    
    @Transactional(readOnly = true)
    public JobRoleDTO getJobRoleById(Long id) {
        JobRole jobRole = jobRoleRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Funcția cu ID " + id + " nu a fost găsită"));
        return mapEntityToDto(jobRole);
    }
    
    @Transactional(readOnly = true)
    public List<JobRoleDTO> getAllJobRoles() {
        return jobRoleRepository.findAll().stream()
            .map(this::mapEntityToDto)
            .collect(Collectors.toList());
    }
    
    public void deleteJobRole(Long id) {
        JobRole jobRole = jobRoleRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Funcția cu ID " + id + " nu a fost găsită"));
        
        if (jobRole.getEmployees() != null && !jobRole.getEmployees().isEmpty()) {
            throw new BusinessException("Nu se poate șterge funcția. Există angajați asociați.");
        }
        
        jobRoleRepository.delete(jobRole);
    }
    
    private JobRoleDTO mapEntityToDto(JobRole entity) {
        JobRoleDTO dto = new JobRoleDTO();
        dto.setJobId(entity.getJobId());
        dto.setJobTitle(entity.getJobTitle());
        dto.setMinSalary(entity.getMinSalary());
        dto.setMaxSalary(entity.getMaxSalary());
        
        if (entity.getEmployees() != null) {
            dto.setEmployeeCount(entity.getEmployees().size());
        }
        
        return dto;
    }
}
