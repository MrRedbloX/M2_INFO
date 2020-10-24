from pickle import load

'''
Load the content of feeds.data and print it.
'''
if __name__ == '__main__':
    try:
        with open('./output/feeds.data', 'rb') as f:
            print(load(f))
    except:
        print('The file feeds.data does not exists.')
