import java.io.*;
import java.util.*;

// 필요한 메소드를 추가하여 아래 클래스를 완성하시오.
class Graph {
   
   // 필요한 field, method는 추가하시오.
   private boolean Matrix[][];
   private int noVertex;

   // 생성자를 작성하시오.
   public Graph(int noVertex) {
      this.noVertex = noVertex;
      Matrix = new boolean[noVertex][noVertex];
   }
   
   // 간선 (i, j)를 삽입한다.
   public void addEdge(int i, int j) {
      Matrix[i][j] = true;
      Matrix[j][i] = true;
   }
   
   // 간선 (i, j)를 삭제한다.
   public void removeEdge(int i, int j) {
      Matrix[i][j] = false;
      Matrix[j][i] = false;
   }
   
   // BFS로 탐색하면서 방문하는 노드를 출력한다.
   // vertex에서 시작한다.
   public void bfs(int vertex) {
      Queue<Integer> queue = new LinkedList<>();
      boolean visited[] = new boolean[noVertex];

      visited[vertex] = true;
      queue.add(vertex);

      while (!queue.isEmpty()) {
         int currentVertex = queue.poll();
         System.out.print(currentVertex + " ");

         for (int i = 0; i < noVertex; i++) {
            if (Matrix[currentVertex][i] && !visited[i]) {
               queue.add(i);
               visited[i] = true;
            }
         }
      }
      System.out.println();
   }
   
   // DFS로 탐색하면서 방문하는 노드를 출력한다.
   // vertex에서 시작한다.
   public void dfs(int vertex) {
      boolean visited[] = new boolean[noVertex];
      dfs(vertex, visited);
      System.out.println();
   }
   
   private void dfs(int vertex, boolean[] visited) {
      visited[vertex] = true;
      System.out.print(vertex + " ");

      for (int i = noVertex - 1; i >= 0; i--) {
         if (Matrix[vertex][i] && !visited[i]) {
            dfs(i, visited);
         }
      }
   }
   // 그래프를 출력하는 메소드이다.
   public void print() {
      for (int i = 0; i < noVertex; i++) {
      System.out.print(i + " ");
      for (int j = 0; j < noVertex; j++) {
         if (Matrix[i][j]) {
            System.out.print(j + " ");
         }
      }
      System.out.println();
      }
   }
}

class Main {
   
   // main 메소드는 수정하지 마시오.
   public static void main(String[] args) throws Exception {
      Scanner scan = new Scanner(System.in);

      int noVertex = scan.nextInt();
      Graph graph = new Graph(noVertex);

      for(int i = 0; i < noVertex; i++) {
         for(int j = 0; j < noVertex; j++) {
            int vertex = scan.nextInt();
            if (vertex == 1)
               graph.addEdge(i, j);
         }
      }
      
      
      while(scan.hasNext()) {
         String cmd = scan.next();
         if (cmd.equals("P"))
            graph.print();
         else if (cmd.equals("I")) {
            int from = scan.nextInt();
            int to = scan.nextInt();
            graph.addEdge(from, to);
         } else if (cmd.equals("D")) {
            int from = scan.nextInt();
            int to = scan.nextInt();
            graph.removeEdge(from, to);
         } else if (cmd.equals("DFS")) {
            int vertex = scan.nextInt();
            graph.dfs(vertex);
         } else if (cmd.equals("BFS")) {
            int vertex = scan.nextInt();
            graph.bfs(vertex);
         } else if (cmd.equals("E")) { // 종료한다.
            break;
         }
      }
      
      scan.close();      
   }
}