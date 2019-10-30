package rh.virh.casestudy;

import java.util.concurrent.ArrayBlockingQueue;

public class QueueTest {

	public static void main(String[] args) {
		ArrayBlockingQueue<Integer> q = new ArrayBlockingQueue<>(10);
		for (int i = 0; i < 10; i++) {
			q.add(i);
		}
		pop(q);
		System.out.println(q.size());
		q.forEach(i -> System.out.println("origin " +i));
	}
	
	static void pop(ArrayBlockingQueue<Integer> q) {
		int i = q.size();
		while(i-- > 0) {
			Integer value = q.poll();
			q.add(value);
			System.out.println("read " + value);
			System.out.println(i);
		}
	}
	
}
