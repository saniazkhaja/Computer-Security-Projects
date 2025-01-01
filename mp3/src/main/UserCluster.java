package main;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.Math;

class UnionFind {
    private Map<Long, Long> parent;

    public UnionFind(Map<String, Long> keyMap) {
        parent = new HashMap<>();
        for (Long userId : keyMap.values()) {
            parent.put(userId, userId);
        }
    }

    public Long find(Long userId) {
        if (!parent.get(userId).equals(userId)) {
            parent.put(userId, find(parent.get(userId))); // Path compression
        }
        return parent.get(userId);
    }

    public void union(Long user1, Long user2) {
        Long root1 = find(user1);
        Long root2 = find(user2);
        if (!root1.equals(root2)) {
            parent.put(root2, root1); // Merge the sets
        }
    }
}

public class UserCluster {
	private Map<Long, List<String>> userMap; // Map a user id to a list of
												// bitcoin addresses
	private Map<String, Long> keyMap; // Map a bitcoin address to a user id
	private long currentUserId; // Unique user id for each cluster
	private List<String> transactions; // To store transactions for processing
	private Set<String> inAddresses; // Addresses that appear as inputs
	private Set<String> outAddresses; // Addresses that appear as outputs

	int hash_index = 0;
	int addr_index = 1;
	int val_index  = 2;
	int type_index = 3;
	int column_len = 4;

	public UserCluster() {
		userMap = new HashMap<Long, List<String>>();
		keyMap = new HashMap<String, Long>();
		currentUserId = 0;
		transactions = new ArrayList<>();
		inAddresses = new HashSet<>();
        outAddresses = new HashSet<>();
	}

	/**
	 * Read transactions from file
	 *
	 * @param file
	 * @return true if read succeeds; false otherwise
	 */
	public boolean readTransactions(String file) {
		// TODO implement me
		// return false;
		try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(" ");
                if (parts.length < column_len) {
                    return false;
                }
                String txHash = parts[hash_index];
                String address = parts[addr_index];
                String type = parts[type_index];
				
				transactions.add(line); // Store the transaction for further processing
	
				// Ensure that all input and output addresses are added to keyMap
				if (type.equals("in") || type.equals("out")) {
					keyMap.putIfAbsent(address, currentUserId++); // Ensure unique mapping
				}
				// Track input and output addresses
				if (type.equals("in")) {
					inAddresses.add(address);
				} else if (type.equals("out")) {
					outAddresses.add(address);
				}
            }
            return true; // Successful read
        } catch (IOException e) {
            e.printStackTrace();
            return false; // Read failure
        }
	}
	

	/**
	 * Merge addresses based on joint control
	 */
	public void mergeAddresses() {
		// TODO implement me
		// Initialize Union-Find structure
		UnionFind uf = new UnionFind(keyMap);

		// Map to group all input addresses per transaction
		Map<String, List<String>> txToInAddresses = new HashMap<>();
        
        // Group all input addresses by transaction hash
        for (String transaction : transactions) {
            String[] columns = transaction.split(" ");
			if (columns.length < column_len) {
                continue; // Skip invalid transactions
            }
            if (columns[type_index].equals("in")) {
                String txHash = columns[hash_index];
                String address = columns[addr_index];
                txToInAddresses.computeIfAbsent(txHash, k -> new ArrayList<>()).add(address);
            }
        }

        // Perform unions for addresses in the same transaction
        for (List<String> inAddrList : txToInAddresses.values()) {
            if (inAddrList.size() > 1) {
                Long firstUserId = keyMap.get(inAddrList.get(0));
                for (int i = 1; i < inAddrList.size(); i++) {
                    Long currentUserId = keyMap.get(inAddrList.get(i));
                    uf.union(firstUserId, currentUserId);
                }
            }
        }

        // Assign addresses to clusters based on Union-Find results
        for (String address : keyMap.keySet()) {
            Long userId = keyMap.get(address);
            if (inAddresses.contains(address)) {
                Long rootUser = uf.find(userId);
                userMap.computeIfAbsent(rootUser, k -> new ArrayList<>()).add(address);
            }
        }

        // Assign output-only addresses to their own unique clusters
        for (String address : outAddresses) {
            // If an address appears both as input and output, it's already handled
            if (!inAddresses.contains(address)) {
                Long userId = keyMap.get(address);
                userMap.putIfAbsent(userId, new ArrayList<>());
                userMap.get(userId).add(address);
            }
        }
	}

	/**
	 * Return number of users (i.e., clusters) in the transaction dataset
	 *
	 * @return number of users (i.e., clusters)
	 */
	public int getUserNumber() {
		// TODO implement me
		// return 0;
		return userMap.size();
	}

	/**
	 * Return the largest cluster size
	 *
	 * @return size of the largest cluster
	 */
	public int getLargestClusterSize() {
		// TODO implement me
		// return 0;
		return userMap.values().stream()
		.mapToInt(List::size)
		.max()
		.orElse(0);
	}

	public boolean writeUserMap(String file) {
		try {
			BufferedWriter w = new BufferedWriter(new FileWriter(file));
			for (long user : userMap.keySet()) {
				List<String> keys = userMap.get(user);
				w.write(user + " ");
				for (String k : keys) {
					w.write(k + " ");
				}
				w.newLine();
			}
			w.flush();
			w.close();
		} catch (IOException e) {
			System.err.println("Error in writing user list!");
			e.printStackTrace();
			return false;
		}

		return true;
	}

	public boolean writeKeyMap(String file) {
		try {
			BufferedWriter w = new BufferedWriter(new FileWriter(file));
			for (String key : keyMap.keySet()) {
				w.write(key + " " + keyMap.get(key) + "\n");
				w.newLine();
			}
			w.flush();
			w.close();
		} catch (IOException e) {
			System.err.println("Error in writing key map!");
			e.printStackTrace();
			return false;
		}

		return true;
	}

	public boolean writeUserGraph(String txFile, String userGraphFile) {
	     try {
                        BufferedReader r1 = new BufferedReader(new FileReader(txFile));
                        Map<String, Long> txUserMap = new HashMap<String, Long>();
                        String nextLine;
                        while ((nextLine = r1.readLine()) != null) {
                                String[] s = nextLine.split(" ");
                                if (s.length < column_len) {
                                        System.err.println("Invalid format: " + nextLine);
                                        r1.close();
                                        return false;
                                }
                                if (s[type_index].equals("in") && !txUserMap.containsKey(s[hash_index])) { // new transaction
                                        Long user;
                                        if ((user=keyMap.get(s[addr_index])) == null) {
                                                System.err.println(s[addr_index] + " is not in the key map!");
                                                System.out.println(nextLine);
                                                r1.close();
                                                return false;
                                        }
                                        txUserMap.put(s[hash_index], user);
                                }
                        }
                        r1.close();

                        BufferedReader r2 = new BufferedReader(new FileReader(txFile));
                        BufferedWriter w = new BufferedWriter(new FileWriter(userGraphFile));
                        while ((nextLine = r2.readLine()) != null) {
                                String[] s = nextLine.split(" ");
                                if (s.length < column_len) {
                                        System.err.println("Invalid format: " + nextLine);
                                        r2.close();
                                        w.flush();
                                        w.close();
                                        return false;
                                }
                                if (s[type_index].equals("out")) {
                                        if(txUserMap.get(s[hash_index]) == null) {
                                                System.err.println("Did not find input transaction for Tx: " + s[hash_index]);
                                                r2.close();
                                                w.flush();
                                                w.close();
                                                return false;
                                        }
                                        long inputUser = txUserMap.get(s[hash_index]);
                                        Long outputUser;
                                        if ((outputUser=keyMap.get(s[addr_index])) == null) {
                                                System.err.println(s[addr_index] + " is not in the key map!");
                                                r2.close();
                                                w.flush();
                                                w.close();
                                                return false;
                                        }
                                        w.write(inputUser + "," + outputUser + "," + s[val_index] + "\n");
                                }
                        }
                        r2.close();
                        w.flush();
                        w.close();
                } catch (IOException e) {
                        e.printStackTrace();
                }
                return true;

	}

}

