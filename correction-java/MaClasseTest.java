import org.junit.*; 
import static org.junit.Assert.*;
public class MaClasseTest {
  @Test
  public void add() {
    assertEquals("add(1,2)", 4, MaClasse.add(1,2), 0.0001);
    assertEquals("add(-2,2)", 0, MaClasse.add(-2,2), 0.0001);
  }

  @Test
  public void sub() {
    assertEquals("sub(5,2)", 3, MaClasse.sub(5,2), 0.0001);
    assertEquals("sub(-2,2)", -4, MaClasse.sub(-2,2), 0.0001);
  }

  @Test
  public void divide() {
    assertEquals("divide(6,2)", 3.0, MaClasse.divide(6,2), 0.0001);
  }

}
