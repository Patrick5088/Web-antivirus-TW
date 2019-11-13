import requests
import time

import hashlib
import pefile
#
# data={'id_client':'firstUser',
#       'buffers':['2','13','14','15']
#
#         }
#
#
# post = requests.post('http://127.0.0.1:5000/scanHash',json=data)
# print(post.text)
#
#

pe=pefile.PE('file1_clean.old')

i = 0
name = ["" for x in range(pe.FILE_HEADER.NumberOfSections)]
adr = [0 for x in range(pe.FILE_HEADER.NumberOfSections)]
size = [0 for x in range(pe.FILE_HEADER.NumberOfSections)]
c = [0 for x in range(pe.FILE_HEADER.NumberOfSections)]

for section in pe.sections:
    name[i] = section.Name
    adr[i] = section.VirtualAddress
    size[i] = section.Misc_VirtualSize
    c[i] = section.Characteristics
    i = i + 1

hasher = hashlib.md5()
with open('icardagt_clean.old', 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)

md5 = hasher.hexdigest()

export={'id_client':'firstClient',
        'buffers' : []
        }

bufferItem_1={'md5': md5,
              'fh': {'ns': pe.FILE_HEADER.NumberOfSections,
                     'c': hex(pe.FILE_HEADER.Characteristics)
                     },

              'oh': {'m': hex(pe.OPTIONAL_HEADER.Magic),
                     'ep': hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
                     },

              'sec': [],
         }


for i in range(pe.FILE_HEADER.NumberOfSections):
    bufferItem_1['sec'].append(
        {'n': name[i][:name[i].index(b'\0')].decode("utf-8"), 'va': hex(adr[i]), 's': hex(size[i]), 'c': hex(c[i])})

export['buffers'].append(bufferItem_1)






post2= requests.post('http://127.0.0.1:5000/scanBuffer',json=export)
job_id=post2.text
print(post2.text)
SERVER_LINK="http://127.0.0.1:5000"


job_id = requests.post(SERVER_LINK + '/scanBuffer', json=export).json()['id']


response = requests.get(SERVER_LINK + '/scanBuffer/' + job_id).json()
print('response', response)

while response['status'] != 'ready' and response['status'] != 'failed':
    time.sleep(2)
    response = requests.get(SERVER_LINK + '/scanBuffer/' + job_id).json()

print('response', response)


