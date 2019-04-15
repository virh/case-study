package com.ranhfun.zipkin;

import java.util.logging.Logger;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
public class ZipkinApplication3 {

	public static void main(String[] args) {
		SpringApplication.run(ZipkinApplication3.class, args);
	}

}

class ZipkinController {

    @Autowired
    RestTemplate restTemplate;
 
    @Bean
    public RestTemplate getRestTemplate() {
        return new RestTemplate();
    }
 
    private static final Logger LOG = Logger.getLogger(ZipkinController.class.getName());
     
    @GetMapping(value="/zipkin3")
    public String zipkinService1()
    {
        LOG.info("Inside zipkinService 3..");
         
         String response = (String) restTemplate.exchange("http://localhost:8082/zipkin4",
                        HttpMethod.GET, null, new ParameterizedTypeReference<String>() {}).getBody();
        return "Hi...";
    }
	
}