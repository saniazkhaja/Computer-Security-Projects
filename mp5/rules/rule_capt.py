import itertools

def check_capt(pw1,pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (boolean): if pw1 and pw2 can be transformed by this category of rule
    #e.g. pw1 = abcdE, pw2= abCde, output =True
    #e.g. pw1 = boat, pw2 = boat, output = False (The two inputs are already identical)

    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************

    return pw1.lower() == pw2.lower() and pw1 != pw2

def check_capt_transformation(pw1, pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    #consider if head char is capt transformed, if tail char is capt transformed, and # of chars that has been capt transformed in total
    #example pw1 = abcde, pw2 = AbcDe, transformation = head\t2 (head char is capt transformed, in total 2 chars are capt transformed)
    #example pw1 = abcdE, pw2 = AbcDe, transformation = head\ttail\t3 (head char and tail chars are capt transformed, in total 3 chars are capt transformed)
    #example pw1 = abcde, pw2 = abcDe, transformation = 1 (in total 1 chars are capt transformed)
    
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    head_transformed = False
    tail_transformed = False
    total_transformed = 0
    
    # Check head transformation (first character)
    if pw1[0].isupper() != pw2[0].isupper():
        head_transformed = True
        total_transformed += 1
    
    # Check tail transformation (last character)
    if pw1[-1].isupper() != pw2[-1].isupper():
        tail_transformed = True
        total_transformed += 1
    
    # Check the rest of the characters in the middle
    for i in range(1, len(pw1)-1):
        if pw1[i].isupper() != pw2[i].isupper():
            total_transformed += 1
    
    # Build the transformation string
    transformation = ""
    if head_transformed:
        transformation += "head\t"
    if tail_transformed:
        transformation += "tail\t"
    
    if total_transformed > 0:
        transformation += str(total_transformed)
    else:
        transformation = "0"  # No transformations
    
    return transformation.strip()

def apply_capt_transformation(ori_pw, transformation):
    # Check if the transformation involves the head and/or tail
    head_transformed = "head" in transformation
    tail_transformed = "tail" in transformation

    # Parse the transformation string to get the number of transformations required
    parts = transformation.split("\t")
    total_transformed = int(parts[-1]) if parts[-1].isdigit() else 0

    if total_transformed < 1:
        return []  # Return an empty list if no transformations are needed

    result = set()

    # Helper function to apply transformation only to alphabetic characters
    def transform_password(comb, fixed_positions=set()):
        transformed_pw = ""
        for i in range(len(ori_pw)):
            # Transform only if the position is in `comb` and it's alphabetic
            if i in fixed_positions:
                transformed_pw += ori_pw[i].swapcase()
            elif i in comb and ori_pw[i].isalpha():
                transformed_pw += ori_pw[i].swapcase()
            else:
                transformed_pw += ori_pw[i]
        return transformed_pw

    # If head is transformed, ensure the first character is transformed
    if head_transformed and not tail_transformed:
        transformable_positions = [i for i in range(1, len(ori_pw) - 1) if ori_pw[i].isalpha()]
        for comb in itertools.combinations(transformable_positions, total_transformed - 1):
            result.add(transform_password(comb, fixed_positions={0}))

    # If tail is transformed, ensure the last character is transformed
    if tail_transformed and not head_transformed:
        transformable_positions = [i for i in range(1, len(ori_pw) - 1) if ori_pw[i].isalpha()]
        for comb in itertools.combinations(transformable_positions, total_transformed - 1):
            result.add(transform_password(comb, fixed_positions={len(ori_pw) - 1}))

    # If both head and tail are transformed
    if head_transformed and tail_transformed:
        transformable_positions = [i for i in range(1, len(ori_pw) - 1) if ori_pw[i].isalpha()]
        for comb in itertools.combinations(transformable_positions, total_transformed - 2):
            result.add(transform_password(comb, fixed_positions={0, len(ori_pw) - 1}))

    # If neither head nor tail is transformed (only internal characters)
    if not head_transformed and not tail_transformed:
        transformable_positions = [i for i in range(1, len(ori_pw) - 1) if ori_pw[i].isalpha()]
        for comb in itertools.combinations(transformable_positions, total_transformed):
            result.add(transform_password(comb))

    return sorted(list(result))  # Sort the results for consistency



# Example test cases
# if __name__ == "__main__":
#     print("\nTesting apply_capt_transformation function...")
    
#     # Test case for head\t2 (only head characters are transformed, 2 total)
#     print(apply_capt_transformation("1bcde", "head\t2"))  
#     # Expected output: ['ABcde', 'AbCde', 'AbcDe']
    
#     # Test case for head\ttail\t3 (head and tail transformed, 3 total)
#     print(apply_capt_transformation("abcde", "head\ttail\t3"))  
#     # Expected output: ['ABcdE', 'AbCdE', 'AbcDE']
    
#     # Test case for just 1 character transformed
#     print(apply_capt_transformation("abcde", "1"))  
#     # Expected output: ['Abcde', 'aBcde', 'abCde', 'abcDe', 'abcdE']

#     print(apply_capt_transformation("password", "2"))