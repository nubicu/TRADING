package com.company.employeemanagement.repository;

import com.company.employeemanagement.entity.JobRole;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

/**
 * Repository pentru JobRole
 */
@Repository
public interface JobRoleRepository extends JpaRepository<JobRole, Long> {
    
    Optional<JobRole> findByJobTitle(String jobTitle);
    
    boolean existsByJobTitle(String jobTitle);
}
