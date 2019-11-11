package rh.virh.casestudy;

import java.util.Date;
import java.util.TimeZone;

public class TimeZoneTest {

	public static void main(String[] args) {
		 System.out.println("Date in UTC: " + new Date().toString());
		 TimeZone.setDefault(TimeZone.getTimeZone("UTC"));

        System.out.println("Date in UTC: " + new Date().toString());
	}
	
}
