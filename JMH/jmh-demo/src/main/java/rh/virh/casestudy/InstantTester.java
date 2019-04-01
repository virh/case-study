package rh.virh.casestudy;

import java.time.Instant;

public class InstantTester {

	public static void main(String[] args) {
		System.out.println(Instant.parse("2015-01-01T00:00:00Z").toEpochMilli());
		System.out.println(Instant.now().toEpochMilli());
	}
	
}
