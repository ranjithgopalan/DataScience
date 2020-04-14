package Ranjith.Appus;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@EnableAutoConfiguration

@SpringBootApplication
public class ImageProcessingApplication extends SpringBootServletInitializer {
	@RequestMapping("/YourName")
	String home() {
		return "Ranjith";
	}
	public static void main(String[] args) {
		SpringApplication.run(ImageProcessingApplication.class, args);
	}

}