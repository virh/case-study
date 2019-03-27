package jvm;

import junit.framework.Test;

public class Outer extends Inner {
	
	int test(int j, int z) {
		return (int) 1l;
	}
	
}

class Inner implements Tester {
	public int test(int i) {
		return 1;
	}
}

interface Tester {
	default int test(int i) {
		return 2;
	}
}

enum days {
	TEST {
		@Override
		String test() {
			// TODO Auto-generated method stub
			return null;
		}
	}, TEST2 {
		@Override
		String test() {
			// TODO Auto-generated method stub
			return null;
		}
	};
	
	abstract String test();
}