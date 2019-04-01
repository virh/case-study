package interviews;

import java.io.IOException;

public class Outer /*implements Tester*/{
	
	private int i = 3;
	
	public void someOuterMethod() {
		// Line 3
		int j = 3;
		String work = "out.local.work";
		class Inner {
			int z =0;
			
			public void eat() {
				System.out.println(i);
				System.out.println(j);
				System.out.println(work);
			}
		}
		new Inner().eat();
	}

	public static void main(String[] argv) {
		Outer o = new Outer();
		// Line 8
		try {
			o.someOuterMethod();
			System.exit(-1);
		} finally {
			System.out.println("Finnal");
		}
		
	}

//	@Override
//	public void methoda() {
//		// TODO Auto-generated method stub
//		
//	}
//
//	@Override
//	public double methodb(int i) {
//		// TODO Auto-generated method stub
//		return 0;
//	}
//
//	@Override
//	public double methodb(float j) throws RuntimeException {
//		// TODO Auto-generated method stub
//		return 0;
//	}

}

//interface Tester {
//	void methoda();
//
//	public double methodb(int i);
//	
//	public double methodb(float j) throws IOException;
//
//	static void methodac(double d1) {
//	};
//}