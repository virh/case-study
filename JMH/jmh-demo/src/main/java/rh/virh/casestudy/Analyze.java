package rh.virh.casestudy;

import java.util.Scanner;

public class Analyze<AnyType> {
	private int x;
	
	void test() {
		AnyType[] objs = (AnyType[])new Object[5];
	}

	   public static void main(String[] args)
	   {
	      Analyze tmp = new Analyze();
	      System.out.println(tmp.x);
	      new Scope().method();
	      
	      int n = Integer.parseInt(args[0]);
	      double sum = 0.0;
	      Scanner scanner = new Scanner(System.in); //it's defined in java.util

	      for(int k = 0; k < n; k++)
	      	sum += scanner.nextInt();

	      System.out.println("Average = " + sum/n);
	   }
}
class Scope
{
   private int x;

   public Scope () {x = 0;}

   public void method()
   {
      int x = 1;
      System.out.print( this.x );
   }
}