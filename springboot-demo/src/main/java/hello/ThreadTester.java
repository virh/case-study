package hello;

public class ThreadTester {

	public static void main(String[] args) {
		System.out.println(Thread.currentThread().getName());
		new Thread("MyThread") {
			@Override
			public void run() {
				System.out.println(Thread.currentThread().getName());
			}
		}.run();
	}
	
}
