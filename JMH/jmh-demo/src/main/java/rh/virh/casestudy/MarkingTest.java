package rh.virh.casestudy;

import java.util.ArrayList;
import java.util.List;

public class MarkingTest {
  // Execute this code with options:
  // -XX:+PrintGCApplicationStoppedTime - prints the time the application was stopped
  // -XX:+PrintSafepointStatistics - prints stats about safepoints
  // -Xmx300m - maximum heap size (in mb)
  // -XX:+PrintGCDetails - prints GC details
  // -XX:+PrintGCTimeStamps - prints GC time
  public static void main(String[] args) throws InterruptedException {
    long startTime = System.currentTimeMillis();
    int upperBound = 5800000;
    List<Worker> workers = new ArrayList<>();
    for (int i = 0; i < upperBound; i++) {
      Worker worker = new Worker();
      worker.setCurrentCompany(new Company());
      workers.add(worker);
    }
 
    // Now dereference the half of companies
    for (int i = 0; i < upperBound / 2; i++) {
      workers.get(i).setCurrentCompany(null);
    }
    long endTime = System.currentTimeMillis();
    System.out.println("Executed on " + (endTime - startTime) + " ms");
  }
 
  public static class Worker {
    private Company currentCompany;
 
    public Company getCurrentCompany() {
      return currentCompany;
    }
 
    public void setCurrentCompany(Company currentCompany) {
      this.currentCompany = currentCompany;
    }
  }
 
  public static class Company {
  }
}
