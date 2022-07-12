import os
import shutil
import logging
import traceback

from progress.bar import ShadyBar

arscan_path = 'Arscan/'
arscan_temp_path = 'Arscan.temp/'

#create logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='log')
logging.info('               ')
logging.info('+++++++++++++++')
logging.info('start programm')

folders_temp = []
folders = []
folders_numbers = []

#read folders

for item in os.listdir(arscan_path):
    if os.path.isdir(os.path.join(arscan_path, item)):
        folders.append(item)
for item in os.listdir(arscan_temp_path):
    if os.path.isdir(os.path.join(arscan_temp_path, item)):
        folders_temp.append(item)
logging.info('read folders ok')

####
folders.sort()
folders_temp.sort()
####

#check folders names. if not standart name of folder - del folder from list
i_in_while = 0
while i_in_while < len(folders):
    try:
        if folders[i_in_while][-4] == '.' and folders[i_in_while][-9] == '-':
            i = 0
        else:
            del folders[i_in_while]
            continue
    except:
        del folders[i_in_while]
        continue
    i_in_while += 1
logging.info('check and del folder names ok')

#create associate list folders names <---> folders numbers for folders
for folder_name in folders:
    num = []
    num.append('')
    num.append('')
    num_num = 0
    i_in_while = 3
    while i_in_while < len(folder_name):
        if folder_name[i_in_while] == '.':
            i_in_while += 1
        elif folder_name[i_in_while] == ' ':
            i_in_while += 3
            num_num = 1
        num[num_num] += folder_name[i_in_while]
        i_in_while += 1
    folders_numbers.append(num)
    del num
    num_num = 0
logging.info('create associate list ok')
####

#folders numbers strings to ints
i_in_while = 0
while i_in_while < len(folders_numbers):
    folders_numbers[i_in_while][0] = int(folders_numbers[i_in_while][0])
    folders_numbers[i_in_while][1] = int(folders_numbers[i_in_while][1])
    i_in_while += 1
logging.info('folders numbers string to ints ok')

#folders names temp strings to ints
i_in_while = 0
while i_in_while < len(folders_temp):
    try:
        folders_temp[i_in_while] = int(folders_temp[i_in_while])
    except:
        del folders_temp[i_in_while]
        continue
    i_in_while += 1
logging.info('folders names temp strings to ints ok')

#associate folders and folders_numbers <---> folders_temp
i_in_while = 0
bar = ShadyBar('', max=len(folders_temp))
while i_in_while < len(folders_temp):
    j_in_while = 0
    while j_in_while < len(folders):
        if (folders_temp[i_in_while] >= folders_numbers[j_in_while][0] and
                folders_temp[i_in_while] <= folders_numbers[j_in_while][1]):
            try:
                shutil.move(arscan_temp_path+'00'+str(folders_temp[i_in_while]), arscan_path+str(folders[j_in_while]))
            except:
                logging.warning('folder already exists. copy files from folder')
                err = traceback.format_exc()
                err = err[-15:-1]
                if err == 'already exists':
                    file_list = os.listdir(arscan_temp_path+'00'+str(folders_temp[i_in_while]))
                    if file_list:
                        k_in_while = 0
                        while k_in_while < len(file_list):
                            try:
                                shutil.move(arscan_temp_path+'00'+str(folders_temp[i_in_while])+'/'+file_list[k_in_while],
                                        arscan_path+str(folders[j_in_while])+'/00'+str(folders_temp[i_in_while]))
                                k_in_while += 1
                            except:
                                logging.warning('file already exists. rename file')
                                err_1 = traceback.format_exc()
                                err_1 = err_1[-15:-1]
                                if err_1 == 'already exists':
                                    os.system('mv '+arscan_temp_path+'00'+str(folders_temp[i_in_while])+'/'+file_list[k_in_while]+' '+
                                            arscan_temp_path+'00'+str(folders_temp[i_in_while])+'/'+file_list[k_in_while]+'1')
                                else:
                                    logging.error('error file rename')
                        os.system('rm -r '+arscan_temp_path+'/00'+str(folders_temp[i_in_while]))
                        #print('rm -r '+arscan_temp_path+'/00'+str(folders_temp[i_in_while]))
                else:
                    logging.warning('error move folder '+str(folders_temp[i_in_while])+' to '+ str(folders[j_in_while]))
            break
        j_in_while += 1
    i_in_while += 1
    bar.next()
bar.finish()

logging.info('move folders ok')
logging.info('+++++++++++++++')





















