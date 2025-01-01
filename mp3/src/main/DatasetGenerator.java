package main;
import info.blockchain.api.blockexplorer.*;
import info.blockchain.api.blockexplorer.entity.*;
import info.blockchain.api.*;
import java.lang.*;

import java.util.*;
import java.io.FileWriter;
import java.io.IOException;


public class DatasetGenerator {
	String file;

	public DatasetGenerator(String file) {
		this.file = file;
	}

	public boolean writeTransactions() {
		// TODO implement me
    	// return false;
		try (FileWriter writer = new FileWriter(file)) {
            BlockExplorer blockExplorer = new BlockExplorer();

            // Get blocks with height between [265852, 266085]
            long startHeight = 265852; // Start height for 10/25/2013
            long endHeight = 266085;   // End height for 10/25/2013

            // Loop through each block in the height range
            for (long height = startHeight; height <= endHeight; height++) {
                List<Block> blocks = blockExplorer.getBlocksAtHeight(height);

                for (Block block : blocks) {
                    List<Transaction> transactions = block.getTransactions();

                    for (Transaction transaction : transactions) {
                        // Ignore coinbase transactions
                        if (transaction.getInputs() != null && !isCoinbaseTransaction(transaction)) {
                            // Process inputs
                            for (Input input : transaction.getInputs()) {
                                String previousOutputAddress = input.getPreviousOutput().getAddress();
                                long previousOutputValue = input.getPreviousOutput().getValue();
                                String inputRecord = generateInputRecord(transaction.getHash(), previousOutputAddress, previousOutputValue);
                                writer.write(inputRecord + "\n");
                            }

                            // Process outputs
                            for (Output output : transaction.getOutputs()) {
                                String outputAddress = output.getAddress();
                                long outputValue = output.getValue();
                                String outputRecord = generateOutputRecord(transaction.getHash(), outputAddress, outputValue);
                                writer.write(outputRecord + "\n");
                            }
                        }
                    }
                }
            }
            return true; // Return true if successful
        } catch (IOException e) {
            e.printStackTrace();
            return false; // Return false if an error occurs
        } catch (APIException e) {
            e.printStackTrace();
            return false; // Return false if API call fails
        }
	}

	private boolean isCoinbaseTransaction(Transaction transaction) {
        // A coinbase transaction has a single input without a previous output
        return transaction.getInputs().size() == 1 && transaction.getInputs().get(0).getPreviousOutput() == null;
    }

	/**
	 * Generate a record in the transaction dataset
	 *
	 * @param txHash
	 *            Transaction hash
	 * @param address
	 *            Previous output address of the input
	 * @param value
	 *            Number of Satoshi transferred
	 * @return A record of the input
	 */
	private String generateInputRecord(String txHash,
			String address, long value) {
		return txHash + " " + address + " " + value + " in";
	}

	/**
	 * Generate a record in the transaction dataset
	 *
	 * @param txHash
	 *            Transaction hash
	 * @param address
	 *            Output bitcoin address
	 * @param value
	 *            Number of Satoshi transferred
	 * @return A record of the output
	 */
	private String generateOutputRecord(String txHash,
			String address, long value) {
		return txHash + " " + address + " " + value + " out";
	}
}