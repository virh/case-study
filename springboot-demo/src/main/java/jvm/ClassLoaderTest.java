package jvm;

public class ClassLoaderTest {
	  public static void main(String[] a) {
	      java.io.PrintStream out = System.out;
	      Object o = null;
	      Class c = null;
	      ClassLoader l = null;

	      l = ClassLoader.getSystemClassLoader();
	      out.println("");
	      out.println("Built-in ClassLoaders");
	      out.println("System ClassLoader: "+l.getClass().getName());
	      l = l.getParent();
	      out.println("Extensions ClassLoader: "+l.getClass().getName());
	      l = l.getParent();
	      out.println("Bootstrap ClassLoader: "+l);

	      o = new java.lang.String();
	      c = o.getClass();
	      l = c.getClassLoader();
	      out.println("");
	      out.println("ClassLoader of java.lang.String: "+l);

	      try {
	         c = Class.forName("sun.security.pkcs11.P11Util");
	         l = c.getClassLoader();
	         out.println("");
	         out.println("ClassLoader of sun.security.pkcs11.P11Util: "
	            +l.getClass().getName());
	      } catch (Exception e) {
	      }

	      o = new ClassLoaderTest();
	      c = o.getClass();
	      l = c.getClassLoader();
	      out.println("");
	      out.println("ClassLoader of ClassLoaderTest: "
	         +l.getClass().getName());
	   }
}
