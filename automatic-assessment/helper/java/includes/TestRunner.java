import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

public class TestRunner {
	public static void main(String[] args) {
		Result result = JUnitCore.runClasses(TACTACTAChaha.class);

		System.out.print("{");
		System.out.print("\"testrun\":\"" + result.getRunCount() + "\",");
		System.out.print("\"failure\":[");

		int size = result.getFailureCount();
		for(Failure failure : result.getFailures()) {
			// System.out.print("\"test\":{},");
			System.out.print("{\"function\":\"" + failure.getDescription() + "\",");
			System.out.println("\"message\":\"" + failure.getMessage() + "\"}");
			if(--size != 0) {
				System.out.print(",");
			}
		}
		System.out.print("],");
		System.out.print("\"success\":\"" + result.wasSuccessful() + "\"");
		System.out.println("}]");
	}
}
