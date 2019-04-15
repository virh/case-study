package com.ranhfun.secondservice.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SecondController {

	@RequestMapping("/")
	public String demo() {
		return "Second service";
	}
	
}
