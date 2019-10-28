package rh.virh.casestudy;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.PriorityQueue;
import java.util.stream.IntStream;

public class PriorityQueueTest {

	public static void main(String[] args) {
		List<User> users = new ArrayList<>();
		for (int i = 0; i < 5; i++) {
			users.add(new User("user" + i));
		}
		PriorityQueue<User> queue = new PriorityQueue<>();
		users.forEach(user -> {
			try {
				queue.add(user.clone());
			} catch (CloneNotSupportedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		});
		queue.forEach(user-> {
			System.out.println(user.name);
		});
		queue.forEach(user-> {
			System.out.println(user.name);
		});
//		queue.stream().filter(user->!user.getName().equals("user3")).forEach(user-> {
//			System.out.println(user.name);
//		});
		Iterator<User> iterator = queue.iterator();
		IntStream.range(0, 2).forEach(index -> {
			System.out.println(iterator.next().name);
		});
	}
	
}

class User implements Comparable<User>, Cloneable {
	String name;
	public User() {
	}
	public User(String name) {
		this.name = name;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	@Override
	public int compareTo(User o) {
		return this.name.compareTo(o.name);
	}
	
	@Override
	protected User clone() throws CloneNotSupportedException {
		User user = (User) super.clone();
		user.name = this.name;
		return user;
	}
	
}