import os, sys
import numpy as np
import urllib
from multiprocessing.dummy import Pool as ThreadPool
import time

# USAGE
# >> python download_pictures.py [destination-folder]



##################################################################
# Automatic generated params, modify in case something looks wrong
HOST = '$HOST$'
FILES = '$FILES$'
##################################################################




# Usually you do not need to modify these params
SITE = 'http://%s/static/media/' % HOST
COUNT = 0
MAX = 0
BARLENGTH = 40
THREADS = 1  # with one works just fine
MAIN_FOLDER = os.path.abspath('.')


def update_progress(step, end):
    """Shows a fancy progresbar"""
    progress = step / float(end)
    barLength = BARLENGTH # Modify this to change the length of the progress bar
    status = "Downloading..."
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), int(progress*100), status)
    sys.stdout.write(text)
    sys.stdout.flush()


def read_pictures():
    """Builds an array full of tuples with the pictures and its paths
    format: (path, picture)
    """
    pictures = []
    for filename in FILES:
        with open(filename, 'r') as file:
            for line in file:
                # removes breakline
                line = line.rstrip('\n').rstrip('\r')
                # splits into filename and label
                try:
                    picture_path, label = line.split(' ')
                except ValueError:
                    print "Skip file %s" % (line)
                    pass
                complete_path = picture_path.split('/')
                path = complete_path[:-1]
                picture = complete_path[-1]
                pictures.append((os.path.sep.join(path), picture))
    return pictures


def create_folders(struct):
    """Creates all the folders needed"""
    for info in struct:
        folder = info[0]
        abs_path = os.path.join(MAIN_FOLDER, folder)
        if not os.path.exists(abs_path):
            #print "%s doesn't exists" %(abs_path)
            os.makedirs(abs_path)



def download_set(set):
    global COUNT
    for num, info in enumerate(set):
        folder = info[0]
        pic_name = info[1]
        url = SITE + '/'.join(info)
        abs_path = os.path.join(MAIN_FOLDER, folder, pic_name)
        urllib.urlretrieve(url, abs_path)

        COUNT += 1
        if num % 10 == 0:
            update_progress(COUNT, MAX)
    update_progress(COUNT, MAX)



def download_pictures(struct):
    if THREADS > 1:
        data = np.array_split(struct, THREADS)
    else:
        data = [struct]

    pool = ThreadPool(THREADS)
    pool.map(download_set, data)

    #for set in data:
    #    download_set(set)



def main():
    global MAX
    pictures = read_pictures()
    MAX = len(pictures)
    create_folders(pictures)
    init = time.clock()
    download_pictures(pictures)
    end = time.clock()

    print "%i pictures with %i workers, %f seconds" % (MAX, THREADS, end-init)


if __name__ == '__main__':
    global MAIN_FOLDER
    if len(sys.argv) > 1:  # we have output folder
        MAIN_FOLDER = sys.argv[1]

    main()

