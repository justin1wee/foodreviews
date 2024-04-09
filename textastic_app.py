

from textastic import Textastic

def main():
    tt = Textastic()

    tt.load_text('txt/futago-udon-boston.txt', 'futago')
    tt.load_text('txt/happy-lamb-hot-pot-boston-4.txt', 'happylamb')
    tt.load_text('txt/kaju-tofu-house-allston-2.txt', 'kaju')
    tt.load_text('txt/mala-restaurant-boston.txt', 'mala')
    tt.load_text('txt/peach-farm-boston.txt', 'peach')
    tt.load_text('txt/pho-le-restaurant-boston.txt', 'pho')
    tt.load_text('txt/santouka-back-bay-boston-2.txt', 'santouka')
    tt.load_text('txt/seoul-soulongtang-boston.txt', 'seoul')
    tt.load_text('txt/tora-japanese-restaurant-boston.txt', 'tora')

    tt.sentiment_scatter(['futago', 'happylamb', 'kaju', 'mala', 'peach', 'pho',
                            'santouka', 'seoul', 'tora'])
    tt.wordcount_sankey(['futago', 'happylamb', 'kaju', 'mala', 'peach', 'pho',
                            'santouka', 'seoul', 'tora'], k=7)
    tt.generate_word_cloud(['futago', 'happylamb', 'kaju', 'mala', 'peach', 'pho',
                            'santouka', 'seoul', 'tora', 'tora'])

if __name__ == '__main__':
    main()