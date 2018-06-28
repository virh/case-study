package hello;

import java.time.LocalDate;
import java.time.Period;

public class PeriodExample {

	public static void main(String[] args) {
		LocalDate startDate = LocalDate.of(2015, 2, 20);
		LocalDate endDate = LocalDate.of(2017, 1, 15);
		 
		Period period = Period.between(startDate, endDate);
		System.out.println("Years:" + period.getYears() + 
				  " months:" + period.getMonths() + 
				  " days:"+period.getDays());
		
		//System.out.println(period.plusDays(50).getDays());
		System.out.println(period.minusMonths(9).getMonths());
		
		System.out.println(7&4);
	}
	
}
