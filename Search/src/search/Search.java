/*
* @Author Logan Williams
* Computer Science 476X/576X
* Project 2
*/

package search;

import java.io.*;
import java.util.ArrayList;
import java.util.LinkedList;

public class Search {

    static Cell[][] cObstacle = new Cell[360][360];

    public static void readObstacleFile(){
        try{
            FileInputStream f = new FileInputStream("cObstacles.txt");
            DataInputStream in = new DataInputStream(f);
            BufferedReader br = new BufferedReader(new InputStreamReader(in));
            String line;
            int row = 0;
            while((line = br.readLine()) != null){
                String[] tokens = line.split(" ");
                int col = 0;
                for(String t : tokens){
                    int val = Integer.parseInt(t);
                    cObstacle[row][col] = new Cell(val, row, col);
                    col++;
                }
                row++;
            }
        } catch (Exception e){
            System.err.println("Error while reading from the file specified");
        }
    }

    public static void BFS(Cell goal, Cell start){
        LinkedList<Cell> queue = new LinkedList<>();
        start.visited = 1;
        goal.setGoal(true);
        queue.add(start);
        while(!queue.isEmpty()){
            Cell temp = queue.remove();
            if(temp.getGoal()) {
                Object[] solution = findSolution(goal);
                writePathToFile(solution);
                return;
            }
            for(Cell neighbor : temp.getNeighbors()){
                if(neighbor.getVisited() == 0){
                    neighbor.setVisited(1);
                    neighbor.setParent(temp);
                    queue.add(neighbor);
                }
            }
            temp.setVisited(2);
        }

    }

    public static void writePathToFile(Object[] solution){
        try{
            FileWriter fileWriter = new FileWriter("path.txt");
            PrintWriter printWriter = new PrintWriter(fileWriter);
            for(Object temp : solution){
                printWriter.printf("%d %d\n", ((Cell) temp).x, ((Cell) temp).y);
            }
            printWriter.close();
        } catch(Exception e){
            System.err.println("Error while writing to the file specified");
        }
    }

    public static Object[] findSolution(Cell goal){
        LinkedList<Cell> solution = new LinkedList<Cell>();
        solution.addFirst(goal);
        while(goal.parent != null) {
            goal = goal.parent;
            solution.addFirst(goal);
        }
        return solution.toArray();
    }

    /**
    * initializes all the neighbors of the cells
    **/
    private static void initNeighbors(){
        for(int i = 0; i < cObstacle.length; i++){
            for(int j = 0; j < cObstacle[i].length; j++){
                if(isValid(i - 1,j))
                    cObstacle[i][j].addNeighbors(cObstacle[i - 1][j]);
                if(isValid(i + 1,j))
                    cObstacle[i][j].addNeighbors(cObstacle[i + 1][j]);
                if(isValid(i,j - 1))
                    cObstacle[i][j].addNeighbors(cObstacle[i][j - 1]);
                if(isValid(i,j + 1))
                    cObstacle[i][j].addNeighbors(cObstacle[i][j + 1]);
            }
        }
    }

    private static boolean isValid(int x, int y){
        if(x < 0 || x >= cObstacle.length || y < 0 || y >= cObstacle[x].length)
            return false;
        return true;
    }



    public static void main(String args[]){
        readObstacleFile();
        initNeighbors();
        BFS(cObstacle[180][270],cObstacle[0][0]);
    }

}

class Cell {
    int value;
    Cell parent;
    int visited;
    boolean isGoal;
    ArrayList<Cell> Neighbors;
    int x;
    int y;

    public void setGoal(boolean t) {
        this.isGoal = t;
    }
    public boolean getGoal(){
        return this.isGoal;
    }

    public int getVisited() {
        return visited;
    }

    public void setVisited(int visited) {
        this.visited = visited;
    }

    public int getValue() {
        return value;
    }

    public Cell getParent() {
        return parent;
    }

    public void setParent(Cell parent) {
        this.parent = parent;
    }

    public ArrayList<Cell> getNeighbors() {
        return Neighbors;
    }

    public void addNeighbors(Cell neighbor) {
        Neighbors.add(neighbor);
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public Cell(int value, int x, int y){
        this.value = value;
        this.x = x;
        this.y = y;
        this.parent = null;
        this.Neighbors = new ArrayList<>();
        this.visited = 0;
        this.isGoal = false;
    }
}
