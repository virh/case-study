package rh.virh.casestudy;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class OldGenerationRun {
	// -XX:+AlwaysTenure
	// remove -XX:+AlwaysTenure
	// -Xmx300m - maximum heap size (in mb)
	// -XX:+PrintGCDetails - prints GC details
	// -XX:+PrintGCTimeStamps - prints GC time
	public static void main(String[] args) {
		long expectedEnd = System.currentTimeMillis() + 5000;
		Map<Integer, List<Integer>> container = new HashMap<>();
		for (int j = 0; j < 200_000; j++) {
			container.put(j, new ArrayList<>());
		}
		int i = 0;
		while (System.currentTimeMillis() < expectedEnd) {
			if (i == 20_000) {
				i = 0;
			}
			container.put(i, new ArrayList<>());
			for (int j = 0; j < 20_000; j++) {
				container.get(i).add(j);
			}
			i++;
		}
	}
}
