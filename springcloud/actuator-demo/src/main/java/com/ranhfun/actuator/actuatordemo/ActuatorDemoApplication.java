package com.ranhfun.actuator.actuatordemo;

import java.util.Date;
import java.util.TimeZone;

import javax.annotation.PostConstruct;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.ImportAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@ImportAutoConfiguration(classes = ActuatorSecurityConfig.class)
@SpringBootApplication
public class ActuatorDemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(ActuatorDemoApplication.class, args);
	}
	
    @PostConstruct
    public void init(){
      // Setting Spring Boot SetTimeZone
      System.out.println("Date in before UTC: " + new Date().toString());
      TimeZone.setDefault(TimeZone.getTimeZone("UTC"));
      System.out.println("Date in after UTC: " + new Date().toString());
    }

}
