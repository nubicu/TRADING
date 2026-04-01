package com.company.employeemanagement.exception;

/**
 * Excepție pentru erori de logică de business
 */
public class BusinessException extends RuntimeException {
    
    public BusinessException(String message) {
        super(message);
    }
    
    public BusinessException(String message, Throwable cause) {
        super(message, cause);
    }
}
