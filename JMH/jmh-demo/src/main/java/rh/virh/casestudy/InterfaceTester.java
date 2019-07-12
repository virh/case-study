package rh.virh.casestudy;

public class InterfaceTester implements T1, T2 {

	@Override
	public void method1() {
		T1.super.method1();
		T2.super.method1();
	}

	public static void main(String[] args) {
		InterfaceTester tester = new InterfaceTester();
		tester.method1();
		T1 t1 = tester;
		t1.method1();
		T2 t2 = tester;
		t2.method1();
	}
	
}

interface T1 {
	default void method1() {
		System.out.println("T1");
	};
}

interface T2 {
	default void method1() {
		System.out.println("T2");
	}
}
