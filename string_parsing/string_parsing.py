def join_with_space(word_list):
    ret_string = ""

    for word in word_list:
        word_with_space = word + " "
        ret_string += word_with_space

    if len(ret_string) == 0:
        return ret_string

    return ret_string.strip()