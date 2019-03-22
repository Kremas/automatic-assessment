public class MaClasse{
  public static int add(int a, int b) {
    int res = a + b;
    return res;
  }

  public static int sub(int a, int b) {
    int res = a - b;
    return res;
  }

  public static int multiply(int a, int b) {
    int res = a * b;
    return res;
  }

  public static double divide(int a, int b) {
    double res;
    if(b != 0) res = a / b;
    else res = 0.0;
    return res;
  }

  public static String concatenate(String a, String b) {
    return a + b;
  }
}
