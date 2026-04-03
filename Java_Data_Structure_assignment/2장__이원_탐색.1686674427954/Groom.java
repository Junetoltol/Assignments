public class Groom {
    // 여기에 binsearch 메소드를 작성하시오.
	public static int binsearch(int[] a, int key, int left, int right) {
        while(left<=right){
    int mid = (left+right)/2;
    if(a[mid]==key){
       return mid;
    }else if (a[mid]>key){
       right=mid-1;
    }else{
       left=mid +1;
    }
 }
      return -1;
  }
}

/*
업로드시 public class Groom{

}

해당 부분 지울것
*/