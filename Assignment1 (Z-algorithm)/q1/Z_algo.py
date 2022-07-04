"""
Name: Wong Cheok Foong
Std ID: 29801028
"""

def z_algorithm(string):
    """
    creates z-array for prefix matching
    :complexity: O(N), where N is length of string
    """
    z_array = len(string) * [None]
    z_box = [0,0] # stores the first and last index of the matching substring to the prefix in the string
    z_array[0] = len(string)

    for i in range(1, len(string)):
        prefix_length = 0
        index = i
        substring = i # right end of z_box
        count = 0

        if index > z_box[0] and index <= z_box[1]:
            k = index - z_box[0]
            remaining = z_box[1] - index + 1

            if z_array[k] < remaining:
                z_array[i] = z_array[k]

            elif z_array[k] > remaining:
                z_array[i] = remaining

            #if z_array[k] == remaining
            else:
                # compute Z[R+1] first where R is right most of z_box
                after_R = z_box[1] + 1

                #if Z[R+1] is out of range
                if after_R >= len(string):
                    z_array[i] = z_array[k]

                # if Z[R+1] is not out of range
                else:
                    prefix_length += z_array[k]
                    while after_R < len(string) and string[after_R] == string[prefix_length]:
                        count += 1
                        prefix_length += 1
                        after_R += 1

                    # if a substring/z_box exist
                    if after_R > index:
                        z_box[0] = index
                        z_box[1] = after_R -1

                    z_array[i] = z_array[k] + count

        else:
            while substring < len(string) and string[substring] == string[prefix_length]:
                count += 1
                prefix_length += 1
                substring += 1

            # if a substring/z_box exist
            if substring > index:
                z_box[0] = index
                z_box[1] = substring -1
            z_array[i] = count

    return z_array


def reverse_z_algorithm(string):
    """
    creates z-array for suffix matching
    :complexity: O(N), where N is length of string
    """
    z_array = len(string) * [None]
    N = len(string) - 1
    z_array[N] = len(string)
    z_box = [N,N] # stores the first and last index of the matching substring to the prefix in the string

    for i in range(N -1, -1, -1):
        suffix = N
        index = i
        substring = i # right end of z_box
        count = 0

        if index < z_box[0] and index >= z_box[1]:
            k = N - abs(index - z_box[0])
            remaining = abs(z_box[1] - index - 1)

            if z_array[k] < remaining:
                z_array[i] = z_array[k]

            elif z_array[k] > remaining:
                z_array[i] = remaining

            #if z_array[k] == remaining
            else:
                # compute Z[R+1] first
                after_R = z_box[1] - 1

                #if Z[R+1] is out of range
                if after_R < 0:
                    z_array[i] = z_array[k]

                else:
                    suffix -= z_array[k]
                    while after_R >= 0 and string[after_R] == string[suffix]:
                        count += 1
                        suffix -= 1
                        after_R -= 1

                    # if a substring/z_box exist
                    if after_R < index:
                        z_box[0] = index
                        z_box[1] = after_R +1

                    z_array[i] = z_array[k] + count

        else:
            while substring >= 0 and string[substring] == string[suffix]:
                count += 1
                suffix -= 1
                substring -= 1

            # if a substring/z_box exist
            if substring < index:
                z_box[0] = index
                z_box[1] = substring +1
            z_array[i] = count

    return z_array
