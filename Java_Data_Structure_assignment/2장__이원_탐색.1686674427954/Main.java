import java.util.Scanner;
import java.io.*;

class Main {
	// 여기에 binsearch 메소드를 작성하시오.
public static int binsearch(int[] arr, int key, int left, int right) {
   while(left<=right){
      int mid = (left+right)/2;
      if(arr[mid]==key){
         return mid;
      }else if (arr[mid]>key){
         right=mid-1;
      }else{
         left=mid +1;
      }
   }
   
   return -1;
}

	
	// main 메소드는 수정하지 마시오.
	public static void main(String[] args) throws Exception {
		Scanner scan = new Scanner(System.in);
		
		int no = scan.nextInt();			// 데이터의 갯수 입력
		int[] arr = new int[no];		// 데이터를 저장할 배열 생성
		
		// 데이터 입력
		for(int i = 0; i < no; i++)
			arr[i] = scan.nextInt();
		
		// 찾고자 하는 값
		int key = scan.nextInt();

		int idx = binsearch(arr, key, 0, no - 1);
		System.out.println(idx);
	}
}