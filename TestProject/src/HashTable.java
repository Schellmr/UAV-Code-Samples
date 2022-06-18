import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

/**
 * COP 3530: Project 5 – Hash Tables
 * <p>
 * This class is an implementation of a Hash Table
 *
 * @author <Hayden Keeney>
 * @version <4/18/2021>
 */
public class HashTable {
    private final int arraySize;
    public List<LinkedList<Node>> hashTable;

    /**
     * A default constructor for our HashTable. Initialized to a default size of 101.
     */
    public HashTable() {
        this.arraySize = 101;
        this.hashTable = new ArrayList<>(arraySize);
        for (int i = 0; i < arraySize; i++) {
            hashTable.add(new LinkedList<>());
        }
    }

    /**
     * An insert method. Inserts a given state with population and deaths into the Hash Table
     *
     * @param state the state's name to insert
     * @param population the state's population to insert
     * @param deaths the state's deaths to insert
     */
    public void insert(String state, long population, long deaths) {
        Node newNode = new Node(state, population, deaths);
        hashTable.get(getHash(newNode)).add(newNode);
    }
    /**
     * A method to find a state and print its information
     *
     * @param state A state's name to find
     * @param population The state's population
     * @param deaths The state's total deaths
     * @return either the Hash Value indicating where the state is stored in the table or -1 to indicate it isn't found
     */
    public int find(String state, long population, long deaths) {
        Node nodeToFind = new Node(state, population, deaths);
        int hashVal = getHash(nodeToFind);

        List<Node> nodeList = hashTable.get(hashVal);
        for (Node node : nodeList) {
            if (node.name.equals(state) && node.deaths == deaths && node.population == population) {
                return hashVal;
            }
        }
        return -1;
    }
    /**
     * A delete method. Deletes a given state from the Hash Table if it exists.
     *
     * @param state The state's name to be deleted
     * @param population The state's population
     * @param deaths The state's total COVID deaths.
     */
    public void delete(String state, long population, long deaths) {
        Node nodeToDelete = new Node(state, population, deaths);
        int hashVal = getHash(nodeToDelete);

        List<Node> nodeList = hashTable.get(hashVal);
        for (Node node : nodeList) {
            if (node.name.equals(state) && node.deaths == deaths && node.population == population) {
                nodeList.remove(node);
            }
        }
    }
    /**
     * A display method. Prints the entire table and formats it nicely.
     */
    public void display() {
        for (int i = 0; i < arraySize; i++) {
            System.out.printf("%3d. ", i);
            List<Node> nodeList = hashTable.get(i);
            if (nodeList.isEmpty()) {
                System.out.println("Empty");
            } else {
                nodeList.get(0).printNode();
                for (int j = 1; j < nodeList.size(); j++) {
                    System.out.print("     ");
                    nodeList.get(j).printNode();
                }
            }
        }
    }
    /**
     * An informational method to show the number of collisions and empty cells.
     */
    public void printEmptyAndCollisions() {
        int numEmpty = 0, numCollisions = 0;
        for (int i = 0; i < arraySize; i++) {
            List<Node> nodeList = hashTable.get(i);
            if (nodeList.isEmpty()) {
                numEmpty++;
            } else if (nodeList.size() > 1) {
                numCollisions++;
            }
        }
        System.out.println("There are " + numEmpty + " empty cells and " + numCollisions + " collisions in the" +
                " hash table");
    }

    /**
     * Gets the hash of a node
     *
     * @param node the node to calculate the hash of
     * @return the hash of that node.
     */
    private int getHash(Node node) {
        int hash = 0;
        for (char c : node.name.toCharArray()) {
            hash += c;
        }
        return (int) (hash + (node.population + node.deaths)) % 101;
    }

    /**
     * An inner class that we will be using to store in the table
     */
    public static class Node {
        String name;
        long population;
        long deaths;

        /**
         * A constructor for the node taking name population and deaths
         *
         * @param name the name of the state
         * @param population the population of the state
         * @param deaths the total covid related deaths in the state
         */
        public Node(String name, long population, long deaths) {
            this.name = name;
            this.population = population;
            this.deaths = deaths;
        }

        /**
         * A method to print the node nicely
         */
        public void printNode() {
            System.out.printf("%-30s %-20.5f\n", name, ((double) deaths) / ((double) population));
        }
    }
}
