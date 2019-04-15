package com.ranhfun.netflixclient.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.netflix.appinfo.InstanceInfo;
import com.netflix.discovery.EurekaClient;
import com.netflix.hystrix.contrib.javanica.annotation.HystrixCommand;

@Service
public class ClientService {

	@Autowired
	private EurekaClient eurekaClient;
	
	@HystrixCommand(fallbackMethod = "failed")
	public String test() {
		InstanceInfo instanceInfo = eurekaClient.getNextServerFromEureka("netflix-service", false);
		String serviceBaseUrl = instanceInfo.getHomePageUrl();
		String result = new RestTemplate().getForObject(serviceBaseUrl + "demo", String.class);
		return result;
	}
	
	public String failed() {
		return "failed";
	}
}
