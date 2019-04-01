package interviews;

public class Sub extends Super {

	public Sub() {
		// TODO Auto-generated constructor stub
	}
	
	public void Sub() {
		System.out.println();
	}
	
	@Override
	String test() {
		// TODO Auto-generated method stub
		return null;
	}
	
	public Long getLength(Long t) {
		return new Long(5);
	}
	
	public static void main(String[] args) {
		System.out.println(4&7);
		 int ia [][] = new int[][]{{4, 5, 6},{1, 2, 3}};
		 byte i = 0;
		 switch (i) {
		case 1:
			
			break;

		default:
			break;
		}
		 new Thread().start();
	}
	
}

abstract class Super {
	
	abstract String test();
	
	public Integer getLength() {
		return new Integer(4);
	}
	
}
