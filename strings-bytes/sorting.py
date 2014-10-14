import locale

def check(sorted_list):
    return 'CORRECT' if fruits == sorted_list else 'WRONG'

fruits = ['açaí', 'acerola', 'atemoia', 'cajá', 'caju']

print(locale.getlocale(locale.LC_COLLATE))

print('manual_sort ', fruits)

plain_sort = sorted(fruits)

print('plain_sort  ', plain_sort, check(plain_sort))

locale_sort1 = sorted(fruits, key=locale.strxfrm)

print('locale_sort1', locale_sort1, check(locale_sort1))

locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')

print('locale set to:', locale.getlocale(locale.LC_COLLATE))

locale_sort2 = sorted(fruits, key=locale.strxfrm)

print('locale_sort2', locale_sort2, check(locale_sort2))
