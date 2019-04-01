package interviews;

import java.io.IOException;

public class JavaExceptionPropagation {

	public static void main(String args[]){
		JavaExceptionPropagation obj=new JavaExceptionPropagation();
		obj.method1();
		System.out.println("Normal code execution flow continues...");
	}

	void method1(){
		try{
			method2();
		} catch(Exception e){
			System.out.println("Exception handling is done here");
		}
	}

	void method2() throws IOException{
		method3();
	}

	void method3() throws IOException{
		throw new java.io.IOException("Some IO Exception..");
	}
}
