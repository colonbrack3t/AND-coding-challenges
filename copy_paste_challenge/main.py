import unittest
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
processed_strs= [
  "Given test cases : ",
  "the big red fox jumps over the big red fox jumps lazy dog.",
  "the tall oak tree towers over the lush green meadow.",
  "the sun shines down on the sun shines down the busy the sun shines down on the sun shines down.",
  "the tall oak tree towers over the lush green meadow.",
  "a majestic lion searches for a majestic lion in the tall grass.",
  "Twinkling in the dark, the shimmering star shines bright.",
  "a fluffy white cloud drifts  across the sky, a fluffy white cloud drifts ",
  "\nOther edge cases:",
  "Twinkling in the dark, Twinkling shines bright.",
  "Twinkling in the dark, the shimmering star shines bright.",
  "Twinkling in the dark, the shimmering the shimmering star shines bright.",
  "Twinkling in the dark, star shines bright.",

]
import re
ctr_c = '[CTRL+C]'
ctr_x = '[CTRL+X]'
ctr_v = '[CTRL+V]'
ctr_c_r = r'([A-Za-z ]+)\[CTRL\+C\]'
ctr_x_r = r'([\S ]+)\[CTRL\+X\]'
ctr_v_r = r'\[CTRL\+V\]'

def get_last_cut(all_ctr_xs,before_paste):
    end_index = len(all_ctr_xs[-1]) + before_paste.index(all_ctr_xs[-1]) + len(ctr_x)
    before_paste = before_paste[end_index:]
    copy_string = all_ctr_xs[-1]
    while ctr_x in copy_string:
        ctr_x_index = len(ctr_x) + copy_string.index(ctr_x)
        copy_string = copy_string[ctr_x_index:]
    copy_string = copy_string.replace(ctr_c, '')
    return before_paste , copy_string
def handle_paste(s):
    # string to be pasted to ctr_v
    copy_string = ""
    # available string before ctr_v command. Shortened if encountered with ctr_x
    before_paste = s[:s.index(ctr_v)]
    all_ctr_xs = re.findall(ctr_x_r,before_paste)
    if len(all_ctr_xs) > 0:
        before_paste , copy_string = get_last_cut(all_ctr_xs, before_paste)
    all_ctr_cs = re.findall(ctr_c_r,before_paste)
    if len(all_ctr_cs) > 0:    
        copy_string = ''.join(all_ctr_cs)
    s = before_paste.replace(ctr_c, '') + copy_string + s[s.index(ctr_v) + len(ctr_v):]
    return s 
def challenge(s):
    if not ctr_c in s and not ctr_x in s:
        s = s.replace(ctr_v,'')
        return s
        
    while ctr_v in s:
        s = handle_paste(s)
    # removes any ctr_c that were placed at the start of the s string. 
    # these wont be captured by the regex so need to be removed at the end
    s = s.replace(ctr_c,'').replace(ctr_x,'')
    return s

class UnitTests(unittest.TestCase):
    def test_regex_strings(self):
        def assert_1_find(re_str, str):
            self.assertEqual(len(re.findall(re_str, str)), 1)

        # ctr_c regex requires text to capture
        assert_1_find(ctr_c_r,"text" + ctr_c)
        assert_1_find(ctr_v_r,ctr_v)
        # ctr_x regex requires text to capture
        assert_1_find(ctr_x_r,"cut text" + ctr_x)
        # test grouping works for copy
        string_before_copy_command = "this is a copied string"
        ctr_c_group = re.findall(ctr_c_r, string_before_copy_command + ctr_c)
        self.assertEqual(len(ctr_c_group) , 1)
        self.assertEqual(ctr_c_group[0] , string_before_copy_command)
        # test groupin works for cut
        # cut should also consider the ctr_c command in its cut.
        string_before_cut_command = string_before_copy_command + ctr_c
        ctr_x_group = re.findall(ctr_x_r, string_before_cut_command + ctr_x)
        self.assertEqual(len(ctr_x_group) , 1)
        self.assertEqual(ctr_x_group[0] , string_before_cut_command)

    def test_get_last_cut(self):
        test_cases = {
           "test_ignore_ctrc":
            [   {"prompt": "[CTRL+C]abababcdcdcdcd",
                "answer" : "abababcdcdcdcd" }, 
                {"prompt": "ababa[CTRL+C]cdcdcd",
                "answer" : "ababacdcdcd"},
                {"prompt": "ababacdcdcd[CTRL+C]",
                "answer" : "ababacdcdcd"},
                {"prompt": "ababa[CTRL+C]cdcdcd[CTRL+C]efefef",
                "answer" : "ababacdcdcdefefef"}
            ]
           ,
           "test_ignores_prev_cuts":
            [   {"prompt": "[CTRL+X]abababcdcdcdcd",
                "answer" : "abababcdcdcdcd"}, 
                {"prompt": "ababa[CTRL+X]",
                "answer" : ""},
                {"prompt": "ababa[CTRL+X]cdcdcd",
                "answer" : "cdcdcd"}, 
                {"prompt": "ababa[CTRL+X]cdc[CTRL+X]dcd",
                "answer" : "dcd"},
            ]
           ,
           "test_cuts_and_copies":[   
               {"prompt": "[CTRL+X]abababcd[CTRL+C]cdcdcd",
                "answer" : "abababcdcdcdcd"}, 
                {"prompt": "ab[CTRL+C]aba[CTRL+X]",
                "answer" : ""},
                {"prompt": "ababa[CTRL+X]cd[CTRL+C]cdcd",
                "answer" : "cdcdcd"}, 
                {"prompt": "ababa[CTRL+X]c[CTRL+C]dc[CTRL+X]dc[CTRL+C]d",
                "answer" : "dcd"},
            ],
            
         }
        for test_name, tests in test_cases.items():
            for t in tests:
                before_paste = t['prompt'] + ctr_x
                all_ctr_xs = re.findall(ctr_x_r,before_paste)
                _ , copy_string = get_last_cut(all_ctr_xs,before_paste)
                self.assertEqual(copy_string , t['answer'], 
                msg = f"test_name : {test_name}, test index : {tests.index(t)}, all_ctr_xs : {all_ctr_xs}, before_paste : {before_paste}"
                
                )
    def test_strs(self):
        for sentence, computed_sentence in zip(strs,processed_strs):
            self.assertEqual(computed_sentence , challenge(sentence))
      

if __name__ == '__main__':
    for s in strs:
        print(challenge(s))
    unittest.main()
