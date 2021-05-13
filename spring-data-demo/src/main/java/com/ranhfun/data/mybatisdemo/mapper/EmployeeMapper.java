package com.ranhfun.data.mybatisdemo.mapper;

import java.util.List;

import com.ranhfun.data.mybatisdemo.model.Employee;

public interface EmployeeMapper {

    public List < Employee > findAll();

    public Employee findById(long id);

    public int deleteById(long id);

    public int insert(Employee employee);

    public int update(Employee employee);
	
    public int deleteAll();
}
