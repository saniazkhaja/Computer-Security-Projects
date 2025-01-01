def check_substring(pw1,pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (boolean): if pw1 and pw2 can be considered as substring of the other 
    # eg. pw1 = abc, pw2 = abcd, output true
    # eg. pw1 = abcde, pw2 = abcd, output true
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    return pw1 in pw2 or pw2 in pw1

def check_substring_transformation(pw1, pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    #example: pw1=123hello!!, pw2=hello, output=head\t123\ttail\t!!
    #example: pw1=hello!!, pw2=hello, output=head\t\ttail\t!!
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    if pw2 in pw1:
        # Find the position of pw2 in pw1
        index = pw1.find(pw2)
        head = pw1[:index]  # The part before pw2
        tail = pw1[index + len(pw2):]  # The part after pw2
        return f"head\t{head}\ttail\t{tail}"
    elif pw1 in pw2:
        index = pw2.find(pw1)
        head = pw2[:index]
        tail = pw2[index + len(pw1):]
        return f"head\t{head}\ttail\t{tail}"
    else:
        return ""  # No substring transformation possible

def guess_target_as_substring(ori_pw):
    #the first transformation applied in rule_substring
    #guess the possible passwords as a substring
    #decide to only consider the substring from head or from tail
    #e.g. pw1=abc123, output = [a,ab,abc,abc1,abc12,3,23,123,c123,bc123]
    #in transformation dictionary, the transformation = 'special_trans_as_substring'
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************

    substrings = []

    # Generate substrings by removing characters from the head
    for i in range(1, len(ori_pw)):
        substrings.append(ori_pw[i:])  # Substring from index `i` to the end

    # Generate substrings by removing characters from the tail
    for i in range(1, len(ori_pw)):
        substrings.append(ori_pw[:len(ori_pw) - i])  # Substring from start to `len(ori_pw) - i`

    return substrings

def apply_substring_transformation(ori_pw, transformation):
    #ori_pw (string): input password that needs to be transformed
    #transformation (string): transformation in string
    #output (list of string): list of passwords that after transformation
    #add head string to head, add tail string to tail
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    
    # Check if the transformation is "special_trans_as_substring"
    if transformation == "special_trans_as_substring":
        return guess_target_as_substring(ori_pw)
    
    # Otherwise, handle normal substring transformation
    parts = transformation.split("\t")
    head, tail = parts[1], parts[3]  # Extract head and tail from transformation
    
    # Combine head and tail to generate the transformation
    return [head + ori_pw + tail]

# Example test cases
# if __name__ == "__main__":
#     print(apply_substring_transformation("hello", "head\t123\ttail\t!!")) # Output: ["123hello!!"]
#     print(apply_substring_transformation("hello", "head\t\ttail\t!!")) # Output: ["hello!!"]
#     ori_pw_example = "abcd"
#     print(guess_target_as_substring(ori_pw_example)) # The final output should be ["bcd", "cd", "d", "abc", "ab", "a"].