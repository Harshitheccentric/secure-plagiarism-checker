"""
Knuth-Morris-Pratt (KMP) String Matching Algorithm
Implementation for plagiarism detection system
"""

def compute_lps_array(pattern):
    """
    Compute the Longest Proper Prefix which is also Suffix (LPS) array
    
    Args:
        pattern (str): The pattern string
    
    Returns:
        list: LPS array for the pattern
    """
    length = 0  # Length of the previous longest prefix suffix
    lps = [0] * len(pattern)
    i = 1
    
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps

def kmp_search(pattern, text):
    """
    Search for pattern in text using KMP algorithm
    
    Args:
        pattern (str): Pattern to search for
        text (str): Text to search in
    
    Returns:
        list: List of starting indices where pattern is found
    """
    if not pattern or not text:
        return []
    
    # Compute LPS array
    lps = compute_lps_array(pattern)
    
    matches = []
    i = 0  # Index for text
    j = 0  # Index for pattern
    
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == len(pattern):
            matches.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return matches

def find_common_substrings(text1, text2, min_length=10):
    """
    Find common substrings between two texts using KMP
    
    Args:
        text1 (str): First text
        text2 (str): Second text
        min_length (int): Minimum length of substrings to consider
    
    Returns:
        list: List of tuples (substring, positions_in_text1, positions_in_text2)
    """
    common_substrings = []
    
    # Generate all substrings of text1 with minimum length
    for i in range(len(text1) - min_length + 1):
        for j in range(i + min_length, len(text1) + 1):
            substring = text1[i:j]
            
            # Search for this substring in text2 using KMP
            matches = kmp_search(substring, text2)
            
            if matches:
                # Found common substring
                common_substrings.append((substring, [i], matches))
    
    # Remove duplicates and sort by length (descending)
    unique_substrings = {}
    for substring, pos1, pos2 in common_substrings:
        if substring not in unique_substrings:
            unique_substrings[substring] = (pos1, pos2)
    
    # Convert back to list and sort by length
    result = [(substr, pos1, pos2) for substr, (pos1, pos2) in unique_substrings.items()]
    result.sort(key=lambda x: len(x[0]), reverse=True)
    
    return result

def plagiarism_score(text1, text2, method='word_based'):
    """
    Calculate plagiarism score between two texts
    
    Args:
        text1 (str): First text
        text2 (str): Second text
        method (str): 'word_based' or 'char_based' or 'line_based'
    
    Returns:
        dict: Dictionary containing similarity metrics
    """
    if not text1 or not text2:
        return {'similarity_percentage': 0.0, 'common_segments': 0, 'method': method}
    
    if method == 'word_based':
        return _word_based_similarity(text1, text2)
    elif method == 'char_based':
        return _char_based_similarity(text1, text2)
    elif method == 'line_based':
        return _line_based_similarity(text1, text2)
    else:
        return _word_based_similarity(text1, text2)  # Default

def _word_based_similarity(text1, text2):
    """Word-based similarity using KMP"""
    # Tokenize into words
    words1 = text1.lower().split()
    words2 = text2.lower().split()
    
    if not words1 or not words2:
        return {'similarity_percentage': 0.0, 'common_segments': 0, 'method': 'word_based'}
    
    # Find common word sequences
    common_sequences = []
    min_seq_length = 3  # Minimum 3 words in sequence
    
    for i in range(len(words1) - min_seq_length + 1):
        for length in range(min_seq_length, min(10, len(words1) - i + 1)):  # Max 10 words
            sequence = ' '.join(words1[i:i+length])
            text2_joined = ' '.join(words2)
            
            matches = kmp_search(sequence, text2_joined)
            if matches:
                common_sequences.append(sequence)
    
    # Calculate similarity
    if common_sequences:
        total_common_words = sum(len(seq.split()) for seq in set(common_sequences))
        max_words = max(len(words1), len(words2))
        similarity = min(100.0, (total_common_words / max_words) * 100)
    else:
        # Fallback: individual word matching
        common_words = set(words1) & set(words2)
        total_words = len(set(words1) | set(words2))
        similarity = (len(common_words) / total_words * 100) if total_words > 0 else 0.0
    
    return {
        'similarity_percentage': round(similarity, 2),
        'common_segments': len(set(common_sequences)),
        'method': 'word_based'
    }

def _char_based_similarity(text1, text2):
    """Character-based similarity using longest common substrings"""
    # Remove whitespace and convert to lowercase
    clean_text1 = ''.join(text1.lower().split())
    clean_text2 = ''.join(text2.lower().split())
    
    if not clean_text1 or not clean_text2:
        return {'similarity_percentage': 0.0, 'common_segments': 0, 'method': 'char_based'}
    
    # Find common substrings of reasonable length
    common_substrings = find_common_substrings(clean_text1, clean_text2, min_length=5)
    
    if common_substrings:
        # Calculate total length of common substrings (avoiding overlap)
        total_common_length = 0
        used_positions = set()
        
        for substring, _, _ in common_substrings:
            if not any(pos in used_positions for pos in range(len(substring))):
                total_common_length += len(substring)
                used_positions.update(range(len(substring)))
        
        max_length = max(len(clean_text1), len(clean_text2))
        similarity = (total_common_length / max_length) * 100
    else:
        similarity = 0.0
    
    return {
        'similarity_percentage': round(similarity, 2),
        'common_segments': len(common_substrings),
        'method': 'char_based'
    }

def _line_based_similarity(text1, text2):
    """Line-based similarity using KMP"""
    lines1 = [line.strip().lower() for line in text1.split('\n') if line.strip()]
    lines2 = [line.strip().lower() for line in text2.split('\n') if line.strip()]
    
    if not lines1 or not lines2:
        return {'similarity_percentage': 0.0, 'common_segments': 0, 'method': 'line_based'}
    
    common_lines = 0
    
    for line1 in lines1:
        # Search for exact line matches
        if kmp_search(line1, '\n'.join(lines2)):
            common_lines += 1
    
    max_lines = max(len(lines1), len(lines2))
    similarity = (common_lines / max_lines) * 100 if max_lines > 0 else 0.0
    
    return {
        'similarity_percentage': round(similarity, 2),
        'common_segments': common_lines,
        'method': 'line_based'
    }

if __name__ == "__main__":
    # Test KMP algorithm
    text = "ABABDABACDABABCABCABCABCABC"
    pattern = "ABABCABC"
    
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    
    matches = kmp_search(pattern, text)
    print(f"Pattern found at positions: {matches}")
    
    # Test plagiarism detection
    text1 = "The quick brown fox jumps over the lazy dog. This is a test sentence."
    text2 = "A quick brown fox jumps over the lazy dog. This sentence is for testing."
    
    score = plagiarism_score(text1, text2, 'word_based')
    print(f"\nPlagiarism Score: {score}")
    
    # Test with identical texts
    score2 = plagiarism_score(text1, text1, 'word_based')
    print(f"Identical texts score: {score2}")