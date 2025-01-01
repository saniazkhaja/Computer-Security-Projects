package main;
import info.blockchain.api.blockexplorer.*;
import info.blockchain.api.blockexplorer.entity.*;
import info.blockchain.api.*;
import java.lang.*;

import java.util.*;
import java.io.IOException;

public class Checkpoint1 {

	private static final String BLOCK_HASH = "000000000000000f5795bfe1de0381a44d4d5ea2ad81c21d77f275bffa03e8b3";
    private Block block;

	// Constructor
	public Checkpoint1() {
        try {
            BlockExplorer blockExplorer = new BlockExplorer();
            this.block = blockExplorer.getBlock(BLOCK_HASH);
        } catch (IOException | APIException e) {
            e.printStackTrace();
        }
    }

	/**
	 * Blocks-Q1: What is the size of this block?
	 *
	 * Hint: Use method getSize() in Block.java
	 *
	 * @return size of the block
	 */
	public long getBlockSize() {
		// TODO implement me
		// return 0L;
		return block.getSize();
	}

	/**
	 * Blocks-Q2: What is the Hash of the previous block?
	 *
	 * Hint: Use method getPreviousBlockHash() in Block.java
	 *
	 * @return hash of the previous block
	 */
	public String getPrevHash() {
		// TODO implement me
		// return null;
		return block.getPreviousBlockHash();
	}

	/**
	 * Blocks-Q3: How many transactions are included in this block?
	 *
	 * Hint: To get a list of transactions in a block, use method
	 * getTransactions() in Block.java
	 *
	 * @return number of transactions in current block
	 */
	public int getTxCount() {
		// TODO implement me
		// return 0;
		return block.getTransactions().size();
	}

	/**
	 * Transactions-Q1: Find the transaction with the most outputs, and list the
	 * Bitcoin addresses of all the outputs.
	 *
	 * Hint: To get the bitcoin address of an Output object, use method
	 * getAddress() in Output.java
	 *
	 * @return list of output addresses
	 */
	public List<String> getOutputAddresses() {
		// TODO implement me
		// return null;
		List<Transaction> transactions = block.getTransactions();
        Transaction targetTx = null;
        int maxOutputs = -1;

        // Find the transaction with the most outputs
        for (Transaction tx : transactions) {
            int outputs = tx.getOutputs().size();
            if (outputs > maxOutputs) {
                maxOutputs = outputs;
                targetTx = tx;
            }
        }

        List<String> outputAddresses = new ArrayList<>();
        if (targetTx != null) {
            for (Output out : targetTx.getOutputs()) {
                String address = out.getAddress();
                if (address != null && !address.isEmpty()) {
                    outputAddresses.add(address);
                }
            }
        }

        return outputAddresses;
	}

	/**
	 * Transactions-Q2: Find the transaction with the most inputs, and list the
	 * Bitcoin addresses of the previous outputs linked with these inputs.
	 *
	 * Hint: To get the previous output of an Input object, use method
	 * getPreviousOutput() in Input.java
	 *
	 * @return list of input addresses
	 */
	public List<String> getInputAddresses() {
		// TODO implement me
		// return null;
		List<Transaction> transactions = block.getTransactions();
        Transaction targetTx = null;
        int maxInputs = -1;

        // Find the transaction with the most inputs
        for (Transaction tx : transactions) {
            int inputs = tx.getInputs().size();
            if (inputs > maxInputs) {
                maxInputs = inputs;
                targetTx = tx;
            }
        }

        List<String> inputAddresses = new ArrayList<>();
        if (targetTx != null) {
            for (Input in : targetTx.getInputs()) {
                Output prevOut = in.getPreviousOutput();
                if (prevOut != null) {
                    String address = prevOut.getAddress();
                    if (address != null && !address.isEmpty()) {
                        inputAddresses.add(address);
                    }
                }
            }
        }

        return inputAddresses;
	}

	/**
	 * Transactions-Q3: What is the bitcoin address that has received the
	 * largest amount of Satoshi in a single transaction?
	 *
	 * Hint: To get the number of Satoshi received by an Output object, use
	 * method getValue() in Output.java
	 *
	 * @return the bitcoin address that has received the largest amount of Satoshi
	 */
	public String getLargestRcv() {
		// TODO implement me
		// return null;
		List<Transaction> transactions = block.getTransactions();
        String largestAddr = null;
        long largestValue = -1;

        for (Transaction tx : transactions) {
            Map<String, Long> addrToValue = new HashMap<>();

            for (Output out : tx.getOutputs()) {
                String addr = out.getAddress();
                long value = out.getValue();
                if (addr != null && !addr.isEmpty()) {
                    addrToValue.put(addr, addrToValue.getOrDefault(addr, 0L) + value);
                }
            }

            for (Map.Entry<String, Long> entry : addrToValue.entrySet()) {
                if (entry.getValue() > largestValue) {
                    largestValue = entry.getValue();
                    largestAddr = entry.getKey();
                }
            }
        }

        return largestAddr;
	}

	/**
	 * Transactions-Q4: How many coinbase transactions are there in this block?
	 *
	 * Hint: In a coinbase transaction, getPreviousOutput() == null --> although this matches with the documentation, the result is wrong.
	 * Even if it's a coinbase transactions, it's not null during my test.
	 * I would recommend another work around that a coinbase transaction should have the sum of getPreviousOutput().getValue() equal to 0 because the total input should be 0.
	 * You can see an example of coinbase transaction here: https://www.blockchain.com/btc/tx/cdab676fe718b5155251f15b275c5f92ad965ee8557270d1eec07ccc42d4aaaf
	 * I'm using Java 1.8.0_242, if anyone made it success with getPreviousOutput() == null, please email me or send a campuswire post. Much appreciated!
	 *
	 * @return number of coin base transactions
	 */
	public int getCoinbaseCount() {
		// TODO implement me
		// return 0;
		int count = 0;
        List<Transaction> transactions = block.getTransactions();

        for (Transaction tx : transactions) {
            List<Input> inputs = tx.getInputs();
            long sum = 0L;

            for (Input in : inputs) {
                Output prevOut = in.getPreviousOutput();
                if (prevOut != null) {
                    sum += prevOut.getValue();
                }
            }

            if (sum == 0L) {
                count++;
            }
        }

        return count;
	}

	/**
	 * Transactions-Q5: What is the number of Satoshi generated in this block?
	 *
	 * @return number of Satoshi generated
	 */
	public long getSatoshiGen() {
		// TODO implement me
		// return 0L;
		long total = 0L;
        List<Transaction> transactions = block.getTransactions();

        for (Transaction tx : transactions) {
            List<Input> inputs = tx.getInputs();
            long sum = 0L;

            for (Input in : inputs) {
                Output prevOut = in.getPreviousOutput();
                if (prevOut != null) {
                    sum += prevOut.getValue();
                }
            }

            if (sum == 0L) {
                // This is a coinbase transaction
                for (Output out : tx.getOutputs()) {
                    total += out.getValue();
                }
            }
        }

        return total;
	}

}
