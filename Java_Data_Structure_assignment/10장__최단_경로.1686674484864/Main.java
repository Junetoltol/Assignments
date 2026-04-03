import java.io.*;
import java.util.Scanner;
import java.util.ArrayList;

class Graph {
	int noVertex;	// 정점의 갯수
	int[][] m;	// 인접 행렬
	public static final int NONE = 999; // 경로 없음
	

	/**
	 * 그래프 데이터를 읽어들임.
	 */
	public void loadData(Scanner scan) {
		int noVertex = scan.nextInt();	// 정점의 갯수

		this.noVertex = noVertex;
		m = new int[noVertex][noVertex];
		
		// 간선이 없는 그래프 생성
		for(int i = 0; i < noVertex; i++)
			for(int j = 0; j < noVertex; j++)
				m[i][j] = scan.nextInt();	// 가중치
	}

/**
     * 교재 p.393 참조
     * startVertex에서 출발하여 모든 정점으로의 최소 비용을 구한다.
     *
     * @param startVertex 출발하는 정점 (p.384에서 정점 0에 해당)
     * @return 출발정점에서 다른 모든 정점으로의 최소 비용 (p.394의 최종결과에 해당)
     */
    public ArrayList<Integer> shortestPath(int startVertex, int finalVertex) {
        ArrayList<Integer> path = new ArrayList<Integer>(); // 최단 경로를 기록하기 위한 변수
        int[] dist = new int[noVertex];
        int[] prev = new int[noVertex];
        boolean[] visited = new boolean[noVertex];

        for (int i = 0; i < noVertex; i++) {
            dist[i] = NONE;
            prev[i] = NONE;
            visited[i] = false;
        }

        dist[startVertex] = 0;

        for (int i = 0; i < noVertex - 1; i++) {
            int minVertex = findMinVertex(dist, visited);
            visited[minVertex] = true;

            for (int j = 0; j < noVertex; j++) {
                if (!visited[j] && m[minVertex][j] != NONE && dist[minVertex] + m[minVertex][j] < dist[j]) {
                    dist[j] = dist[minVertex] + m[minVertex][j];
                    prev[j] = minVertex;
                }
            }
        }

        if (dist[finalVertex] == NONE) {
            return path; // No path found
        }

        int currentVertex = finalVertex;
        while (currentVertex != startVertex) {
            path.add(currentVertex);
            currentVertex = prev[currentVertex];
        }
        path.add(startVertex);
        reverseList(path);

        return path;
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

    // 리스트 순서 뒤집기
    private void reverseList(ArrayList<Integer> list) {
        int left = 0;
        int right = list.size() - 1;
        while (left < right) {
            int temp = list.get(left);
            list.set(left, list.get(right));
            list.set(right, temp);
            left++;
            right--;
        }
    }

    /**
     * 경로 path의 모든 가중치의 합을 구한다.
     *
     * @param path shortestPath 메소드에서 구한 경로로 가중치의 합을 계산하기 위한 것이다.
     * @return path의 비용 합을 반환한다.
     */
    public int getCost(ArrayList<Integer> path) {
        int cost = 0;
        for (int i = 0; i < path.size() - 1; i++) {
            int source = path.get(i);
            int destination = path.get(i + 1);
            cost += m[source][destination];
        }
        return cost;
    }
}
class Main {
	
	// main 메소드는 수정하지 마시오.
	public static void main(String[] args) throws Exception {
		Scanner scan = new Scanner(System.in);

		Graph g = new Graph();	// 그래프 생성
		g.loadData(scan);	// 그래프 데이터 읽음
		
		int startVertex = scan.nextInt();	// 출발 정점 
		int finalVertex = scan.nextInt(); // 도착 정점
			
		ArrayList<Integer> path = g.shortestPath(startVertex, finalVertex); // 최단 경로에 따른 비용을 구함
		for(int vertex : path)
			System.out.print(vertex + " ");	// 경로 출력
		System.out.println();
		System.out.println(g.getCost(path)); // 비용 출력
	}
}