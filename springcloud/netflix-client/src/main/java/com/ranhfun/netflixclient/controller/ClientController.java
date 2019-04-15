package com.ranhfun.netflixclient.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ClientController {

	@Autowired
	private ClientService clientService;
	
	@GetMapping("/test")
	public String test() {
		return clientService.test();
	}
	
}
