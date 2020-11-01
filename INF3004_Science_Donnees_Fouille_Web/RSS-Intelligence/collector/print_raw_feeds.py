from shelve import open as shopen

'''
Load the content of feeds.data and print it.
'''
if __name__ == '__main__':
    try:
        f = shopen('./output/feeds')
        for key in f.keys():
            print(f[key], '\n')
    except:
        print('The file feeds does not exists.')
