package com.ranhfun.data.mybatisdemo.mapper;

import java.util.List;

import com.ranhfun.data.mybatisdemo.model.ValueInfo;

public interface ValueInfoMapper {

    public List < ValueInfo > findAll();

    public ValueInfo findById(long id);

    public int deleteById(long id);

    public int insert(ValueInfo valueInfo);

    public int update(ValueInfo valueInfo);
	
    public int deleteAll();
}
