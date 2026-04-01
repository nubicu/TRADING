package com.company.employeemanagement.service;

import com.company.employeemanagement.dto.EmployeeDTO;
import com.company.employeemanagement.entity.Department;
import com.company.employeemanagement.entity.Employee;
import com.company.employeemanagement.entity.JobRole;
import com.company.employeemanagement.exception.ResourceNotFoundException;
import com.company.employeemanagement.exception.BusinessException;
import com.company.employeemanagement.repository.DepartmentRepository;
import com.company.employeemanagement.repository.EmployeeRepository;
import com.company.employeemanagement.repository.JobRoleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Service pentru Employee - conține logica de business
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class EmployeeService {
    
    private final EmployeeRepository employeeRepository;
    private final DepartmentRepository departmentRepository;
    private final JobRoleRepository jobRoleRepository;
    
    /**
     * Creează un angajat nou
     */
    public EmployeeDTO createEmployee(EmployeeDTO employeeDTO) {
        log.info("Creating employee: {} {}", employeeDTO.getFirstName(), employeeDTO.getLastName());
        
        // Verifică dacă email-ul există deja
        if (employeeRepository.existsByEmail(employeeDTO.getEmail())) {
            throw new BusinessException("Email-ul " + employeeDTO.getEmail() + " este deja folosit");
        }
        
        Employee employee = new Employee();
        mapDtoToEntity(employeeDTO, employee);
        
        // Validează salariul față de limitele funcției
        validateSalary(employee.getJobRole(), employeeDTO.getSalary());
        
        Employee savedEmployee = employeeRepository.save(employee);
        log.info("Employee created successfully with ID: {}", savedEmployee.getEmployeeId());
        
        return mapEntityToDto(savedEmployee);
    }
    
    /**
     * Actualizează un angajat existent
     */
    public EmployeeDTO updateEmployee(Long id, EmployeeDTO employeeDTO) {
        log.info("Updating employee with ID: {}", id);
        
        Employee employee = employeeRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Angajatul cu ID " + id + " nu a fost găsit"));
        
        // Verifică dacă email-ul este schimbat și dacă noul email există deja
        if (!employee.getEmail().equals(employeeDTO.getEmail()) && 
            employeeRepository.existsByEmail(employeeDTO.getEmail())) {
            throw new BusinessException("Email-ul " + employeeDTO.getEmail() + " este deja folosit");
        }
        
        mapDtoToEntity(employeeDTO, employee);
        
        // Validează salariul față de limitele funcției
        validateSalary(employee.getJobRole(), employeeDTO.getSalary());
        
        Employee updatedEmployee = employeeRepository.save(employee);
        log.info("Employee updated successfully: {}", id);
        
        return mapEntityToDto(updatedEmployee);
    }
    
    /**
     * Găsește un angajat după ID
     */
    @Transactional(readOnly = true)
    public EmployeeDTO getEmployeeById(Long id) {
        log.info("Fetching employee with ID: {}", id);
        
        Employee employee = employeeRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Angajatul cu ID " + id + " nu a fost găsit"));
        
        return mapEntityToDto(employee);
    }
    
    /**
     * Găsește toți angajații
     */
    @Transactional(readOnly = true)
    public List<EmployeeDTO> getAllEmployees() {
        log.info("Fetching all employees");
        
        return employeeRepository.findAll().stream()
            .map(this::mapEntityToDto)
            .collect(Collectors.toList());
    }
    
    /**
     * Găsește angajați activi
     */
    @Transactional(readOnly = true)
    public List<EmployeeDTO> getActiveEmployees() {
        log.info("Fetching active employees");
        
        return employeeRepository.findByIsActive(1).stream()
            .map(this::mapEntityToDto)
            .collect(Collectors.toList());
    }
    
    /**
     * Șterge un angajat (soft delete)
     */
    public void deleteEmployee(Long id) {
        log.info("Deleting employee with ID: {}", id);
        
        Employee employee = employeeRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Angajatul cu ID " + id + " nu a fost găsit"));
        
        employee.setIsActive(0);
        employeeRepository.save(employee);
        
        log.info("Employee deactivated successfully: {}", id);
    }
    
    /**
     * Găsește angajați după departament
     */
    @Transactional(readOnly = true)
    public List<EmployeeDTO> getEmployeesByDepartment(Long departmentId) {
        log.info("Fetching employees for department: {}", departmentId);
        
        return employeeRepository.findByDepartment_DepartmentId(departmentId).stream()
            .map(this::mapEntityToDto)
            .collect(Collectors.toList());
    }
    
    /**
     * Caută angajați după nume
     */
    @Transactional(readOnly = true)
    public List<EmployeeDTO> searchEmployeesByName(String searchTerm) {
        log.info("Searching employees by name: {}", searchTerm);
        
        return employeeRepository.searchByName(searchTerm).stream()
            .map(this::mapEntityToDto)
            .collect(Collectors.toList());
    }
    
    /**
     * Actualizează salariul unui angajat
     */
    public EmployeeDTO updateSalary(Long id, BigDecimal newSalary) {
        log.info("Updating salary for employee: {}", id);
        
        Employee employee = employeeRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Angajatul cu ID " + id + " nu a fost găsit"));
        
        validateSalary(employee.getJobRole(), newSalary);
        
        employee.setSalary(newSalary);
        Employee updatedEmployee = employeeRepository.save(employee);
        
        log.info("Salary updated successfully for employee: {}", id);
        return mapEntityToDto(updatedEmployee);
    }
    
    // ===== METODE HELPER =====
    
    private void validateSalary(JobRole jobRole, BigDecimal salary) {
        if (jobRole.getMinSalary() != null && salary.compareTo(jobRole.getMinSalary()) < 0) {
            throw new BusinessException("Salariul este sub minimul permis pentru funcție: " + 
                                       jobRole.getMinSalary());
        }
        
        if (jobRole.getMaxSalary() != null && salary.compareTo(jobRole.getMaxSalary()) > 0) {
            throw new BusinessException("Salariul depășește maximul permis pentru funcție: " + 
                                       jobRole.getMaxSalary());
        }
    }
    
    private void mapDtoToEntity(EmployeeDTO dto, Employee entity) {
        entity.setFirstName(dto.getFirstName());
        entity.setLastName(dto.getLastName());
        entity.setEmail(dto.getEmail());
        entity.setPhoneNumber(dto.getPhoneNumber());
        entity.setHireDate(dto.getHireDate());
        entity.setSalary(dto.getSalary());
        entity.setIsActive(dto.getIsActive() != null ? dto.getIsActive() : 1);
        
        // Set JobRole
        JobRole jobRole = jobRoleRepository.findById(dto.getJobId())
            .orElseThrow(() -> new ResourceNotFoundException("Funcția cu ID " + dto.getJobId() + " nu a fost găsită"));
        entity.setJobRole(jobRole);
        
        // Set Department (optional)
        if (dto.getDepartmentId() != null) {
            Department department = departmentRepository.findById(dto.getDepartmentId())
                .orElseThrow(() -> new ResourceNotFoundException("Departamentul cu ID " + dto.getDepartmentId() + " nu a fost găsit"));
            entity.setDepartment(department);
        }
        
        // Set Manager (optional)
        if (dto.getManagerId() != null) {
            Employee manager = employeeRepository.findById(dto.getManagerId())
                .orElseThrow(() -> new ResourceNotFoundException("Managerul cu ID " + dto.getManagerId() + " nu a fost găsit"));
            entity.setManager(manager);
        }
    }
    
    private EmployeeDTO mapEntityToDto(Employee entity) {
        EmployeeDTO dto = new EmployeeDTO();
        dto.setEmployeeId(entity.getEmployeeId());
        dto.setFirstName(entity.getFirstName());
        dto.setLastName(entity.getLastName());
        dto.setEmail(entity.getEmail());
        dto.setPhoneNumber(entity.getPhoneNumber());
        dto.setHireDate(entity.getHireDate());
        dto.setSalary(entity.getSalary());
        dto.setIsActive(entity.getIsActive());
        dto.setFullName(entity.getFullName());
        
        if (entity.getJobRole() != null) {
            dto.setJobId(entity.getJobRole().getJobId());
            dto.setJobTitle(entity.getJobRole().getJobTitle());
        }
        
        if (entity.getDepartment() != null) {
            dto.setDepartmentId(entity.getDepartment().getDepartmentId());
            dto.setDepartmentName(entity.getDepartment().getDepartmentName());
        }
        
        if (entity.getManager() != null) {
            dto.setManagerId(entity.getManager().getEmployeeId());
            dto.setManagerName(entity.getManager().getFullName());
        }
        
        return dto;
    }
}
