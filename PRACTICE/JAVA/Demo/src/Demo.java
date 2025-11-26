import java.util.Scanner;

public class Demo {
    public static void main(String[] args) {
        int v1 = 4;
        boolean b1 = true;
        String s1 = "hello";
        double d1 = 10.5;
        System.out.println(s1 + " v1 = " + v1 + " " + b1 + " d1 = " + d1);

        Scanner scn = new Scanner(System.in);
        System.out.println("Introdu un nr intreg: ");
        int nrCitit1 = scn.nextInt();
        System.out.println("Numarul introdus a fost: " + nrCitit1);
        System.out.println("Introdu un alt nr intreg: ");
        int nrCitit2 = scn.nextInt();
        System.out.println("Al doilea numar introdus a fost: " + nrCitit2);

        scn.close();

        System.out.println("Suma numerelor citite de la tastatura este: " + (nrCitit1 + nrCitit2));
        
    }
}
