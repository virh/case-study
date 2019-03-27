package jvm;

public class ExceptionFlow {

	int testRetrun() {
		try {
			return 3;
		} finally {
			System.out.println("test return");
			return 4;
		}
	}
	
	public static void main(String[] args) throws Exception {
		try {
	          throw new Exception();
	      } catch (Exception e) {
	          System.out.print("Caught!");
	      } finally {
	          System.out.print("Finally!");
	      }
		System.out.println(new ExceptionFlow().testRetrun());
		System.out.println(2<<4);
	}
	
}
