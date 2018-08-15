package hello;

public class MyKey {
	  private String name;
	  private int id;
	 
	    public MyKey(int id, String name) {
	        this.id = id;
	        this.name = name;
	    }
	     
	    // standard getters and setters
	  
	    @Override
	    public int hashCode() {
	        System.out.println("Calling hashCode()");
	        return id;
	    } 
	  
	    // toString override for pretty logging
	 
	    @Override
	    public boolean equals(Object obj) {
	        System.out.println("Calling equals() for key: " + obj);
	        // generated implementation
	        MyKey that = (MyKey)obj;
	        return this.name.equals(that.name) && this.id==that.id;
	    }
}
