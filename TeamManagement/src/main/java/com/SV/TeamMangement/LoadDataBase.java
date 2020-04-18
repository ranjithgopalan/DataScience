package com.SV.TeamMangement;


import jdk.nashorn.internal.runtime.logging.Logger;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
@Logger

public class LoadDataBase {
    @Bean
    CommandLineRunner initDatabase(EmployeeRepository dbRespository){
      return args -> {
         System.out.print("Preloading1" + dbRespository.save(new EmployeeEntity("Ranjith","Principal Consultant","Senior Manager","01-14-1978")));
          System.out.print("Preloading1" + dbRespository.save(new EmployeeEntity("Arath1","Principal Consultant","Manager","01-14-1981")));

      };
    }

}
