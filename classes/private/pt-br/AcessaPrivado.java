import java.lang.reflect.Field;

public class AcessaPrivado {

	public static void main(String[] args) {
		ObjetoSecreto oSecreto = new ObjetoSecreto("senha super secreta");
		Field campoPrivado = null;
		try {
			campoPrivado = ObjetoSecreto.class.getDeclaredField("escondido");
		}
		catch (NoSuchFieldException e) {
			System.err.println(e);
			System.exit(1);
		}
		campoPrivado.setAccessible(true); // arrombamos a porta
		try {
			String tavaEscondido = (String) campoPrivado.get(oSecreto);
			System.out.println("oSecreto.escondido = " + tavaEscondido);
		}
		catch (IllegalAccessException e) { 
			// esta exceção nao acontece porque fizemos setAcessible(true)
			System.err.println(e);
		}	
	}
}
