import java.io.*;
import java.util.Scanner;
import java.util.Stack;

class Main {
	
	// 필요한 필드나 메소드가 있으면 작성하시오.
	  static int precedence(char ch) {
      switch (ch) {
         case '+':
         case '-':
            return 1;
         case '*':
         case '/':
            return 2;
         case '(':
         case ')':
            return 0;
      }
      return -1;
   }
	
	public static void main(String[] args) throws Exception {
	Scanner scan = new Scanner(System.in);
		
	    // 아래 코드를 작성하시오.
      String str = scan.nextLine();
      StringBuilder output = new StringBuilder();
      Stack<Character> operatorStack = new Stack<>();

      for (int i = 0; i < str.length(); i++) {
            char ch = str.charAt(i);

      if (Character.isWhitespace(ch)) {
            continue;
      } else if (Character.isDigit(ch)) {
                     output.append(ch).append(' ');
      } else if (ch == '(') {
                     operatorStack.push(ch);
      } else if (ch == ')') {
            while (!operatorStack.isEmpty() && operatorStack.peek() != '(') {
                  output.append(operatorStack.pop()).append(' ');
            }
            if (!operatorStack.isEmpty() && operatorStack.peek() == '(') {
                  operatorStack.pop(); // Pop the '('
            }
      } else if (ch == '$') {
            break;
      } else { // Operators: +, -, *, /
            while (!operatorStack.isEmpty() && precedence(ch) <= precedence(operatorStack.peek())) {
                  output.append(operatorStack.pop()).append(' ');
            }
               operatorStack.push(ch);
      }
   }

      while (!operatorStack.isEmpty()) {
            output.append(operatorStack.pop()).append(' ');
      }

      System.out.println(output.toString().trim());
   }
}