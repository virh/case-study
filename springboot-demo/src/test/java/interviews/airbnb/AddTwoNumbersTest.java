package interviews.airbnb;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class AddTwoNumbersTest {

	@Test
	public void testConditionSuccess() {
		ListNode node1 = new ListNode(2);
		node1.next = new ListNode(4);
		node1.next.next = new ListNode(3);
		
		ListNode node2 = new ListNode(5);
		node2.next = new ListNode(6);
		node2.next.next = new ListNode(4);
		
		AddTwoNumbers twoNumbers = new AddTwoNumbers();
		ListNode result = twoNumbers.addTwoNumbers(node1, node2);
		assertEquals(7, result.val);
		assertEquals(0, result.next.val);
		assertEquals(8, result.next.next.val);
	}
	
}
