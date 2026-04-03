import java.io.*;
import java.util.Scanner;

class ListNode {
	String data;
	ListNode rlink;
	ListNode llink;
}

class DoubleLinkedList {
	private ListNode head; // 리스트의 첫번째 노드를 가리킴
	private ListNode tail; // 리스트의 마지막 노드를 가리킴

	public DoubleLinkedList() {
		head = tail = null; // 리스트가 비어있을 때는 모두 null 이다.
	}

	/**
	 * 리스트는 이름순으로 정렬되므로 정렬된 적절한 위치에 삽입한다.
	 * @param str 삽입하고자 하는 데이터
	 * 작성하여야 한다.
	 */
   public void insert(String data) {
      ListNode newNode = new ListNode();
      newNode.data = data;
      newNode.llink = null;
      newNode.rlink = null;

      if (head == null) {
         head = tail = newNode;
         return;
      }

      ListNode p = head;
      while (p != null && p.data.compareTo(data) < 0) {
         p = p.rlink;
      }

      if (p == null) {
         newNode.llink = tail;
         tail.rlink = newNode;
         tail = newNode;
      } else {
         if (p.llink == null) {
            newNode.rlink = p;
            p.llink = newNode;
            head = newNode;
         } else {
            newNode.rlink = p;
            newNode.llink = p.llink;
            p.llink.rlink = newNode;
            p.llink = newNode;
         }
      }
   }

	/**
	 * 인자로 입력받은 데이터를 삭제한다.
	 * @param str 삭제하고자 하는 데이터
	 * 작성하여야 한다.
	 */
   public void delete(String data) {
      if (head == null) {
         System.out.println("EMPTY");
         return;
      }

      ListNode p = head;
      while (p != null && !p.data.equals(data)) {
         p = p.rlink;
      }

      if (p == null) {
         System.out.println("NONE");
         return;
      }

      if (p.llink == null && p.rlink == null) {
         head = tail = null;
      } else if (p.llink == null) {
         head = p.rlink;
         head.llink = null;
      } else if (p.rlink == null) {
         tail = p.llink;
         tail.rlink = null;
      } else {
         p.llink.rlink = p.rlink;
         p.rlink.llink = p.llink;
      }
   }

   public void display() {
      if (head == null) {
         System.out.println("EMPTY");
         return;
      }

      ListNode p = head;
      while (p != null) {
         System.out.print(p.data + " ");
         p = p.rlink;
      }
      System.out.println();
   }


	// 저장된 모든 데이터를 출력한다.
	public void print() {
		if (head == null) {
			System.out.println("EMPTY");
			return;
		}

		for(ListNode p = head; p != null; p = p.rlink)
			System.out.print(p.data + " ");
		System.out.println();
	}
}

class Main {
	
	// main 메소드는 수정하지 마시오.
	public static void main(String[] args) throws Exception {
		Scanner scan = new Scanner(System.in);
		
		DoubleLinkedList list = new DoubleLinkedList();
	
		while (true) {
			String cmd = scan.next();
			if (cmd.equals("E"))
				break;

			if (cmd.equals("I")) {
				list.insert(scan.next());
			} else if (cmd.equals("D")) {
				list.delete(scan.next());
			} else if (cmd.equals("P")) {
				list.print();
			} else {
				System.out.println("ERROR");
			}
		}
	}
}