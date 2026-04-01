package com.company.employeemanagement.service;

import com.company.employeemanagement.dto.DepartmentDTO;
import com.company.employeemanagement.entity.Department;
import com.company.employeemanagement.exception.BusinessException;
import com.company.employeemanagement.exception.ResourceNotFoundException;
import com.company.employeemanagement.repository.DepartmentRepository;
import com.company.employeemanagement.repository.EmployeeRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Service pentru Department
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class DepartmentService {
    
    private final DepartmentRepository departmentRepository;
    private final EmployeeRepository employeeRepository;
    
    public DepartmentDTO createDepartment(DepartmentDTO departmentDTO) {
        log.info("Creating department: {}", departmentDTO.getDepartmentName());
        
        if (departmentRepository.existsByDepartmentName(departmentDTO.getDepartmentName())) {
            throw new BusinessException("Departamentul " + departmentDTO.getDepartmentName() + " există deja");
        }
        
        Department department = new Department();
        department.setDepartmentName(departmentDTO.getDepartmentName());
        department.setLocation(departmentDTO.getLocation());
        
        Department saved = departmentRepository.save(department);
        return mapEntityToDto(saved);
    }
    
    public DepartmentDTO updateDepartment(Long id, DepartmentDTO departmentDTO) {
        log.info("Updating department: {}", id);
        
        Department department = departmentRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Departamentul cu ID " + id + " nu a fost găsit"));
        
        if (!department.getDepartmentName().equals(departmentDTO.getDepartmentName()) &&
            departmentRepository.existsByDepartmentName(departmentDTO.getDepartmentName())) {
            throw new BusinessException("Departamentul " + departmentDTO.getDepartmentName() + " există deja");
        }
        
        department.setDepartmentName(departmentDTO.getDepartmentName());
        department.setLocation(departmentDTO.getLocation());
        
        Department updated = departmentRepository.save(department);
        return mapEntityToDto(updated);
    }
    
    @Transactional(readOnly = true)
    public DepartmentDTO getDepartmentById(Long id) {
        Department department = departmentRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Departamentul cu ID " + id + " nu a fost găsit"));
        return mapEntityToDto(department);
    }
    
    @Transactional(readOnly = true)
    public List<DepartmentDTO> getAllDepartments() {
        return departmentRepository.findAll().stream()
            .map(this::mapEntityToDto)
            .collect(Collectors.toList());
    }
    
    public void deleteDepartment(Long id) {
        Department department = departmentRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Departamentul cu ID " + id + " nu a fost găsit"));
        
        long employeeCount = employeeRepository.countByDepartment_DepartmentId(id);
        if (employeeCount > 0) {
            throw new BusinessException("Nu se poate șterge departamentul. Există " + employeeCount + " angajați asociați.");
        }
        
        departmentRepository.delete(department);
    }
    
    private DepartmentDTO mapEntityToDto(Department entity) {
        DepartmentDTO dto = new DepartmentDTO();
        dto.setDepartmentId(entity.getDepartmentId());
        dto.setDepartmentName(entity.getDepartmentName());
        dto.setLocation(entity.getLocation());
        
        long count = employeeRepository.countByDepartment_DepartmentId(entity.getDepartmentId());
        dto.setEmployeeCount((int) count);
        
        return dto;
    }
}
