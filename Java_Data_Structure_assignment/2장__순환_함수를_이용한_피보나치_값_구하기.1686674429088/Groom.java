public class Groom {
    // 피보나치 수열을 계산하는 아래 fib 메소드를 작성하시오.
	public static long fib(int n) {
		if (n <= 1) {
      return n;
   }
   else {
      return fib(n-1) + fib(n-2);
   }
	}

}

/*
업로드시 public class Groom{

}

해당 부분 지울것
*/
