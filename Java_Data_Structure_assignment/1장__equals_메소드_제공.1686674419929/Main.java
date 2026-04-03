import java.io.*;

class Point {
	public int x;
	public int y;
	
	public Point(int x, int y) {
		this.x = x;
		this.y = y;
	}

	/**
	 * 아래에 equals 메소드를 추가하시오.
	 * @param object 반드시 Object 타입이어야 합니다.
	 */
	@Override
public boolean equals(Object object) {
	if (object instanceof Point) {
		Point point = (Point)object;
		return this.x == point.x && this.y == point.y;
		}
		return false;
	}



}

class Main {
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		
		int x1 = Integer.parseInt(br.readLine());
		int y1 = Integer.parseInt(br.readLine());
		int x2 = Integer.parseInt(br.readLine());
		int y2 = Integer.parseInt(br.readLine());
		
		Point point1 = new Point(x1, y1);
		Point point2 = new Point(x2, y2);
		
		System.out.println(point1.equals(point2));
	}
}