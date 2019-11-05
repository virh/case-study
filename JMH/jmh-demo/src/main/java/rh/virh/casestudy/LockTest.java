package rh.virh.casestudy;

public class LockTest {

	public static void main(String[] args) {
		Lock lock = new Lock();
		new Thread() {
			public void run() {
				try {
					lock.lock();
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				lock.unlock();
			};
		}.start();
		new Thread() {
			public void run() {
				try {
					lock.lock();
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				lock.unlock();
			};
		}.start();
	}
	
}

class Lock {
	
	boolean isLocked = false;
	
	synchronized void lock() throws InterruptedException {
		while(isLocked) {
			wait();
		}
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println("lock...");
		isLocked = true;
	}
	
	synchronized void unlock() {
		notify();
		isLocked = false;
		System.out.println("unlock...");
	}
}
