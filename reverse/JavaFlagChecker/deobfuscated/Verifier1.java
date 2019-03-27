public class Veri00058
{
  private static byte[] encrypted = { 115, 117, 111, 105, 120, 110, 97 };
  
  public static boolean verifyFlag(String paramString)
  {
    if (paramString.length() != encrypted.length) {
      return false;
    }
    for (int i = 0; i < encrypted.length; i++) {
      if (encrypted[i] != paramString.charAt(encrypted.length - 1 - i)) {
        return false;
      }
    }
    return true;
  }
}
