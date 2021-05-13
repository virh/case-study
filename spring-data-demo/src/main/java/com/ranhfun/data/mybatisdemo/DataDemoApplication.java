package com.ranhfun.data.mybatisdemo;

import org.mybatis.spring.annotation.MapperScan;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import com.ranhfun.data.mybatisdemo.mapper.EmployeeMapper;
import com.ranhfun.data.mybatisdemo.mapper.ValueInfoMapper;
import com.ranhfun.data.mybatisdemo.model.Employee;
import com.ranhfun.data.mybatisdemo.model.ValueInfo;
import com.ranhfun.data.mybatisdemo.repository.EmployeeMyBatisRepository;
import com.ranhfun.data.mybatisdemo.service.ValueInfoService;

@SpringBootApplication
@EnableTransactionManagement
@MapperScan({"com.ranhfun.data.mybatisdemo.mapper", "com.ranhfun.data.mybatisdemo.repository"})
public class DataDemoApplication implements CommandLineRunner {

    private Logger logger = LoggerFactory.getLogger(this.getClass());

    @Autowired
    private EmployeeMyBatisRepository employeeRepository;
    
    @Autowired
    private EmployeeMapper employeeMapper;
    
    @Autowired
    private ValueInfoMapper valueInfoMapper;
	
    @Autowired
    private ValueInfoService valueInfoService;
    
	public static void main(String[] args) {
		SpringApplication.run(DataDemoApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {
//        logger.info("Inserting -> {}", employeeRepository.insert(new Employee(10011L, "Ramesh", "Fadatare", "ramesh@gmail.com")));
//        logger.info("Inserting -> {}", employeeRepository.insert(new Employee(10012L, "John", "Cena", "john@gmail.com")));
//        logger.info("Inserting -> {}", employeeRepository.insert(new Employee(10013L, "tony", "stark", "stark@gmail.com")));
//
//        logger.info("Employee id 10011 -> {}", employeeRepository.findById(10011L));
//
//        logger.info("Update 10003 -> {}", employeeRepository.update(new Employee(10011L, "ram", "Stark", "ramesh123@gmail.com")));
//
//        employeeRepository.deleteById(10013L);
//
//        logger.info("All users -> {}", employeeRepository.findAll());	
//        
//        employeeRepository.deleteAll();
//
//        logger.info("All users -> {}", employeeRepository.findAll());	
//        
//        // test for EmployeeMapper
//        
//        logger.info("Inserting -> {}", employeeMapper.insert(new Employee(10011L, "Ramesh", "Fadatare", "ramesh@gmail.com")));
//        logger.info("Inserting -> {}", employeeMapper.insert(new Employee(10012L, "John", "Cena", "john@gmail.com")));
//        logger.info("Inserting -> {}", employeeMapper.insert(new Employee(10013L, "tony", "stark", "stark@gmail.com")));
//
//        logger.info("Employee id 10011 -> {}", employeeMapper.findById(10011L));
//
//        logger.info("Update 10003 -> {}", employeeMapper.update(new Employee(10011L, "ram", "Stark", "ramesh123@gmail.com")));
//
//        employeeMapper.deleteById(10013L);
//
//        logger.info("All users -> {}", employeeMapper.findAll());	
//        
//        employeeMapper.deleteAll();
//
//        logger.info("All users -> {}", employeeMapper.findAll());
        
        ValueInfo valueInfo = new ValueInfo();
        valueInfo.setId(1);
        valueInfo.setValue(10);
        valueInfoMapper.insert(valueInfo);
        valueInfoService.testSelect(valueInfo.getId());
        valueInfoMapper.deleteAll();
	}

}
