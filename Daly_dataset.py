import pickle
import os

with open("/home/ubuntu/kang_test/Realtime-Action-Recognition/"
          "data/download_videos/daly1.1.0.pkl", "rb") as f:
    daly = pickle.load(f, encoding='latin1')

# Top-level content.  keys
# print(daly.keys())
#
# print(daly['annot'].keys())

# vid = 'r5PgP20uu2I.mp4'
#
# print(daly['annot'][vid].keys())
#
# print(daly['annot'][vid]['suggestedClass'])
#
# print(daly['annot'][vid]['annot'].keys())
#
# print(daly['annot'][vid]['annot']['Drinking'])


f = open("/home/ubuntu/kang_test/Realtime-Action-Recognition/data/download_videos/video_ids.txt")
videos_ids = f.readlines()
# print(videos_ids)

# for line in videos_ids:
#     print(line)

# print(videos_ids[0])
# print(videos_ids[1])

# def search(dirname):
#     filenames =os.listdir(dirname)
#     for filename in filenames:
#         full_filename = os.path.join(dirname, filename)
#         # print(full_filename)
#         ext = os.path.splitext(full_filename)[-1]
#         if ext == '.mp4':
#             print(full_filename)
#
# search("/home/ubuntu/kang_test/Realtime-Action-Recognition/data/download_videos/videos/")


num = 0
remove_newline_ids = []
_filename = []
collect = []
decollect = []
ori_filename = []
find_file = ""
for i in enumerate(videos_ids):
    remove_newline_ids.append(videos_ids[num].rstrip('\n'))
    # print(daly['annot'][remove_newline_ids + ".mp4"].keys())
    # print(daly['annot'][remove_newline_ids + ".mp4"]['annot'].keys(), "[INFO] id : {}".format(remove_newline_ids))
    # if remove_newline_ids ==

    num = num + 1

# print(remove_newline_ids)
# --> txt 파일에 있는 동영상 리스트 코드 뽑고 개행 없애기


num = 0

# 실제 다운로드된 동영상의 코드 추출
for(path, dir, files) in os.walk("/home/ubuntu/kang_test/Realtime-Action-Recognition"
                                 "/data/download_videos"):
    for filename in files:

        ext = os.path.splitext(filename)[-1]
        if ext == '.mp4':
            # print("%s" % filename)
            ori_filename.append(filename)
            # print(filename[-15:-4])
            _filename.append(filename[-15:-4])
            num = num + 1

# print(len(ori_filename))

# txt 파일과 실제 다운로드된 동영상의 코드 비교후 txt 파일의 코드에는 포함되지 않은 동영상 파일 추출
for i in range(len(remove_newline_ids)):
    for i2 in range(len(_filename)):
        # print(i, i2)
        if i2 == len(_filename) - 1:
            # print("A")
            decollect.append(remove_newline_ids[i])
            break
        if remove_newline_ids[i] == _filename[i2]:
            # print("B")
            collect.append(_filename[i2])
            break

# for i in range(len(videos_ids)):
#     for i2 in range(len(decollect)):
#         if videos_ids[i].find(decollect[i2]) == -1:

print(videos_ids[2])
print(decollect[2])

f.close()


# print(collect)
# print(len(collect))
# print(decollect)
# print(len(decollect))
