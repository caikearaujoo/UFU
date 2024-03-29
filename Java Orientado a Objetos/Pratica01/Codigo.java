import java.util.Scanner;

public class Main 
{
	public static void main(String args[])
	{
		Scanner scan = new Scanner(System.in);
		
		int ladoa, ladob, ladoc, result;
		
		Triangulo objeto = new Triangulo();
		
		System.out.println("Olá usuário, escreva o lado A do triangulo");
		ladoa = scan.nextInt();
		
		System.out.println("Olá usuário, escreva o lado B do triangulo");
		ladob= scan.nextInt();
		
		System.out.println("Olá usuário, escreva o lado C do triangulo");
		ladoc= scan.nextInt();
		
		if(objeto.possivel(ladoa, ladob, ladoc) == true)
		{
			objeto.setA(ladoa);
			objeto.setB(ladob);
			objeto.setC(ladoc);
			System.out.println("Foi possível criar o triangulo.");
		}
		else System.out.println("As medidas do triangulo nao funcionam.");
		
		if(objeto.tipo_triangulo(ladoa, ladob, ladoc) == 1)
		{
			System.out.println("Triangulo equilatero");
		}
		else if(objeto.tipo_triangulo(ladoa, ladob, ladoc) == 2)
		{
			System.out.println("Triangulo escaleno");
		}
		else
		{
			System.out.println("Triangulo isósceles");
		}
		
		result = objeto.perimetro(ladoa, ladob, ladoc);
		System.out.println("perimetro do triangulo: "+ result);
		
	}
}

//outra parte

public class Triangulo 
{
	private int a;
	private int b;
	private int c;
	private int tipo;
	
	public int getA() {
		return a;
	}
	public void setA(int a) {
		if(a<= 0)
		{
			this.a= 1;
		}
		else this.a = a;
	}
	public int getB() {
		return b;
	}
	public void setB(int b) 
	{
		if(b<= 0)
		{
			this.b= 1;
		}
		else this.b = b;
	}
	public int getC() {
		return c;
	}
	public void setC(int c) 
	{
		if(c<= 0)
		{
			this.c= 1;
		}
		else this.c = c;
	}
	
	public boolean possivel(int a, int b, int c)
	{
		if((a > b+c) || (b>a+c) || (c>a+b))
		{
			return false;
		}
		else return true;
	}
	
	public int perimetro(int a, int b, int c)
	{
		int resultado = a+b+c;
		return resultado;
	}
	
	public int alteraA(int num)
	{
		a = num;
		return a;
	}
	
	public int alteraB(int num)
	{
		b = num;
		return b;
	}
	
	public int alteraC(int num)
	{
		c = num;
		return c;
	}
	
	public int tipo_triangulo(int a, int b, int c)
	{
		if (a == b && b == c)
		{
			tipo = 1;
		}
		else if(a != b && b != c && c!=a)
		{
			tipo = 2;
		}
		else tipo = 3;
		
		return tipo;
	}
}

