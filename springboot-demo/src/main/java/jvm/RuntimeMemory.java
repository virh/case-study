package jvm;

public class RuntimeMemory {
	public static void main(String[] a) {
	      java.io.PrintStream out = System.out;

	      // getting the Runtime instance of the JVM
	      Runtime rt = Runtime.getRuntime();

	      // obtaining basic information
	      out.println("# of processors: " + rt.availableProcessors());
	      out.println(" Maximum memory: " + rt.maxMemory());
	      out.println("   Total memory: " + rt.totalMemory());
	      out.println("    Free memory: " + rt.freeMemory());
	   }
}
