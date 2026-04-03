import java.io.*;
import java.util.Scanner;

class Graph {
    int noVertex;    // 정점의 갯수
    int[][] m;    // 인접 행렬

    public Graph(int noVertex) {
        this.noVertex = noVertex;
        m = new int[noVertex][noVertex];
    }

    // 필요한 메소드나 필드를 추가하시오.

    /**
     * 그래프의 전향폐쇄를 계산한다.
     *
     * @return 그래프의 전향폐쇄를 나타내는 2차원 배열을 반환한다.
     */
    public int[][] getTransitiveClosure() {
        int[][] closure = new int[noVertex][noVertex];

        for (int i = 0; i < noVertex; i++) {
            for (int j = 0; j < noVertex; j++) {
                closure[i][j] = m[i][j]; // 전향폐쇄의 초기값은 인접행렬과 동일하게 설정
            }
        }

        for (int k = 0; k < noVertex; k++) {
            for (int i = 0; i < noVertex; i++) {
                for (int j = 0; j < noVertex; j++) {
                    closure[i][j] = closure[i][j] | (closure[i][k] & closure[k][j]);
                }
            }
        }

        return closure;
    }

}

class Main {

    // main 메소드는 수정하지 마시오.
    public static void main(String[] args) throws Exception {
        Scanner scan = new Scanner(System.in);
        int noVertex = scan.nextInt();    // 정점의 갯수

        Graph g = new Graph(noVertex);    // 그래프 생성
        for (int i = 0; i < noVertex; i++)
            for (int j = 0; j < noVertex; j++)
                g.m[i][j] = scan.nextInt();

        int[][] mat = g.getTransitiveClosure();
        for (int[] m : mat) {
            for (int exist : m)
                System.out.print(exist + " ");
            System.out.println();
        }
    }
}