import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * COP 3530: Project 5 - Hash Tables
 * <p> This project implements a Hash Table using a specified hashing function. This class contains the entry point of
 * the program as well as the table instance. Furthermore, this class will maintain a list of all the states.</p>
 *
 * @author <Hayden Keeney>
 * @version <4/18/2021>
 */
public class Project5 {
    private HashTable myTable;
    private ArrayList<String> lines;

    /**
     * This creates an instance of Project5 taking only a path from which a file should be read.
     *
     * @param path the path to the file from which we read.
     */
    public Project5(String path) {
        try {
            BufferedReader reader = new BufferedReader(new FileReader(path));

            myTable = new HashTable();
            lines = new ArrayList<>();

            String line;
            reader.readLine();
            while ((line = reader.readLine()) != null) {
                String[] inputs = line.split(",");
                myTable.insert(inputs[0], Long.parseLong(inputs[4]), Long.parseLong(inputs[6]));
                lines.add(line);
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    /**
     * This is the entry point for the program. It will request user input, create an instance of project 5, and act
     * as the IO handler for most of the program functionality.
     *
     * @param args command line arguments (unused in this program)
     */
    public static void main(String[] args) {
        try {
            Scanner scanner = new Scanner(System.in);
            System.out.println("Enter a file path: ");
            String path = scanner.nextLine();

            Project5 project5 = new Project5(path);

            boolean quit = false;
            while (!quit) {
                int input;
                do {
                    System.out.print("\t1. Print hash table\n\t2. Delete a state of a given name\n\t3. Insert a " +
                            "state of a given name\n\t4. Search and print a state and its DR for a give name\n\t" +
                            "5. Print numbers of empty cells and collisions\n\t6. Exit\n");
                    System.out.print("Enter a number between 1 and 6: ");

                    while (!scanner.hasNextInt()) {
                        System.out.print("Please enter an integer: ");
                        scanner.next();
                    }
                    input = scanner.nextInt();
                } while (input < 1 || input > 6);

                switch (input) {
                    case 1 -> project5.myTable.display();
                    case 2 -> {
                        scanner = new Scanner(System.in);
                        String userInput;
                        System.out.print("Enter a state's name: ");
                        while (!scanner.hasNextLine()) {
                            System.out.print("Try again: ");
                            scanner.next();
                        }
                        userInput = scanner.nextLine();

                        boolean handled = false;
                        for (String line : project5.lines) {
                            String[] inputs = line.split(",");
                            if (inputs[0].equals(userInput)) {
                                String name = inputs[0];
                                long population = Long.parseLong(inputs[4]), deaths = Long.parseLong(inputs[6]);
                                int hash = project5.myTable.find(name, population, deaths);
                                if (hash != -1) {
                                    project5.myTable.delete(inputs[0], Long.parseLong(inputs[4]),
                                            Long.parseLong(inputs[6]));
                                    System.out.println("Deleted " + userInput + "!");

                                    handled = true;
                                } else {
                                    System.out.println("That state wasn't in the table.");
                                }
                            }
                        }
                        if (!handled) {
                            System.out.println(userInput + " is not a state.");
                        }
                    }
                    case 3 -> {
                        scanner = new Scanner(System.in);
                        String userInput;
                        System.out.print("Enter a state's name: ");
                        while (!scanner.hasNextLine()) {
                            System.out.print("Try again: ");
                            scanner.next();
                        }
                        userInput = scanner.nextLine();

                        boolean handled = false;
                        for (String line : project5.lines) {
                            String[] inputs = line.split(",");
                            if (inputs[0].equals(userInput)) {
                                String name = inputs[0];
                                long population = Long.parseLong(inputs[4]), deaths = Long.parseLong(inputs[6]);
                                int hash = project5.myTable.find(name, population, deaths);
                                if (hash == -1) {
                                    project5.myTable.insert(inputs[0], Long.parseLong(inputs[4]),
                                            Long.parseLong(inputs[6]));
                                    System.out.println("Inserted " + userInput + "!");
                                } else {
                                    System.out.println(userInput + " already exists in this table.");
                                }
                                handled = true;
                            }
                        }
                        if (!handled) {
                            System.out.println(userInput + " is not a state.");
                        }
                    }
                    case 4 -> {
                        scanner = new Scanner(System.in);
                        String userInput;
                        System.out.print("Enter a state's name: ");
                        while (!scanner.hasNextLine()) {
                            System.out.print("Try again: ");
                            scanner.next();
                        }
                        userInput = scanner.nextLine();

                        boolean handled = false;
                        for (String line : project5.lines) {
                            String[] inputs = line.split(",");
                            if (inputs[0].equals(userInput)) {
                                String name = inputs[0];
                                long population = Long.parseLong(inputs[4]), deaths = Long.parseLong(inputs[6]);
                                int hash = project5.myTable.find(name, population, deaths);
                                if (hash != -1) {
                                    for (int i = 0; i < project5.myTable.hashTable.get(hash).size(); i++) {
                                        if (project5.myTable.hashTable.get(hash).get(i).name.equals(name)) {
                                            project5.myTable.hashTable.get(hash).get(i).printNode();
                                        }
                                    }
                                } else {
                                    System.out.println("That state wasn't in the table.");
                                }
                                handled = true;
                            }
                        }
                        if (!handled) {
                            System.out.println(userInput + " is not a state.");
                        }                    }
                    case 5 -> project5.myTable.printEmptyAndCollisions();
                    default -> {
                        System.out.println("Have a nice day!");
                        quit = true;
                    }
                }
                System.out.println();
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
