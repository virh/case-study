package jvm;

public class LongSleep {
	public static void main(String[] a) {
	      Runtime rt = Runtime.getRuntime();
	      System.out.println(" Free memory: " + rt.freeMemory());
	      System.out.println("Total memory: " + rt.totalMemory());
	      try {Thread.sleep(1000*60*60);} 
	      catch (InterruptedException e) {}
	   }
}
