def normalice_romaji_name(name):

    def count_spaces(name):

        num = 0

        for c in name:

            if c == ' ':
                num += 1
            else:
                break

        return num

    num_start = count_spaces(name)
    name_wt_start = name[num_start:][::-1]

    end_start = count_spaces(name_wt_start)
    name_wt_end = name_wt_start[end_start:][::-1]

    name_aux = name_wt_end.split(' ')
    last_name = name_aux[1]+name_aux[2]

    return name_aux[0].title()+' '+last_name.title()

