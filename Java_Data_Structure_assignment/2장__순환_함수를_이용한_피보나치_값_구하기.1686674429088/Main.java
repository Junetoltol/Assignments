import java.util.Scanner;
import java.io.*;

class Main {
	// 피보나치 수열을 계산하는 아래 fib 메소드를 작성하시오.
public static long fib(int n) {
   if (n <= 1) {
      return n;
   }
   else {
      return fib(n-1) + fib(n-2);
   }
}
	// main 메소드는 수정하지 마시오.
	public static void main(String[] args) throws Exception {
		Scanner scan = new Scanner(System.in);
		int n = scan.nextInt();			// 데이터의 갯수 입력
		
		System.out.println(fib(n));
	}
}