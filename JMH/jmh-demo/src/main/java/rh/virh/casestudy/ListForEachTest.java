package rh.virh.casestudy;

import java.util.ArrayList;
import java.util.List;
import java.util.OptionalInt;
import java.util.Random;
import java.util.stream.IntStream;

public class ListForEachTest {

	public static void main(String[] args) {
		List<Integer> l = new ArrayList<Integer>();
		for (int i = 0; i < 10; i++) {
			l.add(i);
		}
//		System.out.println("===============before forEach output===========");
//		l.forEach(i -> {
//			System.out.println(i);
//			try {
//				Thread.sleep(new Random().nextInt(1000));
//			} catch (InterruptedException e) {
//				// TODO Auto-generated catch block
//				e.printStackTrace();
//			}
//		});
//		System.out.println("===============after forEach output===========");
//		System.out.println("===============before stream forEach output===========");
//		l.parallelStream().forEach(i -> {
//			System.out.println(i);
//			try {
//				Thread.sleep(new Random().nextInt(1000));
//			} catch (InterruptedException e) {
//				// TODO Auto-generated catch block
//				e.printStackTrace();
//			}
//		});
//		System.out.println("===============after stream forEach output===========");
//		System.out.println("===============before IntStream range output===========");
//		IntStream.range(0, 10).forEach(i -> {
//			System.out.println(l.get(i));
//			try {
//				Thread.sleep(new Random().nextInt(1000));
//			} catch (InterruptedException e) {
//				// TODO Auto-generated catch block
//				e.printStackTrace();
//			}
//		});
//		System.out.println("===============after IntStream range output===========");
		OptionalInt indexOpt = IntStream.range(0, 10).reduce((left, right)-> {
			int leftValue = l.get(left);
			int rightValue = l.get(right);
			int greaterIndex = left;
			if (rightValue < leftValue) {
				greaterIndex = right;
			}
			return greaterIndex;
		});
		System.out.println(indexOpt.getAsInt());
	}
	
}
