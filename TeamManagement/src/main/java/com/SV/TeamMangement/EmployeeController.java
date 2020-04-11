package com.SV.TeamMangement;

import org.springframework.web.bind.annotation.*;

import java.util.Collection;
import java.util.Optional;

@RestController
public class EmployeeController {
    private final EmployeeRepository dbRespository;


    public EmployeeController(EmployeeRepository dbRespository) {
        this.dbRespository = dbRespository;
    }
    @GetMapping("/EmployeeList")
    Collection<EmployeeEntity> all() {
        return dbRespository.findAll();
    }

    @GetMapping("/EmployeeList/{id}")
    Optional<EmployeeEntity> findbyId(@PathVariable long id) {
        return dbRespository.findById( id);
    }
    @PostMapping("/EmployeeList")
    EmployeeEntity newEmployee(@RequestBody EmployeeEntity newEmployee){
        return dbRespository.save(newEmployee);

    }
    @PutMapping("/EmployeeList/{id}")
    EmployeeEntity replaceEmployee(@RequestBody EmployeeEntity newEmployee, @PathVariable long id){
        return dbRespository.findById(id).map(EmployeeEntity->{
            EmployeeEntity.setName(newEmployee.getName());
            EmployeeEntity.setRole(newEmployee.getRole());
            EmployeeEntity.setDesignation(newEmployee.getDesignation());
            EmployeeEntity.setDob(newEmployee.getDob());
             return dbRespository.save(EmployeeEntity);
        })
                .orElseGet(() ->{
                    newEmployee.setId(id);
                    return dbRespository.save(newEmployee);
                });

    }
   @DeleteMapping("/EmployeeList/{id}")
   void deleteEmployee(@PathVariable long id){
        dbRespository.deleteById(id);
   }


}
