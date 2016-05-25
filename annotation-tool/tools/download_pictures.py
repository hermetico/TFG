import os
import sys
import urllib
import time

# USAGE
# >> python download_pictures.py
# optinal parameters
# --path <output path>
# --threads <num threads to download>



##################################################################
# Auto generated params, modify in case something looks wrong
HOST = '$HOST$'
FILES = '$FILES$'
EXTRA_PATH = '$PATH$'
##################################################################




# Usually you do not need to modify these params
SITE = 'http://%s/static/media/' % HOST
COUNT = 0
MAX = 0
BARLENGTH = 40




def update_progress(step, end):
    """Shows a fancy progressbar"""
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
                if EXTRA_PATH:
                    # we should extract the extra_path before trying to download the picture etc..
                    picture_path = picture_path.replace(EXTRA_PATH + os.path.sep, "")
                complete_path = picture_path.split('/')
                path = complete_path[:-1]
                picture = complete_path[-1]
                pictures.append((path, picture))
    return pictures


def create_folders(struct):
    """Creates all the folders needed"""
    for info in struct:
        folder = os.path.sep.join(info[0])
        abs_path = os.path.join(MAIN_FOLDER, folder)
        if not os.path.exists(abs_path):
            #print "%s doesn't exists" %(abs_path)
            os.makedirs(abs_path)



def download_set(set):
    global COUNT
    for num, info in enumerate(set):
        url_relative_path = '/'.join(info[0] + [info[1]])
        local_relative_path = os.path.sep.join(info[0] + [info[1]])
        abs_path = os.path.join(MAIN_FOLDER, local_relative_path)
        urllib.urlretrieve(SITE + '/' + url_relative_path, abs_path)

        COUNT += 1
        if num % 5 == 0:
            update_progress(COUNT, MAX)
    update_progress(COUNT, MAX)



def download_pictures(struct):
    if THREADS > 1:
        # just in case people do not have numpy or use weird o.s.'s
        import numpy as np
        from multiprocessing.dummy import Pool as ThreadPool
        data = np.array_split(struct, THREADS)
        pool = ThreadPool(THREADS)
        pool.map(download_set, data)
    else:
        # 1 thread should always work
        data = [struct]
        for set in data:
            download_set(set)



def main():
    global MAX
    print "Reading pictures ..."
    pictures = read_pictures()
    MAX = len(pictures)
    print "Creating folder structure ..."
    create_folders(pictures)
    print "%i pictures are going do be downloaded using %i worker(s)" % (MAX, THREADS)
    init = time.clock()
    download_pictures(pictures)
    end = time.clock()
    print
    print "%i pictures downloaded with %i worker(s) in  %f seconds" % (MAX, THREADS, end-init)


if __name__ == '__main__':
    global MAIN_FOLDER, THREADS

    if '--path' in sys.argv:
        MAIN_FOLDER = sys.argv[sys.argv.index('--path') + 1]
    else:
        MAIN_FOLDER = os.path.abspath('.')

    if '--threads' in sys.argv:
        THREADS = int(sys.argv[sys.argv.index('--threads') + 1])
    else:
        THREADS = 1  # with 1 works just fine, with 4 is obviously faster

    main()

