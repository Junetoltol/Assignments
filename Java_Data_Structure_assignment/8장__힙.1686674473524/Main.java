import java.io.*;
import java.util.Scanner;

class MaxHeap {
      
   private int size = 0;   // MaxHeap에 저장된 데이터 갯수. p.336에서는 변수 n으로 표현
   private int[] heap; // MaxHeap
   
   /**
    * @param capacity 힙 배열의 크기
    */
   public MaxHeap(int capacity) {
      heap = new int[capacity + 1];
   }
   
   public void print() {
      for(int i = 1; i <= size; i++)
         System.out.print(heap[i] + " ");
      System.out.println();
   }
   
   // 아래 2개의 메소드(insert, delete)를 작성하시오.
   
   /**
    * 교재 p.336 참조
    * @param x 삭입하고자 하는 데이터
    */
   public void insert(int x) {
int i = ++size;
      
      while (i != 1 && x > heap[i / 2]) {
         heap[i] = heap[i / 2];
         i /= 2;
      }
      
      heap[i] = x;
   }
   
   /**
    * 교재 p.338 참조
    * MaxHeap에서 최대값을 삭제하고 그 같은 반환한다.
    * @return 최대값 출력
    */
   public int delete() {
      int deletedValue = heap[1];
      int temp = heap[size--];
      
      int parent = 1;
      int child = 2;
      
      while (child <= size) {
         // choose bigger child
         if (child < size && heap[child] < heap[child + 1]) {
            child++;
         }
         
         if (temp >= heap[child]) break;
         
         heap[parent] = heap[child];
         parent = child;
         child *= 2;
      }
      
      heap[parent] = temp;
      return deletedValue;
   }
}
class Main {
   
   // 아래 main 메소드는 수정하지 마시오.
   public static void main(String[] args) throws Exception {
      Scanner scan = new Scanner(System.in);
      MaxHeap heap = new MaxHeap(100);
      
      while (scan.hasNext()) {
         String command = scan.next();
         
         if (command.equals("I")) {
            int data = Integer.parseInt(scan.next());
            heap.insert(data);
         } else if (command.equals("D")) {
            heap.delete();
         } else if (command.equals("P")) {
            heap.print();
         } else if (command.equals("E")) {
            break;
         }
      }
      scan.close();
   }
   
}