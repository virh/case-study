package rh.virh.casestudy;

import org.openjdk.jmh.annotations.Benchmark;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class VolatileTest {

	private static final Logger logger = LoggerFactory.getLogger(VolatileTest.class);
	
	private volatile int counter;
	
	@Benchmark
	public void testVolatileReadBeforeWrite() {
		new Thread(new Runnable() {
			@Override
			public void run() {
				System.out.println("read........" + counter);
				try {
					Thread.sleep(1000);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				System.out.println("read........" + counter);
			}
		}).start();
		new Thread(new Runnable() {
			@Override
			public void run() {
				System.out.println("before write........" + counter);
				counter++;
				System.out.println("after write........" + counter);
			}
		}).start();
	}
	
	public static void main(String[] args) {
		new VolatileTest().testVolatileReadBeforeWrite();
	}
	
}
