import org.junit.*; 
import static org.junit.Assert.*;
public class MaClasseTest {
  @Test
  public void add() {
    assertEquals("add(1, 2)", 3, MaClasse.add(1, 2), 0.0001);
    assertEquals("add(0, 2)", 2, MaClasse.add(0, 2), 0.0001);
  }

  @Test
  public void sub() {
    assertEquals("sub(5, 2)", 3, MaClasse.sub(5, 2), 0.0001);
  }

  @Test
  public void divide() {
    assertEquals("divide(6, 2)", 3, MaClasse.divide(6, 2), 0.0001);
  }

}
