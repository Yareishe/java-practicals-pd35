package ua.duikt.automaton;

import java.util.Scanner;

public final class Main {
    private Main() {
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Введіть рядок: ");
        String input = scanner.nextLine();

        Automaton.State finalState = new Automaton().run(input);
        System.out.println("Кінцевий стан автомата: " + finalState.label());
    }
}
