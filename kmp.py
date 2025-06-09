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
    """Word-based similarity using KMP - fixed to avoid over-counting"""
    # Tokenize into words
    words1 = text1.lower().split()
    words2 = text2.lower().split()
    
    if not words1 or not words2:
        return {'similarity_percentage': 0.0, 'common_segments': 0, 'method': 'word_based'}
    
    # Find exact sentence/phrase matches first (most reliable)
    lines1 = [line.strip().lower() for line in text1.strip().split('\n') if line.strip()]
    lines2 = [line.strip().lower() for line in text2.strip().split('\n') if line.strip()]
    
    exact_line_matches = 0
    total_lines = max(len(lines1), len(lines2))
    
    for line1 in lines1:
        if line1 in lines2:
            exact_line_matches += 1
    
    # If we have significant exact line matches, use that as primary metric
    if exact_line_matches > 0:
        line_similarity = (exact_line_matches / total_lines) * 100
    else:
        line_similarity = 0
    
    # Find common word sequences (3+ words) without over-counting
    common_sequences = []
    min_seq_length = 3
    max_seq_length = 8  # Reasonable upper bound
    
    # Use a greedy approach: find longest sequences first
    found_sequences = set()  # To avoid duplicates
    
    for seq_length in range(max_seq_length, min_seq_length - 1, -1):
        for i in range(len(words1) - seq_length + 1):
            sequence = ' '.join(words1[i:i+seq_length])
            
            # Skip if this sequence is already covered by a longer sequence
            if any(sequence in longer_seq for longer_seq in found_sequences):
                continue
                
            text2_joined = ' '.join(words2)
            matches = kmp_search(sequence, text2_joined)
            
            if matches:
                found_sequences.add(sequence)
                common_sequences.append(sequence)
    
    # Calculate sequence-based similarity
    if common_sequences:
        total_common_words = sum(len(seq.split()) for seq in common_sequences)
        # Use harmonic mean of text lengths for better balance
        avg_length = 2 * len(words1) * len(words2) / (len(words1) + len(words2))
        sequence_similarity = min(100.0, (total_common_words / avg_length) * 100)
    else:
        sequence_similarity = 0
    
    # Individual word overlap (fallback)
    common_words = set(words1) & set(words2)
    all_words = set(words1) | set(words2)
    word_similarity = (len(common_words) / len(all_words) * 100) if all_words else 0.0
    
    # Combine metrics with weights
    # Prioritize exact line matches, then sequences, then individual words
    if exact_line_matches > 0:
        final_similarity = line_similarity * 0.7 + sequence_similarity * 0.3
    else:
        final_similarity = max(sequence_similarity, word_similarity)
    
    return {
        'similarity_percentage': round(min(final_similarity, 100.0), 2),
        'common_segments': len(common_sequences),
        'method': 'word_based'
    }

def _char_based_similarity(text1, text2):
    """Character-based similarity using optimized longest common substrings"""
    # Remove whitespace and convert to lowercase
    clean_text1 = ''.join(text1.lower().split())
    clean_text2 = ''.join(text2.lower().split())
    
    if not clean_text1 or not clean_text2:
        return {'similarity_percentage': 0.0, 'common_segments': 0, 'method': 'char_based'}
    
    # Use a more efficient approach: dynamic programming for LCS
    def longest_common_substring_length(s1, s2, min_length=5):
        """Find length of longest common substring using optimized approach"""
        if len(s1) > len(s2):
            s1, s2 = s2, s1  # Ensure s1 is shorter
        
        max_length = 0
        common_substrings = []
        
        # Only check substrings of reasonable length to avoid timeout
        max_check_length = min(50, len(s1))  # Limit to prevent exponential growth
        
        for i in range(len(s1) - min_length + 1):
            for j in range(i + min_length, min(i + max_check_length, len(s1) + 1)):
                substring = s1[i:j]
                if substring in s2:  # Simple string search instead of KMP for short strings
                    if len(substring) > max_length:
                        max_length = len(substring)
                    common_substrings.append(substring)
        
        return max_length, len(set(common_substrings))
    
    max_common_length, num_substrings = longest_common_substring_length(clean_text1, clean_text2)
    
    if max_common_length > 0:
        max_length = max(len(clean_text1), len(clean_text2))
        similarity = (max_common_length / max_length) * 100
    else:
        similarity = 0.0
    
    return {
        'similarity_percentage': round(similarity, 2),
        'common_segments': num_substrings,
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