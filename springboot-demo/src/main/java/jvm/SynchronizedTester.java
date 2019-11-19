package jvm;

public class SynchronizedTester {

	public SynchronizedTester() {
		int i = 1_000_000_100;
		System.out.println(i/100*10);
		System.out.println("empty");
	}
	
	public SynchronizedTester(String test1, int test2) {
		System.out.println(test1 + " " + test2);
	}
	
	public void test1() {
		synchronized (this) {
			System.out.println("test1");
		}
	}
	
	public synchronized void test2() {
		System.out.println("test2");
	}
	
	public static void main(String[] args) {
		new SynchronizedTester();
		Parent  parent = new Parent();
		Child child = new Child();
		parent = child;
		child = (Child)parent;
	}
	
}


class Parent {
	
}

class Child extends Parent {
	
}