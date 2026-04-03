import java.io.*;
import java.util.Scanner;
import java.util.Queue;
import java.util.LinkedList;

class BinaryTree {
   String data;
   BinaryTree left;
   BinaryTree right;
   
   public BinaryTree(String data) {
      this.data = data;
      left = right = null;
   }
   
   public void setChildren(BinaryTree left, BinaryTree right) {
      this.left = left;
      this.right = right;
   }
}

// Stack 클래스에 필요한 필드와 메소드를 추가하고, push, pop, isEmpty를 수정하여 완성하시오.
class Stack {
   
   // 필요한 필드와 메소드를 추가하시오.
   private LinkedList<BinaryTree> list = new LinkedList<BinaryTree>();
   
   
   public void push(BinaryTree item) {
      list.addFirst(item);
   }
   
   public BinaryTree pop() {
      if (isEmpty()) {
         throw new IllegalStateException("Stack is empty");
      }
      return list.removeFirst();
   }
   
   public boolean isEmpty() {
      return list.isEmpty();
   }
}

// 추가적으로 필요한 클래스(예를 들어 큐)가 있으면 작성하시오.

class Main {
   
   
   /***********************************
    * 아래 4개의 메소드를 작성하시오. *
   ***********************************/

   public static void inorder(BinaryTree node) {
      if (node != null) {
         inorder(node.left);
         System.out.print(node.data + " ");
         inorder(node.right);
      }
   }
   
   public static void preorder(BinaryTree node) {
      if (node != null) {
         System.out.print(node.data + " ");
         preorder(node.left);
         preorder(node.right);
      }
   }
   
   public static void postorder(BinaryTree node) {
      if (node != null) {
         postorder(node.left);
         postorder(node.right);
         System.out.print(node.data + " ");
      }
   }
   
   public static void levelorder(BinaryTree node) {
      if (node == null) {
         return;
      }
      
      Queue<BinaryTree> queue = new LinkedList<>();
      queue.add(node);

      while (!queue.isEmpty()) {
         BinaryTree current = queue.remove();
         System.out.print(current.data + " ");

      if (current.left != null) {
         queue.add(current.left);
         }

      if (current.right != null) {
         queue.add(current.right);
         }
      }
   }

   // 아래 main 메소드는 수정하지 마시오.
   public static void main(String[] args) throws Exception {
      Scanner scan = new Scanner(System.in);
      Stack stack = new Stack();
      
      BinaryTree root = null;
      
      // 이진 트리 생성
      while(scan.hasNext()) {
         String token = scan.next();
         if (token.equals("null")) {
            stack.push(null);
         } else if (token.equals(")")) {
            BinaryTree right = stack.pop();
            if (stack.isEmpty()) {
               root = right;
               break;
            }
            BinaryTree left = stack.pop();
            root = stack.pop();
            root.setChildren(left, right);
            stack.push(root);
         } else if (token.equals("(")) {
            continue;
         } else {
            stack.push(new BinaryTree(token));
         }
      }
      
      scan.close();
      
      inorder(root);
      System.out.println();
      preorder(root);
      System.out.println();
      postorder(root);
      System.out.println();
      levelorder(root);
   }
}