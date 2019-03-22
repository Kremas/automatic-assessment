import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

public class TestRunner {
	public static void main(String[] args) {
		Result result = JUnitCore.runClasses(TACTACTAChaha.class);

		System.out.println("<result>");
		System.out.println("<testrun>" + result.getRunCount() + "</testrun>");
		System.out.println("  <failure>");


		for(Failure failure : result.getFailures()) {
			System.out.println("    <test>");
			System.out.println("      <function>" + failure.getDescription() + "</function>");
			System.out.println("      <message>" + failure.getMessage() + "</message>");
			System.out.println("    </test>");
		}
		System.out.println("  </failure>");
		System.out.println("<success>" + result.wasSuccessful() + "</success>");
		System.out.println("</result>");
	}
}
