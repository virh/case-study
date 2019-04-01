package jvm;

public class RuntimeShutdown {
	public static void main(String[] a) {
	      java.io.PrintStream out = System.out;
	      Runtime rt = Runtime.getRuntime();
	      String opt = a[0];

	      out.println("Adding a shutdown hook...");
	      rt.addShutdownHook(new MyShutdownHook());

	      if (opt.equals("exit")) {
	         out.println("Asking JVM to shutdown...");
	         rt.exit(0);
	      } else if (opt.equals("halt")) {
	         out.println("Asking JVM to terminate...");
	         rt.halt(0);
	      } else {
	         out.println("Putting the application to sleep...");
	         try {Thread.sleep(1000*60*60);} 
	         catch (InterruptedException e) {}
	      }
	   }
	   public static class MyShutdownHook extends Thread {
	      public void run() {
	         System.out.println("Running my shutdown hook...");
	      }
	   }
}
