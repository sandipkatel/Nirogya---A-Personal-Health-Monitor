def merge_dic(S, L, R):
    i = j = k = 0
    while i < len(L) and j < len(R):
        if L[i][1] >= R[j][1]:  # Compare based on probabilities
            S[k] = L[i]
            i += 1
        else:
            S[k] = R[j]
            j += 1
        k += 1
    
    while i < len(L):
        S[k] = L[i]
        i += 1
        k += 1
    
    while j < len(R):
        S[k] = R[j]
        j += 1
        k += 1

def sort_dic(S):
    n = len(S)
    if n > 1:
        mid = n // 2
        L, R = S[:mid], S[mid:]
        sort_dic(L)
        sort_dic(R)
        merge_dic(S, L, R)
