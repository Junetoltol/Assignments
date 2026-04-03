import java.io.*;
import java.util.Scanner;

class Polynomial {

	/**
	 * 클래스 내부에 클래스를 만드는 경우를 예로 든 것이다.
	 * 이렇게 할 경우 클래스 Term은 Polynomial 클래스 내에서만
	 * 의미가 있다는 것을 알 수 있다.
	 */
	class Term {
		int coef;
		int exp;
		Term link;
	}

	private Term head;  // 첫번째 항을 가리키는 레퍼런스 변수
	private Term tail;  // 마지막 항을 가리키는 레퍼런스 변수

	public Polynomial() {
		head = tail = null; // 원래 객체의 인스턴스 필드는 null로 초기화되지만 이해를 위해 초기화함
	}

	/**
	 * @param coef 계수
	 * @param exp 지수
	 */
	public void addTerm(int coef, int exp) {
		Term term = new Term();
		term.coef = coef;
		term.exp = exp;
		term.link = null;
	
		if (head == null) {  // 처음으로 항이 추가되는 경우
			head = tail = term;
		} else {
			tail.link = term;
			tail = term;  // 마지막을 가리키는 항을 재지정
		}
	}



	/**
	 * 출력할 때 사용
	 * @return 객체를 문자열로 반환 (예: 3x^15+2x^3+4x^2+x+5 )
	 * 메소드를 완성하시오.
	 */
public String toString() {
   if (head == null) {
      return "0";
   }
   
   StringBuilder sb = new StringBuilder();
   Term term = head;
   while (term != null) {
      if (term.coef != 0) {
         if (term.coef > 0 && sb.length() > 0) {
            sb.append("+");
         }
         if (term.coef != 1 || term.exp ==0)
         sb.append(term.coef);
         if (term.exp !=0) {
            sb.append("x");
            if (term.exp !=1) {
               sb.append("^").append(term.exp);
            }
         }
      }
      term =term.link;
   }
   return sb.toString();
}
	/**
	 * 두 개의 다항식을 더한다.
	 * @param p1 첫번째 다항식
	 * @param p2 두번째 다항식
	 * @return 두 개의 다항식을 더한 결과
	 * 메소드를 완성하시오. 
	 */


public static Polynomial polyAdd(Polynomial p1, Polynomial p2) {
   Polynomial result = new Polynomial();
   
   Term term1 = p1.head;
   Term term2 = p2.head;
   
   while (term1 != null && term2 != null) {
      if (term1.exp > term2.exp) {
         result.addTerm(term1.coef, term1.exp);
         term1 = term1.link;
      } else if (term1.exp <term2.exp) {
         result.addTerm(term2.coef, term2.exp);
         term2= term2.link;
      } else {
         int coefSum = term1.coef +term2.coef;
         if (coefSum !=0) {
            result.addTerm(coefSum, term1.exp);
         }
         term1 = term1.link;
         term2 = term2.link;
      }
   }
   while (term1 != null) {
      result.addTerm(term1.coef, term1.exp);
      term1 = term1.link;
   }
   while (term2 != null) {
      result.addTerm(term2.coef, term2.exp);
      term2 =term2.link;
   }
   return result;
}
}
class Main {
	
	// main 메소드는 수정하지 마시오.
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

		// 두번째 다항식 입력 코드 작성할 것
	      no = scan.nextInt();

      for(int i = 0; i < no; i++) {
         int coef = scan.nextInt();
         int exp  = scan.nextInt();
         p2.addTerm(coef, exp);
      }


		// 두개의 다항식 덧셈
		Polynomial p3 = Polynomial.polyAdd(p1, p2);

		System.out.print(p3);  // 이것은 System.out.print(p3.toString())과 동일
	}
}
