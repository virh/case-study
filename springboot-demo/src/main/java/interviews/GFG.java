package interviews;

//Java program to explain the 
//concept of joining a thread. 
import java.io.*; 

//Java program to illustrate exec() 
//method of Runtime class 
public class GFG 
{ 
	public static void main(String[] args) 
	{ 
		try
		{ 
			// create a file with the working directory we wish 
			File f = new File("/home/saket/Desktop");
			f.mkdirs();
			
			// create a process and execute gedit and currect environment 
			Process process = Runtime.getRuntime().exec("notepad", null); 
			System.out.println("Gedit opening."); 
		} 
		catch (Exception e) 
		{ 
			e.printStackTrace(); 
		} 
	} 
} 



