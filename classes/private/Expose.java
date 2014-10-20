import java.lang.reflect.Field;

public class Expose {

    public static void main(String[] args) {
        Confidential message = new Confidential("top secret text");
        Field secretField = null;
        try {
            secretField = Confidential.class.getDeclaredField("secret");
        }
        catch (NoSuchFieldException e) {
            System.err.println(e);
            System.exit(1);
        }
        secretField.setAccessible(true); // break the lock!
        try {
            String wasHidden = (String) secretField.get(message);
            System.out.println("message.secret = " + wasHidden);
        }
        catch (IllegalAccessException e) { 
            // this will not happen after setAcessible(true)
            System.err.println(e);
        }   
    }
}
