import java.io.*;
import java.util.Scanner;

class BinarySearchTree {
   class TreeNode {
      String key;
      TreeNode left;
      TreeNode right;
   }
   
   private TreeNode rootNode;
   
   public void insert(String x) {
      rootNode = insertKey(rootNode, x);
   }
   
   public TreeNode find(String x) {
      TreeNode t = rootNode;
      int result;
      
      while (t != null) {
         if ((result = x.compareTo(t.key)) < 0) {
            t = t.left;
         } else if (result == 0) {
            return t;
         } else {
            t = t.right;
         }
      }
      
      return t;
   }
   
   private void printNode(TreeNode n) {
      if (n != null) {
         System.out.print("(");
         printNode(n.left);
         System.out.print(n.key);
         printNode(n.right);
         System.out.print(")");
      }
   }
   
   public void print() {
      printNode(rootNode);
      System.out.println();
   }
   
   // 아래 2개의 메소드 insertKey, delete를 완성하시오.
   
   /**
    * 교재 p.325 참조
    * 이원탐색트리의 노드 t에 데이터 x를 추가한다. 순환함수로 작성해야 한다.
    * @param t 이원탐색트리의 노드. 이 노드 아래에 데이터를 삽입한다.
    * @param x 삽입하고자 하는 데이터
    * @return 사입한 이원탐색트리의 부모 노드
    */
   private TreeNode insertKey(TreeNode t, String x) {
      if (t == null) {
            TreeNode newNode = new TreeNode();
            newNode.key = x;
            newNode.left = newNode.right = null;
         return newNode;
      }
      int result = x.compareTo(t.key);

            if (result < 0) {
                  t.left = insertKey(t.left, x);
            } else if (result > 0) {
                  t.right = insertKey(t.right, x);
            }

            return t;
      }
   }
   
class Main {
   
   // 아래 main 메소드는 수정하지 마시오.
   public static void main(String[] args) throws Exception {
      Scanner scan = new Scanner(System.in);
      BinarySearchTree tree = new BinarySearchTree();
      
      while (scan.hasNext()) {
         String command = scan.next();
         
         if (command.equals("I")) {
            String data = scan.next();
            tree.insert(data);
         } else if (command.equals("P")) {
            tree.print();
         }
      }
      scan.close();
   }
   
}