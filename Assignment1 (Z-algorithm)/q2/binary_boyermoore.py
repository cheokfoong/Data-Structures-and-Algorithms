"""
Name: Wong Cheok Foong
Std ID: 29801028
"""

import sys
from Z_algo import*

def read_file(filename):
    file = open(filename)
    string = file.readline()

    return string

def bad_character(pattern):
    """
    bad character implementation for boyermoore
    :complexity: O(kM), where k is number of characters and M is length of pattern
    """
    unique_character = []

    # discover all unique characters
    for i in pattern:
        if i not in unique_character:
            unique_character.append(i)

    # create matrix table for the unique characters
    matrix_table = [None] * len(unique_character)
    for i in range(len(matrix_table)):
        matrix_table[i] = [0] * (len(pattern) + 1)
        matrix_table[i][0] = unique_character[i]

    # for each unique character in the matrix table the right most position is determined for each index
    # according to the length of pattern
    for i in range(len(pattern), 0, -1):
        for j in range(len(matrix_table)):
            if pattern[i - 1] == matrix_table[j][0]:
                k = i
                while k <= len(pattern):
                    if matrix_table[j][k] == 0:
                        matrix_table[j][k] = i
                        k += 1
                    else:
                        break
    return matrix_table


def Good_suffix(pattern):
    """
    good suffix implementation for boyermoore
    :complexity: O(N) wher N is length of pattern
    """
    z_array = reverse_z_algorithm(pattern)

    m = len(pattern)
    good_suffix_array = [0] * (m + 1)

    for i in range(m - 1):
        j = m - z_array[i]
        good_suffix_array[j] = i

    # longest suffix of pat[i+1...m] that match prefix of pat[1...m-i]
    patt_array = z_algorithm(pattern)
    matched_prefix = [0] * len(pattern)

    for a in range(len(pattern) - 1, -1, -1):
        if (patt_array[a] + a) == len(pattern):
            matched_prefix[a] = patt_array[a]
        else:
            if a == len(pattern) - 1:
                matched_prefix[a] = 0
            else:
                matched_prefix[a] = matched_prefix[a + 1]

    return (good_suffix_array, matched_prefix)



def boyermoore(text, pattern):
    """
    boyermoore optimization using bad character, good suffix and galils
    :complexity: O(m + n), where m is length of pattern and n is length of text
    """
    # call bad character table
    BC_table = bad_character(pattern)
    #print(BC_table)

    # call good suffix and matched prefix table
    good_suffix, matched_prefix = Good_suffix(pattern)
    #print(good_suffix)
    #print(matched_prefix)

    pat = len(pattern)
    total_shift = 0  # total number of shifts
    total_comparison = 0  # total number of comparisons
    moved_position = 0  # starting position of pattern at 0 before shifting
    out_of_bound = False  # if shifting causes out of bound
    output = []  # list of positions where pattern matches the text

    # These variables are used for galil's optimization
    galil = False  # if a prefix pat[1..] that matches txt[..j + m − 1] occurs after a shift
    GS_shift_galil = 0  # Number of good suffix shift is used to know when to skip comparsion in next iteration
    matching_char = 0  # this is the number of matching characters before mismatch in good suffix

    # pattern matching for text and pattern
    while pat + moved_position < len(text):
        all_match = True  # when pattern fully matches characters in text
        shifted = False  # Has a shift occured
        BC_shift = 0  # number of shifting position using bad_character
        GS_shift = 0  # number of shifting position using good_suffix
        skip_compare = False  # skips the repeating occurence of pat in text from galil

        #print("t_c: ", total_comparison)
        # scans pattern from right to left
        for i in range(pat, 0, -1):
            # skipping due to galil's optimization
            if skip_compare == True:
                i = i - matching_char
            if i > 0:

                # galil's optimization
                if galil == True and (pat - i) == GS_shift_galil:
                    i = i - matching_char
                    galil = False
                    skip_compare = True

                if i > 0:
                    total_comparison += 1

                    # if mismatch occurs
                    if pattern[i - 1] != text[i - 1 + moved_position]:
                        galil = False
                        all_match = False

                        # calculate shift using bad_character for mismatch
                        for j in range(len(BC_table)):
                            if BC_table[j][0] == text[i - 1 + moved_position]:
                                right_most = BC_table[j][i]

                                # After shifting pattern by the rightmost and it does not exceed the len(text)
                                if (pat + moved_position + i - right_most) <= len(text):
                                    BC_shift = i - right_most
                                    shifted = True
                                    break

                                else:
                                    out_of_bound = True

                            # If the character is not found in bad_character table
                            # then shift pattern by 1 position past mismatch
                            elif j == len(BC_table) - 1 and BC_table[j][0] != text[i - 1 + moved_position]:
                                if pat + moved_position + i <= len(text):
                                    BC_shift = i
                                    shifted = True
                                    break
                                else:
                                    out_of_bound = True

                        # First character cannot be mismatch in order to use good_suffix
                        if i != pat:
                            # calculate shift using good_suffix for mismatch
                            if good_suffix[i] > 0 and pat + moved_position + (pat - 1) - good_suffix[i] <= len(text):
                                GS_shift = (pat - 1) - good_suffix[i]
                                GS_shift_galil = GS_shift
                                matching_char = pat - i
                                shifted = True
                                galil = True

                            # matched_prefix
                            elif good_suffix[i] == 0 and pat + moved_position + pat - matched_prefix[i] <= len(text):
                                GS_shift = pat - matched_prefix[i]
                                GS_shift_galil = GS_shift
                                matching_char = matched_prefix[i]
                                shifted = True
                                galil = True
                            else:
                                out_of_bound = True

                # If shifting causes out of bound
                if out_of_bound == False:
                    # Stop comparing if shifting has been done
                    if shifted == True:
                        total_shift += 1
                        moved_position += max(BC_shift, GS_shift)
                        break
                else:
                    break

        # If characters matches entire pattern
        if all_match == True:
            if i == 0:
                output.append(i + moved_position)
            else:
                output.append(i-1 + moved_position)

            # shifting using bad_character
            if pat + moved_position + 1 <= len(text):
                BC_shift = 1
            else:
                out_of_bound = True

            # shifting using matched_prefix
            if pat + moved_position + pat - matched_prefix[1] <= len(text):
                GS_shift = pat - matched_prefix[1]
            else:
                out_of_bound = True

            # If shifting causes out of bound
            if out_of_bound == False:
                total_shift += 1
                moved_position += max(BC_shift, GS_shift)

        # stop while loop
        if out_of_bound == True:
            break

    # create txt file for output
    file = open("output_binary_boyermoore.txt", "w")
    for i in range(len(output)):
        file.write(str(output[i]) + "\n")
    file.close

    return (total_comparison, total_shift)



if __name__ == "__main__":

    argument_00 =sys.argv[0]

    argument_01 = sys.argv[1]

    argument_02 = sys.argv[2]

    boyermoore(read_file(argument_01), read_file(argument_02))
