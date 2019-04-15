package com.ranhfun.netflixservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@EnableDiscoveryClient
@SpringBootApplication
public class NetflixServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(NetflixServiceApplication.class, args);
	}
}
