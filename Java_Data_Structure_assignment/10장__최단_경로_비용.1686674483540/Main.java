import java.io.*;
import java.util.Scanner;

class Graph {
    int noVertex;   // 정점의 갯수
    int[][] m;  // 인접 행렬
    public static final int NONE = 999; // 경로 없음

    /**
     * 그래프 데이터를 읽어들임.
     */
    public void loadData(Scanner scan) {
        int noVertex = scan.nextInt();    // 정점의 갯수

        this.noVertex = noVertex;
        m = new int[noVertex][noVertex];

        // 간선이 없는 그래프 생성
        for (int i = 0; i < noVertex; i++)
            for (int j = 0; j < noVertex; j++)
                m[i][j] = scan.nextInt();    // 가중치
    }

    // 필요한 메소드나 필드를 추가하시오.


    /**
     * 교재 p.393 참조
     * startVertex에서 출발하여 모든 정점으로의 최소 비용을 구한다.
     *
     * @param startVertex 출발하는 정점 (p.384에서 정점 0에 해당)
     * @return 출발정점에서 다른 모든 정점으로의 최소 비용 (p.394의 최종결과에 해당)
     */
    public int[] shortestPath(int startVertex) {
        int[] dist = new int[noVertex];
        for (int i = 0; i < dist.length; i++)
            dist[i] = m[startVertex][i];

        boolean[] visited = new boolean[noVertex];
        visited[startVertex] = true;

        for (int i = 0; i < noVertex - 1; i++) {
            int minVertex = findMinVertex(dist, visited);
            visited[minVertex] = true;

            for (int j = 0; j < noVertex; j++) {
                if (!visited[j] && m[minVertex][j] != NONE && dist[minVertex] + m[minVertex][j] < dist[j]) {
                    dist[j] = dist[minVertex] + m[minVertex][j];
                }
            }
        }

        return dist;
    }

    // 최소 비용을 갖는 정점을 찾는 메소드
    private int findMinVertex(int[] dist, boolean[] visited) {
        int minVertex = -1;
        for (int i = 0; i < noVertex; i++) {
            if (!visited[i] && (minVertex == -1 || dist[i] < dist[minVertex])) {
                minVertex = i;
            }
        }
        return minVertex;
    }
}

class Main {

    // main 메소드는 수정하지 마시오.
    public static void main(String[] args) throws Exception {
        Scanner scan = new Scanner(System.in);

        Graph g = new Graph();    // 그래프 생성
        g.loadData(scan);    // 그래프 데이터 읽음

        int startVertex = scan.nextInt();    // 출발 정점

        int[] dist = g.shortestPath(startVertex); // 최단 경로에 따른 비용을 구함
        for (int i = 0; i < dist.length; i++)
            System.out.print(dist[i] + " ");    // 비용 출력
    }
}