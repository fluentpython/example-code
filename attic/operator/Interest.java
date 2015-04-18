/***
Compound interest function with ``BigDecimal``

Equivalent in Python:

    def compound_interest(principal, rate, periods):
        return principal * ((1 + rate) ** periods - 1)

***/

import java.math.BigDecimal;

public class Interest {

    static BigDecimal compoundInterest(BigDecimal principal, BigDecimal rate, int periods) {
        return principal.multiply(BigDecimal.ONE.add(rate).pow(periods).subtract(BigDecimal.ONE));
    }

    public static void main(String[] args) {
        BigDecimal principal = new BigDecimal(1000);
        BigDecimal rate = new BigDecimal("0.06");
        int periods = 5;        
        System.out.println(compoundInterest(principal, rate, periods));
    }

}
