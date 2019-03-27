import java.security.MessageDigest;
import javax.xml.bind.DatatypeConverter;

public class Veri00178
{
  private static String encrypted = "8FA14CDD754F91CC6554C9E71929CCE7865C0C0B4AB0E063E5CAA3387C1A8741FBADE9E36A3F36D3D676C1B808451DD7FBADE9E36A3F36D3D676C1B808451DD7";
  
  public static boolean verifyFlag(String paramString)
  {
    try
    {
      MessageDigest localMessageDigest = MessageDigest.getInstance("MD5");
      
      String str = "";
      for (int k : paramString.toCharArray())
      {
        localMessageDigest.update((byte)k);
        
        str = str + DatatypeConverter.printHexBinary(localMessageDigest.digest());
      }
      return str.equals(encrypted);
    }
    catch (Exception localException) {}
    return false;
  }
}
