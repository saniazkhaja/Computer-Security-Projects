import itertools

#a more complete leet_list
#leet_list = [{'4', 'a', '@', '/\\', '/-\\'}, {'b', '|3', '8', '|o'}, {'<', 'K', 'g', 'S', '9', '6', 'c', '('}, {'0', '()', '{}', 'o', '[]'}, {'!', '|', '][', '#', ')-(', '1', 'i', 'l', '}-{', '|-|', '+', 't', ']-[', 'h', '(-)', '7'}, {'5', 's', '$'}, {'+', 't'}, {'/\\/\\', 'm', '/v\\', '/|\\', '/\\\\', '|\\/|', '(\\/)', "|'|'|"}, {'\\|/', '\\|\\|', '\\^/', '//', 'w', '|/|/', '\\/\\/'}, {'|\\|', '|\\\\|', 'n', '/|/', '/\\/'}, {'u', '|_|'}, {'2', '(\\)', 'z'}, {'(,)', 'q', 'kw'}, {'v', '|/', '\\|', '\\/', '/'}, {'k', '/<', '|{', '\\<', '|<'}, {'<|', 'o|', '|)', '|>', 'd'}, {'f', 'ph', '|=', 'p#'}, {'l', '|_'}, {'j', 'y', '_|'}, {'}{', 'x', '><'}, {"'/", 'y', '`/'}, {'p', '|D', 'r', '|2'}, {'r', '|Z', '|?'}, {'e', '3'}]
leet_list = [{"@","a"},{"3","e"},{"1","i"},{"0","o"},{"$","s"},{"+","t"},{"4","a"},{"5","s"},{"|","i"},{"!","i"}]
def check_leet(pw1,pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (boolean): if pw1 and pw2 can be transformed by this category of rule
    #e.g. pw1 = abcde, pw2 = @bcd3 , output = True
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************

    # First, check if the lengths of the passwords are the same
    if len(pw1) != len(pw2):
        return False
    
    # Now, check each character of pw1 and pw2 for leet transformation
    for c1, c2 in zip(pw1, pw2):
        # If the characters are the same, no need to check further
        if c1 == c2:
            continue
        
        # Check if the characters c1 and c2 can be mapped according to the leet list
        found_match = False
        for transformation in leet_list:
            if c1 in transformation and c2 in transformation:
                found_match = True
                break
        
        if not found_match:
            return False
    
    return True

def check_leet_transformation(pw1, pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    #example: pw1=abcd3 pw2 = @bcde, transformation = 3e\ta@ because pw1->pw2:3->e and a->@ and '3e'<'a@' for the order
    #for simplicity, duplicate item is allowed. example: pw1=abcda pw2 = @bcd@, transformation = a@\ta@ 
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    transformation_pairs = []
    
    for c1, c2 in zip(pw1, pw2):
        for leet_set in leet_list:
            if c1 in leet_set and c2 in leet_set and c1 != c2:
                transformation_pairs.append(f"{c1}{c2}")
    
    # Sort pairs lexicographically and join with tab
    transformation_pairs.sort()
    return "\t".join(transformation_pairs)

def apply_leet_transformation(ori_pw, transformation):
    # Split the transformation string into pairs
    leet_pairs = transformation.split("\t")
    
    # Generate forward and backward transformations from each pair
    forward_transformations = [(pair[0], pair[1]) for pair in leet_pairs]
    backward_transformations = [(pair[1], pair[0]) for pair in leet_pairs]
    
    results = set()  # Using a set to avoid duplicate results

    # Function to apply multiple transformations in all possible combinations
    def apply_combined_transformations(pw, transformations):
        transformed_variants = set()

        # Collect positions for each character in transformations
        transform_positions = {}
        for char, replacement in transformations:
            if char in pw:
                positions = [i for i, c in enumerate(pw) if c == char]
                transform_positions[char] = (positions, replacement)

        # Use itertools.product to generate all combinations of transformations
        for transformation_set in itertools.product(*[
                [(char, pos, replacement) for pos in positions] 
                for char, (positions, replacement) in transform_positions.items()
            ]):
            
            # Create a copy of the original password
            pw_variant = list(pw)

            # Apply each transformation in the current combination
            for char, pos, replacement in transformation_set:
                pw_variant[pos] = replacement
            
            # Add the transformed variant to the set
            transformed_variants.add("".join(pw_variant))

        return transformed_variants
    
    # Step 1: Apply forward transformations with combination handling
    forward_results = apply_combined_transformations(ori_pw, forward_transformations)
    results.update(forward_results)

    # Step 2: Apply backward transformations with similar handling
    backward_results = apply_combined_transformations(ori_pw, backward_transformations)
    results.update(backward_results)

    # Filter out the original password
    results.discard(ori_pw)

    # Return the final results as a list
    return list(results)

# if __name__ == "__main__":
#     # Test cases for apply_leet_transformation function
#     print("\nTesting apply_leet_transformation function...")
#     print(apply_leet_transformation("aacde@3", "3e\ta@"))  
#     # Expected output: ['@acde@e', 'a@cde@e', 'aacd3a3']
#     print(apply_leet_transformation("admin", "i1\ta@"))  
#     print(apply_leet_transformation("password", "0o\ta@"))
#     print(apply_leet_transformation("p@ssword", "@a\t0o"))
#     print(apply_leet_transformation("keyboard", "e3\to0\ta4")) # k3yb04rd
