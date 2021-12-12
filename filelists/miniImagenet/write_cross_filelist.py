# From https://github.com/wyharveychen/CloserLookFewShot/issues/37#issuecomment-524598549
import subprocess
from subprocess import CalledProcessError
def write_miniImagenet_filelist():
  import numpy as np
  from os import listdir
  from os.path import isfile, isdir, join
  import os
  import json
  import random
  import re

  cwd = os.getcwd() 
  # data_path = join(cwd,'ILSVRC2015/Data/CLS-LOC/train') #join(cwd, 'preprocessed') # join(cwd,'ILSVRC2015/Data/CLS-LOC/train')
  data_base_path = join(cwd, 'ILSVRC2015/Data/CLS-LOC/')
  savedir = './'
  dataset_list = ['base', 'val', 'novel']

  #if not os.path.exists(savedir):
  #    os.makedirs(savedir)

  cl = -1
  folderlist = [] # to store label??

  datasetmap = {'base':'train','val':'val','novel':'test'};
  filelists = {'base':{},'val':{},'novel':{} } # label1:[fname1,fname2,...], label2:[fname...], ...
  filelists_flat = {'base':[],'val':[],'novel':[] }
  labellists_flat = {'base':[],'val':[],'novel':[] }

  for dataset in dataset_list:
      data_path = join(data_base_path, datasetmap[dataset])
      with open(datasetmap[dataset] + ".csv", "r") as lines: # read train.csv, val.csv, test.csv
          for i, line in enumerate(lines):
              if i == 0:
                  continue
              fid, extension, label = re.split(',|\.', line) # fid here: filename before .jpg
              # print(fid, extension, label)
              label = label.replace('\n','')
  #             print('fid',fid)
  #             print('label',label)
              if not label in filelists[dataset]:
                  try:
                    fnames = listdir( join(data_path, label) ) # preprocessed files names.jpg in this class
                  except FileNotFoundError:
                    try: 
                      query = f'find ILSVRC2015/Data/CLS-LOC/* -name "{label}"'
                      output = subprocess.check_output(query, shell=True)
                      print(f"{dataset}: {label} not found in {data_path}, found in {output}")
                      mv_cmd = f"mv {output} {data_path}"
                      # print(mv_cmd)
                    except CalledProcessError:
                      print(f"{dataset}: {label} not found anywhere, query={query}")
                    continue

                  folderlist.append(label)
                  # folderlist.append(fid)
                  filelists[dataset][label] = [] # new label

                  # try:
                  #   fnames = listdir( join(data_path, label) ) # preprocessed files names.jpg in this class
                  # except FileNotFoundError:
                  #   try: 
                  #     print(f"{label} not found in {data_path}, found in {subprocess.check_output(query, shell=True)}")
                  #   except CalledProcessError:
                  #     print(f"{label} not found anywhere, query: {query}")
                  #     continue

                  #   continue
                  for i,fname in enumerate(fnames):
  #                 fname_number = [ int(re.split('_|\.', fname)[1]) for fname in fnames] # BUGFIX
                    fname_number = [ int(re.split('_|\.', fname)[0][1:]) for fname in fnames] # preprocessed files names before.jpg
                  sorted_fnames = list(zip( *sorted(  zip(fnames, fname_number), key = lambda f_tuple: f_tuple[1] )))[0] # this class files names.jpg
                  
  #             fid = int(fid[-5:])-1 # last 5 number of fid
  #             print('fid after:',fid,', len of sorted_fnames:',len(sorted_fnames))
  #             name = sorted_fnames[fid]
              # name = fid[-8:] + '.jpg' # BUGFIX
              name = fid + '.jpg' # use whole filename
              fname = join( data_path,label, name ) # file path, BUGFIX: sorted_fnames[fid]
              # print(fname)
              filelists[dataset][label].append(fname)

      for key, filelist in filelists[dataset].items():
          cl += 1
          random.shuffle(filelist)
          filelists_flat[dataset] += filelist
          labellists_flat[dataset] += np.repeat(cl, len(filelist)).tolist() 

  for dataset in dataset_list:
      fo = open(savedir + dataset + ".json", "w")
      fo.write('{"label_names": [')
      fo.writelines(['"%s",' % item  for item in folderlist])
      fo.seek(0, os.SEEK_END) 
      fo.seek(fo.tell()-1, os.SEEK_SET)
      fo.write('],')

      fo.write('"image_names": [')
      fo.writelines(['"%s",' % item  for item in filelists_flat[dataset]])
      fo.seek(0, os.SEEK_END) 
      fo.seek(fo.tell()-1, os.SEEK_SET)
      fo.write('],')

      fo.write('"image_labels": [')
      fo.writelines(['%d,' % item  for item in labellists_flat[dataset]])
      fo.seek(0, os.SEEK_END) 
      fo.seek(fo.tell()-1, os.SEEK_SET)
      fo.write(']}')

      fo.close()
      print("%s -OK" %dataset)

def write_cross_filelist():
  import numpy as np
  from os import listdir
  from os.path import isfile, isdir, join
  import os
  import json
  import random
  import re

  cwd = os.getcwd() 
  # data_path = join(cwd, 'ILSVRC2015/Data/CLS-LOC/train')
  data_base_path = join(cwd, 'ILSVRC2015/Data/CLS-LOC/')

  savedir = './'
  dataset_list = ['base', 'val', 'novel']

  #if not os.path.exists(savedir):
  #    os.makedirs(savedir)

  cl = -1
  folderlist = []

  datasetmap = {'base':'train','val':'val','novel':'test'};
  filelists = {'base':{},'val':{},'novel':{} }
  filelists_flat = {'base':[],'val':[],'novel':[] }
  labellists_flat = {'base':[],'val':[],'novel':[] }

  for dataset in dataset_list:   
      data_path = join(data_base_path, datasetmap[dataset]) 
      with open(datasetmap[dataset] + ".csv", "r") as lines:
          for i, line in enumerate(lines):
              if i == 0:
                  continue
              fid, _ , label = re.split(',|\.', line)
              label = label.replace('\n','')

              if not label in filelists[dataset]:
                  try:
                    fnames = listdir( join(data_path, label) ) # preprocessed files names.jpg in this class
                  except FileNotFoundError:
                    try: 
                      query = f'find ILSVRC2015/Data/CLS-LOC/* -name "{label}"'
                      output = subprocess.check_output(query, shell=True)
                      print(f"{dataset}: {label} not found in {data_path}, found in {output}")
                      mv_cmd = f"mv {output} {data_path}"
                      # print(mv_cmd)
                    except CalledProcessError:
                      print(f"{dataset}: {label} not found anywhere, query={query}")

                  folderlist.append(label)
                  filelists[dataset][label] = []


                  # try:
                  #   fnames = listdir( join(data_path, label) )
                  # except FileNotFoundError:
                  #   print(f"{label} not found in {data_path}")
                  #   continue
                  fname_number = [ int(re.split('_|\.', fname)[0][1:]) for fname in fnames] # BUGFIXED?
                  
              # name = fid[-8:] + '.jpg' BUGIFX
              name = fid + '.jpg' # use whole filename
              fname = join(data_path, label, name)
              filelists[dataset][label].append(fname)

      for key, filelist in filelists[dataset].items():
          cl += 1
          random.shuffle(filelist)
          filelists_flat[dataset] += filelist
          labellists_flat[dataset] += np.repeat(cl, len(filelist)).tolist() 

  #cross setting use base/val/novel together
  filelists_flat_all = filelists_flat['base'] + filelists_flat['val'] + filelists_flat['novel']
  labellists_flat_all = labellists_flat['base'] + labellists_flat['val'] + labellists_flat['novel']
  fo = open(savedir + "all.json", "w")
  fo.write('{"label_names": [')
  fo.writelines(['"%s",' % item  for item in folderlist])
  fo.seek(0, os.SEEK_END) 
  fo.seek(fo.tell()-1, os.SEEK_SET)
  fo.write('],')

  fo.write('"image_names": [')
  fo.writelines(['"%s",' % item  for item in filelists_flat_all])
  fo.seek(0, os.SEEK_END) 
  fo.seek(fo.tell()-1, os.SEEK_SET)
  fo.write('],')

  fo.write('"image_labels": [')
  fo.writelines(['%d,' % item  for item in labellists_flat_all])
  fo.seek(0, os.SEEK_END) 
  fo.seek(fo.tell()-1, os.SEEK_SET)
  fo.write(']}')

  fo.close()
  print("all -OK")

if __name__ == '__main__':
    write_cross_filelist()