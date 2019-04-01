package interviews;

import java.util.BitSet;

public class BitTester {

	public static void main(String[] args) { 
		
	// declaring bitset 
	BitSet bset = new BitSet(6); 

	// assigning values to bset 
//	bset.set(0); 
//	bset.set(1); 
//	bset.set(2); 
//	bset.set(3); 

	// printing the original set 
	System.out.println("The original bitset is : " + bset); 

	// using flip(fromnum,tonum) to remove 1 and 2 
	bset.flip(0,6); 
		
	// printing final bitset 
	// 1 and 2 are removed 
	System.out.println("The flipped bitset is : " + bset); 
	} 
	
}
