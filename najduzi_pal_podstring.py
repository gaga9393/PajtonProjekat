
def najduzi_palindromski_substring(string):
    
    n = len(string) 
    
    if (n == 0):
        return 0, 0
    
    start=0
    maxLength = 1
    for i in range(n):
        low = i - 1
        high = i + 1
        while (high < n and string[high] == string[i] ):                               
            high=high+1
       
        while (low >= 0 and string[low] == string[i] ):                 
            low=low-1
       
        while (low >= 0 and high < n and string[low] == string[high] ):
          low=low-1
          high=high+1
         
     
        length = high - low - 1
        if (maxLength < length):
            maxLength = length
            start=low+1
     
    return start, maxLength
     
if __name__ == "__main__":


    string = input("Unesi string: ")
    palindromStart, palinromLength = najduzi_palindromski_substring(string)
    print(f"Najduzi palindromski string: {string[palindromStart:palindromStart+palinromLength]}; lenght: {palinromLength}")
