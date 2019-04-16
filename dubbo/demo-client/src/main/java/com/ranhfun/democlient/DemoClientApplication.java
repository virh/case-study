package com.ranhfun.democlient;

import org.springframework.boot.SpringApplication;

import javax.annotation.PostConstruct;
import com.alibaba.dubbo.config.annotation.Reference;
import com.ranhfun.HelloService;

import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoClientApplication {

	@Reference(version = "1.0.0", url = "dubbo://localhost:20880")
  	private HelloService demoService;

	public static void main(String[] args) {
		
		SpringApplication.run(DemoClientApplication.class, args);
	}
	
    @PostConstruct
    public void init() {
    	String sayHello = demoService.sayHello("world");
    	System.err.println(sayHello);
    }
}
