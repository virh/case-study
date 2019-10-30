package rh.virh.casestudy;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;

public class SerializationDemo {
	public static void main(String[] args) throws ClassNotFoundException, IOException
	   {
	      ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("output.ser"));

	      out.writeObject("Pittsburgh");

	      out.writeObject(new int[]{1,2,3});

	      ArrayList<String>  tmp = new ArrayList<String>();
	      tmp.add("00");
	      tmp.add("01");
	      out.writeObject(tmp);

	      out.close();



	      ObjectInputStream in = new ObjectInputStream(new FileInputStream("output.ser"));

	      String cl = (String) in.readObject();
	      System.out.println(cl);

	      in.readObject();

	      ArrayList al = (ArrayList) in.readObject();
	      System.out.println(al);

	      in.close();
	   }
}
