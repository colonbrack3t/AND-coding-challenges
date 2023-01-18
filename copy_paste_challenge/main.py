strs = [
  "Given test cases : ",
  "the big red[CTRL+C] fox jumps[CTRL+C] over [CTRL+V] lazy dog.",
  "[CTRL+V]the tall oak tree towers over the lush green meadow.",
  "the sun shines down[CTRL+C] on [CTRL+V][CTRL+C] the busy [CTRL+V].",
  "[CTRL+V]the tall oak[CTRL+C] tree towers over the lush green meadow.",
  "a majestic lion[CTRL+C] searches for [CTRL+V] in the tall grass.",
  "the shimmering star[CTRL+X]Twinkling in the dark, [CTRL+V] shines bright.",
  "[CTRL+X]a fluffy white cloud drifts [CTRL+V][CTRL+C] across the sky, [CTRL+V]",
  "\nOther edge cases:",
  "the shimmering star[CTRL+X]Twinkling[CTRL+C] in the dark, [CTRL+V] shines bright.",
  "the shimmering [CTRL+C]star[CTRL+X]Twinkling in the dark, [CTRL+V] shines bright.",
  "the shimmering [CTRL+C][CTRL+V]star[CTRL+X]Twinkling in the dark, [CTRL+V] shines bright.",
  "the[CTRL+X] shimmering [CTRL+X]star[CTRL+X]Twinkling in the dark, [CTRL+V] shines bright.",

]

import re
ctr_c = '[CTRL+C]'
ctr_x = '[CTRL+X]'
ctr_v = '[CTRL+V]'
ctr_c_r = r'([A-Za-z ]+)\[CTRL\+C\]'
ctr_x_r = r'([\S ]+)\[CTRL\+X\]'
ctr_v_r = r'\[CTRL\+V\]'

def challenge(s):
    if not ctr_c in s and not ctr_x in s:
        s = s.replace(ctr_v,'')
        return s
        
    while ctr_v in s:
        copy_string = ""
        before_paste = s[:s.index(ctr_v)]
        all_ctr_xs = re.findall(ctr_x_r,before_paste)
        if len(all_ctr_xs) > 0:
            end_index = len(all_ctr_xs[-1]) + before_paste.index(all_ctr_xs[-1]) + len(ctr_x)
            before_paste = before_paste[end_index:]
            copy_string = all_ctr_xs[-1]
            while ctr_x in copy_string:
                ctr_x_index = len(ctr_x) + copy_string.index(ctr_x)
                copy_string = copy_string[ctr_x_index:]
            copy_string = copy_string.replace(ctr_c, '')
        all_ctr_cs = re.findall(ctr_c_r,before_paste)
        #print(all_ctr_xs, "\n",before_paste,"\n",copy_string)
        if len(all_ctr_cs) > 0:    
            copy_string = ''.join(all_ctr_cs)
        s = before_paste.replace(ctr_c, '') + copy_string + s[s.index(ctr_v) + len(ctr_v):]
    s = s.replace(ctr_c,'').replace(ctr_x,'')
    return s

if __name__ == '__main__':
    for s in strs:
        print(challenge(s))
