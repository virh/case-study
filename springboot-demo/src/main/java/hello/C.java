package hello;

public class C extends B implements A {

	@Override
	public void setup() {
		super.setup();
	}

	public static void main(String[] args) {
		((A)(new C())).setup();
	}
	
}
