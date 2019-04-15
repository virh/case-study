package com.ranhfun.firstservice.controller;

import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FirstController {

	@RequestMapping("/")
	public String demo(@RequestHeader("X-source") String source) {
		return "First service with" + source;
	}
	
}
