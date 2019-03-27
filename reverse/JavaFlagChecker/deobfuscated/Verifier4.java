public class Veri00148
{
  private static int[] encrypted = { 3376, 3295, 3646, 3187, 3484, 3268 };
  
  public static boolean verifyFlag(String paramString)
  {
    if (paramString.length() != encrypted.length) {
      return false;
    }
    for (int i = 0; i < encrypted.length; i++) {
      if (encrypted[i] != paramString.charAt(i) * '\033' + 568) {
        return false;
      }
    }
    return true;
  }
}
