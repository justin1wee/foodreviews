

from textastic import Textastic
import pprint as pp
import textastic_parsers as tp

def main():
    tt = Textastic()

    tt.load_text('file.txt', 'A')
    tt.load_text('file1.txt', 'B')
    tt.load_text('file2.txt', 'C')
    tt.load_text('myfile.json', 'J', parser=tp.json_parser)

    pp.pprint(tt.data)
    tt.compare_num_words()


if __name__ == '__main__':
    main()