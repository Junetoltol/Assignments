import java.io.*;
import java.util.*;

abstract class Shape {
	protected double x;
	protected double y;

	protected Shape(double x, double y) {
		this.x = x;
		this.y = y;
	}

	public abstract void draw();

	public abstract double getArea();
}

// 여기에 Circle과 Rectangle 클래스를 작성하시오.
class Circle extends Shape {
   public static final double PI = 3.14;
   private double radius;
   
   public Circle(double x, double y, double radius) {
      super(x,y);
      this.radius = radius;
   }
   
   public void draw() {
      System.out.println("Circle");
   }
   
   public double getArea() {
      return PI * radius * radius;
   }
}

class Rectangle extends Shape {
   private double width;
   private double height;
   
   public Rectangle(double x, double y, double width, double height) {
      super(x,y);
      this.width = width;
      this.height = height;
   }
   
   public void draw() {
      System.out.println("Rectangle");
   }
   
   public double getArea() {
      return width * height;
   }
}

public class Main {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int noShape = scan.nextInt();
		Shape[] shapes = new Shape[noShape];

		for (int i = 0; i < noShape; i++) {
			String s = scan.next();
			if (s.equals("Rectangle")) {
				double x = scan.nextDouble();
				double y = scan.nextDouble();
				double width = scan.nextDouble();
				double height = scan.nextDouble();
				shapes[i] = new Rectangle(x, y, width, height);
			} else if (s.equals("Circle")) {
				double x = scan.nextDouble();
				double y = scan.nextDouble();
				double radius = scan.nextDouble();
				shapes[i] = new Circle(x, y, radius);
			}
		}

		// 그 다음엔 면적을 계산한다.
		double sumArea = 0;
		for (Shape shape : shapes) {
			sumArea += shape.getArea();
		}

		System.out.printf("%.2f", sumArea);
	}
}