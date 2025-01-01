import java.math.BigInteger;
import java.util.Random;
/**
 * Created by naveed on 2/15/15.
 */
public class Server {
    public static void main(String[] args) 
    {
        Boolean debug=false;
    	if(args.length != 2) { System.out.println("Invalid arguments, exiting..."); return; }
    	
        String filename = args[0];
        String clientFilename = args[1];
	
        Inputs inputs = new Inputs(filename);
        BigInteger[] serverInputs = inputs.getInputs();
        BigInteger[] encryptedPolyCoeffs = (BigInteger[])StaticUtils.read(clientFilename);
        BigInteger publicKey = (BigInteger)StaticUtils. read("ClientPK.out");
        Paillier paillier = new Paillier();
        paillier.setPublicKey(publicKey);
        BigInteger[] encryptedPolyEval = new BigInteger[serverInputs.length];
        /* TODO: implement server-side protocol here.
         * For each sj in serverInputs:
			- Pick a random rj
			- Homomorphically evaluate P(sj)
			- Compute E_K(rj P(sj) + sj)
			- Set encryptedPolyEval[j] = E_K(rj P(sj) + sj)
        */
 	    // ------ Your code goes here. --------
         for (int j = 0; j < serverInputs.length; j++) {
            // 1: Pick a random rj
            BigInteger rj = randomBigInt(paillier.n);

            // Server input: sj
            BigInteger sj = serverInputs[j];

            // 2: Homomorphically evaluate P(sj)
            BigInteger P_sj = paillier.Encryption(BigInteger.ZERO); // Start with encryption of 0
            BigInteger sj_pow = BigInteger.ONE;  // Keep track of powers of sj

            // 2: Compute P(sj) = sum(encryptedCoeff[i] * sj^i)
            for (int i = 0; i < encryptedPolyCoeffs.length; i++) {
                // 2b: Homomorphically compute E_K(al * sj^l)
                BigInteger al = encryptedPolyCoeffs[i];
                BigInteger term = paillier.const_mul(al, sj_pow); // E_K(al * sj^l)
                
                // 2c: Homomorphically sum the terms
                P_sj = paillier.add(P_sj, term);
                
                // Update sj_pow for the next iteration (sj^i)
                sj_pow = sj_pow.multiply(sj);
            }

            // 2d: Compute E_K(rj * P(sj) + sj)
            BigInteger rj_P_sj = paillier.const_mul(P_sj, rj); // E_K(P(sj))^rj
            BigInteger encrypted_sj = paillier.Encryption(sj); // E_K(sj)
            BigInteger finalValue = paillier.add(rj_P_sj, encrypted_sj); // E_K(rj * P(sj) + sj)

            // Store the encrypted result in the array
            encryptedPolyEval[j] = finalValue;
        }
        
        StaticUtils.write(encryptedPolyEval, clientFilename+".out");
    }
    //This is not cryptographically secure random number.
    public static BigInteger randomBigInt(BigInteger n) 
    {
        Random rand = new Random();
        BigInteger result = new BigInteger(n.bitLength(), rand);
        while( result.compareTo(n) >= 0 ) {
            result = new BigInteger(n.bitLength(), rand);
        }
        return result;
    }
}