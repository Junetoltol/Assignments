import java.util.Scanner;

public class Main {
      public static void main(String[] args) {
            Maze m = new Maze();
            m.MazeData();
            m.findExit();
      }
}

class Maze {
      int sizeX, sizeY;
      int startX, startY;
      int endX, endY;
      int[][] maze;

      public void MazeData() {
            Scanner scan = new Scanner(System.in);

            sizeY = scan.nextInt();
            sizeX = scan.nextInt();
         
            startY = scan.nextInt();
            startX = scan.nextInt();

            endX = scan.nextInt();
            endY = scan.nextInt();

            maze = new int[sizeY][sizeX];

            for (int y = 0; y < sizeY; y++) {
                  for (int x = 0; x < sizeX; x++) {
                        maze[y][x] = scan.nextInt();
                  }
            }

            scan.close();
      }

      public void findExit() {
            if (findPath(maze, startX, startY, endX, endY)) {
                  printPath();
            } else {
                  System.out.println("Path not found.");
            }
      }

      private boolean findPath(int[][] maze, int x, int y, int exitX, int exitY) {
            if (x == exitX && y == exitY) {
                  maze[y][x] = 2;
                  return true;
            }

            if (x < 0 || y < 0 || x >= maze[0].length || y >= maze.length || maze[y][x] != 0) {
                  return false;
            }

            maze[y][x] = 2;

            int[] dx = {1, 0, -1, 0};
            int[] dy = {0, 1, 0, -1};

            for (int i = 0; i < 4; i++) {
                  int newX = x + dx[i];
                  int newY = y + dy[i];

                  if (findPath(maze, newX, newY, exitX, exitY)) {
                           return true;
                  }
            }

            maze[y][x] = 0;

            return false;
      }

      private void printPath() {
            for (int y = 0; y < sizeY; y++) {
                  for (int x = 0; x < sizeX; x++) {
                        if (maze[y][x] == 2 && (y != startY || x != startX) && (y != endY || x != endX)) {
                              System.out.print(" *");
                        } else if (y == startY && x == startX) {
                              System.out.print(" S");
                        } else if (y == endY && x == endX) {
                              System.out.print(" F");
                        } else {
                              System.out.print(" " + maze[y][x]);
                           }
                  }
                  System.out.println();
            }
      }
}