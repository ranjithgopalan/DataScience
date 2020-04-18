package com.SV.TeamMangement;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
@Entity
public class EmployeeEntity {

//    private String Employee;
    @Id @GeneratedValue(strategy= GenerationType.IDENTITY)

    private Long id;
    private String Name;
    private String Role;
    private String Designation;
    private String Dob;

    public EmployeeEntity() {
    }

    public EmployeeEntity(String name, String role, String designation, String dob) {


        Name = name;
        Role = role;
        Designation = designation;
        Dob = dob;
    }



    public void setId(Long id) {
        this.id = id;
    }

    public void setName(String name) {
        Name = name;
    }

    public void setRole(String role) {
        Role = role;
    }

    public void setDesignation(String designation) {
        Designation = designation;
    }

    public void setDob(String dob) {
        Dob = dob;
    }



    public String getName() {
        return Name;
    }

    public String getRole() {
        return Role;
    }

    public Long getId() {
        return id;
    }

    public String getDesignation() {
        return Designation;
    }

    public String getDob() {
        return Dob;
    }
}
