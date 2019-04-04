public class Veri00118
{
  private static String encrypted = "obwaohfcbwq";
  
  public static boolean verifyFlag(String paramString)
  {
    if (paramString.length() != encrypted.length()) {
      return false;
    }
    for (int i = 0; i < encrypted.length(); i++)
    {
      if (!Character.isLowerCase(paramString.charAt(i))) {
        return false;
      }
      if ((encrypted.charAt(i) - 'a' + 12) % 26 != paramString.charAt(i) - 'a') {
        return false;
      }
    }
    return true;
  }
}
