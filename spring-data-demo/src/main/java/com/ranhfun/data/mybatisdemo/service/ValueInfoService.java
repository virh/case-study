package com.ranhfun.data.mybatisdemo.service;

import java.util.stream.IntStream;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.ranhfun.data.mybatisdemo.mapper.ValueInfoMapper;
import com.ranhfun.data.mybatisdemo.model.ValueInfo;

@Service
public class ValueInfoService {

	private Logger logger = LoggerFactory.getLogger(this.getClass());
	
	@Autowired
	ValueInfoMapper valueInfoMapper;
	
	//@Transactional
	public void testSelect(long id) {
		IntStream.range(0, 3).forEach(i-> {
			ValueInfo valueInfo = valueInfoMapper.findById(id);
			logger.info("ValueInfo current value -> {}", valueInfo.getValue());
			valueInfo.setValue(valueInfo.getValue()-2);
			valueInfoMapper.update(valueInfo);
		});
	}
	
}
