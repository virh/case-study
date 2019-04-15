package com.ranhfun.springcloudconfigclient.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RefreshScope
@RestController
public class DemoController {

	@Value("${test.property}")
	private String testProperty;
	
	@Value("${test.local.property}")
	private String localTestProperty;
	
	@Autowired
	private PropertyConfiguration propertyConfiguration;
	
	@RequestMapping("/")
	public String test() {
		StringBuilder  builder = new StringBuilder();
		builder.append("test property - ").append(testProperty).append(" ")
			.append("local property - ").append(localTestProperty)
			.append("property configuration value - ").append(propertyConfiguration.getProperty());
		return builder.toString();
	}
	
}
