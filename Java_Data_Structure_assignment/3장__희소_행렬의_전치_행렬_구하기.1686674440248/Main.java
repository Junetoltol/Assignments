import java.io.*;
import java.util.Scanner;

class SparseMatrix {
	int[][] m;

	/**
	 * @param row 행의 갯수
	 * @param col 열의 갯수
	 * @param no 0이 아닌 항의 갯수
	 */
	
	public SparseMatrix(int row, int col, int no) {
		m = new int[no + 1][3];
		m[0][0] = col;
		m[0][1] = row;
		m[0][2] = no;
	}

	// 이 행렬을 전치 행렬로 변환하는 알고리즘을 작성하시오.
	public void transpose() {
    int[][] transposed = new int[m[0][2] + 1][3];
    transposed[0][0] = m[0][1];
    transposed[0][1] = m[0][0];
    transposed[0][2] = m[0][2];
    if (m[0][2] > 0) {
        int[] rowTerms = new int[m[0][1]];
        int[] startingPos = new int[m[0][1]];
        for (int i = 1; i <= m[0][2]; i++) {
            rowTerms[m[i][1]]++;
        }
        startingPos[0] = 1;
        for (int i = 1; i < m[0][1]; i++) {
            startingPos[i] = startingPos[i-1] + rowTerms[i-1];
        }
        for (int i = 1; i <= m[0][2]; i++) {
            int j = startingPos[m[i][1]]++;
            transposed[j][0] = m[i][1];
            transposed[j][1] = m[i][0];
            transposed[j][2] = m[i][2];
        }
    }
    m = transposed;
}


	// 전치 행렬의 내용을 출력하는 코드를 작성하시오.
	public String toString() {
		StringBuffer str = new StringBuffer();

		for(int i = 0; i <= m[0][2]; i++) {
			str.append(m[i][0]).append(" ")
				 .append(m[i][1]).append(" ")
				 .append(m[i][2]).append("\n");
		}

		return str.toString();
	}
}

class Main {
	
	// main 메소드는 수정하지 마시오.
	public static void main(String[] args) throws Exception {
		Scanner scan = new Scanner(System.in);
		int col = scan.nextInt();
		int row = scan.nextInt();
		int no = scan.nextInt();

		SparseMatrix matrix = new SparseMatrix(row, col, no);

		for(int i = 1; i <= no; i++) {
			matrix.m[i][0] = scan.nextInt();
			matrix.m[i][1] = scan.nextInt();
			matrix.m[i][2] = scan.nextInt();
		}

		matrix.transpose();

		System.out.print(matrix);
	}
}