import java.io.*;
import java.util.Scanner;
class Polynomial {
	private int[][] term;
	private int curNoTerm = 0;

	// @param noTerm 항의 개수
	public Polynomial(int noTerm) {
		term = new int[noTerm][2];
	}

	public Polynomial() {
		this(20);  // default로 최대 20개의 항을 저장함
	}

	/**
	 * @param coef 계수
   * @param exp 지수
	 */
	public void addTerm(int coef, int exp) {
		term[curNoTerm][0] = exp;      //
		term[curNoTerm][1] = coef;
		curNoTerm++;
	}

	// @param exp
	// 작성하시오
	public void delTerm(int exp) {
      // term 배열에서 exp와 일치하는 지수를 찾아 삭제하는 코드를 작성
      for (int i = 0; i < curNoTerm; i++) {
         if (term[i][0] ==exp) {
            // 찾은 지수 이후의 모든 항을 한 칸씩 앞으로 옮겨줌
            for (int j = i; j <curNoTerm -1; j++) {
               term[j][0] = term[j+1][0];
               term[j][1] = term[j+1][1];
            }
            curNoTerm--;
            break;
         }
      }
	}

	/**
	 * 출력할 때 사용
	 * @return 객체를 문자열로 반환 (예: 3x^15+2x^3+4x^2+x+5 )
	 * 작성하시오.
	 */
	public String toString() {
      String result = "";
      for (int i =0; i <curNoTerm; i++) {
         int coef = term[i][1];
         int exp = term[i][0];
         if (coef == 0) continue;
         if (i != 0 && coef > 0) result += "+";
         if (coef != 1 && coef !=-1 || exp == 0) result += coef;
         if (exp != 0) result += "x";
         if (exp != 0 && exp != 1) result += "^" +exp;
      }
      if (result.equals("")) result = "0";
      return result;
	}

	/**
	 * 두 개의 다항식을 더한다.
	 * @param p1 첫번째 다항식
	 * @param p2 두번째 다항식
	 * @return 두 개의 다항식을 더한 결과
	 * 작성할 것 
	 */
	public static Polynomial polyAdd(Polynomial p1, Polynomial p2) {
      Polynomial result = new Polynomial(p1.curNoTerm + p2.curNoTerm);
    int i = 0, j = 0, k = 0;
    while (i < p1.curNoTerm && j < p2.curNoTerm) {
        if (p1.term[i][0] == p2.term[j][0]) { // 지수가 같으면 두 계수를 더함
            int sum = p1.term[i][1] + p2.term[j][1];
            if (sum != 0) { // 더한 결과가 0이 아니면 새로운 항을 추가
                result.term[k][0] = p1.term[i][0];
                result.term[k][1] = sum;
                k++;
            }
            i++;
            j++;
        } else if (p1.term[i][0] > p2.term[j][0]) { // p1의 지수가 더 크면 p1의 항을 추가
            result.term[k][0] = p1.term[i][0];
            result.term[k][1] = p1.term[i][1];
            i++;
            k++;
        } else { // p2의 지수가 더 크면 p2의 항을 추가
            result.term[k][0] = p2.term[j][0];
            result.term[k][1] = p2.term[j][1];
            j++;
            k++;
        }
    }
    // 남은 항들을 추가
    while (i < p1.curNoTerm) {
        result.term[k][0] = p1.term[i][0];
        result.term[k][1] = p1.term[i][1];
        i++;
        k++;
    }
    while (j < p2.curNoTerm) {
        result.term[k][0] = p2.term[j][0];
        result.term[k][1] = p2.term[j][1];
        j++;
        k++;
    }
    // 결과 다항식의 curNoTerm을 업데이트
    result.curNoTerm = k;
    return result;
	}
}

class Main {
	
	public static void main(String[] args) throws Exception {
		Scanner scan = new Scanner(System.in);

		// 첫번째 다항식 입력
		Polynomial p1 = new Polynomial();
		int no = scan.nextInt();
		for(int i = 0; i < no; i++) {
			int coef = scan.nextInt();
			int exp  = scan.nextInt();
			p1.addTerm(coef, exp);
		}


		Polynomial p2 = new Polynomial();
 // 두번째 다항식 입력 코드 여기에 작성할 것
   int no2 = scan.nextInt();
   for(int i =0; i <no2; i++) {
      int coef = scan.nextInt();
      int exp = scan.nextInt();
      p2.addTerm(coef, exp);
   }
		// 두개의 다항식 덧셈
		Polynomial p3 = Polynomial.polyAdd(p1, p2);

		System.out.print(p3);  // 이것은 System.out.print(p3.toString())과 동일
	}
}