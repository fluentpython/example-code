import java.math.BigInteger;

class CorrectFactorial {
    public static BigInteger factorial(BigInteger n) {
        return n.compareTo(BigInteger.ONE) <= 0 ? BigInteger.ONE
                    : n.multiply(factorial(n.subtract(BigInteger.ONE)));
    }

    public static void main(String args[]) {
        BigInteger upperBound = new BigInteger("25"); 
        for (BigInteger i = BigInteger.ONE;
                i.compareTo(upperBound) <= 0;
                i = i.add(BigInteger.ONE)) {
            System.out.println(i + "! = " + factorial(i));
        }
    }
}

/* output:

1! = 1
2! = 2
3! = 6
4! = 24
5! = 120
6! = 720
7! = 5040
8! = 40320
9! = 362880
10! = 3628800
11! = 39916800
12! = 479001600
13! = 6227020800
14! = 87178291200
15! = 1307674368000
16! = 20922789888000
17! = 355687428096000
18! = 6402373705728000
19! = 121645100408832000
20! = 2432902008176640000
21! = 51090942171709440000
22! = 1124000727777607680000
23! = 25852016738884976640000
24! = 620448401733239439360000
25! = 15511210043330985984000000

*/
