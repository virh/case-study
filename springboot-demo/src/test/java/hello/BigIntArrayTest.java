package hello;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.concurrent.CountDownLatch;

public class BigIntArrayTest {

	public static void main(String[] args) throws InterruptedException, IOException, URISyntaxException {
		int mb = 1024*1024;
		Runtime  runtime = Runtime.getRuntime();
		List<String> allLines = Files.readAllLines(Paths.get(BigIntArrayTest.class.getResource("../data/area.txt").toURI()));
		System.gc();
		long preMemory = runtime.freeMemory();
		int[] areas = new int[700000];
		String[] names = new String[500];
		allLines.forEach(line -> {
			String[] items = line.split("\\s+");
			int areaIndex = Integer.parseInt(items[1]);
			areas[1999999-Integer.parseInt(items[0])] = areaIndex;
			names[areaIndex] = items[2];
		});
		allLines = null;
		long afterMemory = runtime.freeMemory();
		System.out.println(preMemory-afterMemory);
		CountDownLatch latch = new CountDownLatch(1);
		System.gc();
		afterMemory = runtime.freeMemory();
		System.out.println((preMemory-afterMemory)/mb);
		latch.await();
	}
	
}
