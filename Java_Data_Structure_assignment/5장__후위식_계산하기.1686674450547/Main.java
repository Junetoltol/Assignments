import java.io.*;
import java.util.Scanner;
import java.util.Stack;

class Main {
	
	// 필요한 필드나 메소드가 있으면 작성하시오.
	
	public static void main(String[] args) throws Exception {
		Scanner scan = new Scanner(System.in);
		Stack<Double> stack = new Stack<>();
		// 아래 코드를 완성하시오.
		String str = scan.next();
		while (!str.equals("$")) {
			if (str.equals("+")) {
				  double operand2 = stack.pop();
          double operand1 = stack.pop();
          double result = operand1 + operand2;
          stack.push(result);
				
				
			} else if (str.equals("-")) {
				double operand2 = stack.pop();
        double operand1 = stack.pop();
        double result = operand1 - operand2;
        stack.push(result);
				
				
			} else if (str.equals("*")) {
				double operand2 = stack.pop();
        double operand1 = stack.pop();
        double result = operand1 * operand2;
        stack.push(result);
				
			} else if (str.equals("/")) {
				double operand2 = stack.pop();
        double operand1 = stack.pop();
        double result = operand1 / operand2;
      	stack.push(result);
				
				
			} else {
				double operand = Double.parseDouble(str);	
	Double.parseDouble(str);   
      	stack.push(operand);
				
				
			}
			
			str = scan.next();
		}
		double result = stack.pop();
		System.out.println(result);
	}
}