'''
Follows the recipe in wiki. Is a good explanation

https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch

TODO:
- deal with when dictionary becomes full

To finish:
- look up other designs of solutions

In real solution
- design a solution
- check that the input is well formed

Created on 28 Dec 2016

@author: chris
'''
import string

from collections import OrderedDict

INITIAL_BIN_DIGITS = 5

def main():
    
    message = 'ABABABABAB#'
    
    compressed_message = compress(message)
    
    message_ret = decompress(compressed_message)
    
    # todo - merge all into one, deal with size
    
    print(message_ret)
    print("".join(message_ret)==message)
    

def split_message(compressed_message):
    
    extended_dict = gen_initial_dict()
    bin_digs = INITIAL_BIN_DIGITS
    
    max_val = max(extended_dict.values())
    
    I = 0
    while(True):
        for count, ind in enumerate(range(I, len(compressed_message), bin_digs)):
            
            ind_end = ind+bin_digs
            
            new_val = max_val + count + 1
            
            new_bin_digs = len(format(new_val, 'b'))
            
            yield compressed_message[ind:ind_end]
            
            if ind_end == len(compressed_message):
                # this assumes well formed input - need to check that
                raise StopIteration
            
            if new_bin_digs > bin_digs:
                I = ind_end
                bin_digs = new_bin_digs
                break

    
def decompress(compressed_message):
    
    message = []
    
    split_mess_gen = split_message(compressed_message)
    
    extended_dictionary = list(gen_initial_dict().keys())
    
    i_next = len(extended_dictionary) + 1
    bin_code = split_mess_gen.__next__()
    
    code = int(bin_code,2)
    
    conjecture = extended_dictionary[code]
    message.append(conjecture)
    
    for bin_code in split_mess_gen:
        
        code = int(bin_code,2)
        
        if code != len(extended_dictionary):
            output_sequence = extended_dictionary[code]
        
            full = conjecture + output_sequence[0]
            
        else:
            full = conjecture + conjecture[0]
            
            output_sequence = full
        
        extended_dictionary.append(full)
        i_next += 1
        conjecture = output_sequence
        
        message.append(output_sequence)
        
    return "".join(message)
    

def compress(message):
    compressed_message = []
    
    extended_dict = gen_initial_dict()
    bin_digs = INITIAL_BIN_DIGITS
    
    current_seq = message[0]
    
    for next_char in message[1:]:
        extended_key = current_seq + next_char
        
        if not extended_key in extended_dict.keys():
            encode_val = extended_dict[current_seq]
            compressed_message.append(format(encode_val, '0' + str(bin_digs) + 'b'))
            new_val = max(extended_dict.values()) + 1
            extended_dict[extended_key] = new_val 
            current_seq = next_char
            
            new_bin_digs = len(format(new_val, 'b'))
            if new_bin_digs > bin_digs:
                bin_digs = new_bin_digs
                
        else:
            current_seq = extended_key
    
        if next_char is '#':
            encode_val = extended_dict[next_char]
            compressed_message.append(format(encode_val, '0' + str(bin_digs) + 'b'))
            break
   
    return "".join(compressed_message)


def gen_initial_dict():
    
    letters = string.ascii_uppercase
    stop_char = '#'
    
    initial_dict = OrderedDict()
    initial_dict[stop_char] = 0
    
    for i, let in enumerate(letters):
        initial_dict[let] = i + 1
        
    return initial_dict
    
if __name__ == '__main__':
    main()