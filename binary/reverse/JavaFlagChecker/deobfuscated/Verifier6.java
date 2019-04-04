import java.security.MessageDigest;
import javax.xml.bind.DatatypeConverter;

public class Veri00208
{
  private static String hash = "1B480158E1F30E0B6CEE7813E9ECF094BD6B3745";
  
  public static boolean verifyFlag(String paramString)
  {
    if (paramString.length() != 4) {
      return false;
    }
    try
    {
      MessageDigest localMessageDigest = MessageDigest.getInstance("SHA1");
      
      localMessageDigest.update(paramString.getBytes());
      
      String str = DatatypeConverter.printHexBinary(localMessageDigest.digest());
      
      return str.equals(hash);
    }
    catch (Exception localException) {}
    return false;
  }
}
