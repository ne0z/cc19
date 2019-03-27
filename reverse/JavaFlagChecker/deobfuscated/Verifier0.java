public class Veri00028
{
  private static byte[] encrypted = { 50, 48, 45, 50, 42, 39, 54, 49 };
  
  public static boolean verifyFlag(String paramString)
  {
    if (paramString.length() != encrypted.length) {
      return false;
    }
    for (int i = 0; i < encrypted.length; i++) {
      if (encrypted[i] != (paramString.charAt(i) ^ 0x42)) {
        return false;
      }
    }
    return true;
  }
}
