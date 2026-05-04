import java.io.*;

class Queue {
	private String[] data;
	private static final int QUEUE_SIZE = 5;
	
	private int head = 0;
	private int tail = 0;

	public Queue() {
		data = new String[QUEUE_SIZE];
	}

	// 작성하시오.
	public void enque(String str) {
		if ((tail + 1) % QUEUE_SIZE == head) {
			throw new RuntimeException("Must not be full when enqueueing");
		}
		data[tail] = str;
		tail = (tail + 1) % QUEUE_SIZE;
	}

	// 작성하시오.	
	public String deque() {
		if (head == tail) {
			throw new RuntimeException("Must not be empty when dequeueing");
		}
		String result = data[head];
		head = (head + 1) % QUEUE_SIZE;
		return result;
	}
	
	// 작성하시오.
	public void print() {
    for (int f = head; f != tail; f = (f + 1) % QUEUE_SIZE) {
      System.out.println(data[f]);
    }
	}
}
class Main {
  public static void main(String[] args) throws Exception {
    Queue queue = new Queue();
		
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    String input = br.readLine();
    int no = Integer.parseInt(input);
		
    for(int i = 0; i < no; i++) {
      String cmd = br.readLine();
		
      if (cmd.equals("enque")) {
        String name = br.readLine();
        queue.enque(name);
      } else if (cmd.equals("deque")) {
        System.out.println(queue.deque());
      } else {
        throw new IllegalArgumentException();
      }
    }
		
    br.close();
  }
}
