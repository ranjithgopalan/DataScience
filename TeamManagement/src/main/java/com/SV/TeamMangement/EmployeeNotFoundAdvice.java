package com.SV.TeamMangement;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@ControllerAdvice
public class EmployeeNotFoundAdvice {
    @ResponseBody
    @ExceptionHandler(EmployeeNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    String EmployeeNOTFoundHandler(EmployeeNotFoundException ex){
        return ex.getMessage();
    }
}
