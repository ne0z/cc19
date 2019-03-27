public class Veri00088
{
  private static int[] encrypted = { 3080674, 3110465, 3348793, 3408375, 3319002, 3229629, 3557330, 3229629, 3408375, 3378584 };
  
  public static boolean verifyFlag(String paramString)
  {
    if (paramString.length() != encrypted.length) {
      return false;
    }
    for (int i = 0; i < encrypted.length; i++) {
      if (encrypted[i] != (paramString.substring(i, i + 1) + "foo").hashCode()) {
        return false;
      }
    }
    return true;
  }
}
