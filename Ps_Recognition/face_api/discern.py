import face_recognition
from face_api.models import IMG


def img_discern(load_files, img_dict):
    data = [[], [], [], 0]
    content = {'text': 1,
               'img': {},
               'bug': False
               }
    for i in img_dict:
        new_img = IMG(img=load_files.get(i))
        new_img.save()
        content['img'][new_img.img] = i
        load_image = face_recognition.load_image_file(new_img.img)
        face_locations = face_recognition.face_locations(load_image)
        if face_locations:
            data[1].append(face_recognition.face_encodings(load_image)[0])
            data[0] += face_locations
            if len(list(set(data[0]))) != len(data[0]):
                content['bug'] = True
                content['text'] = '图片 %s 重复' % load_files.get(i)
                break
        else:
            content['bug'] = True
            content['text'] = '请检测图片 %s 图片内未识别出人脸或脸部遮挡倾斜无法识别' % load_files.get(i)
            break
    if content['bug']:
        content['img'] = new_img.img
        return content
    else:
        for x in range(0, 3):
            for y in range(3 - x):
                data[2].append(face_recognition.face_distance([data[1][x]], data[1][y + x + 1]))

        data[2] = [x for x in data[2] if x != max(data[2]) and x != min(data[2])]
        for i in data[2]:
            data[3] += i

        data[3] = float('%.4f' % data[3])
        if data[3] <= 1.3:
            content['text'] = '完全没有ps痕迹或放入了重复照片'
        elif data[3] >= 1.8:
            content['text'] = '完全不是一个人或照片ps,美颜,遮挡严重'
        else:
            data[3] = (data[3] - 1.3) * 200
            if data[3] <= 40:
                content['text'] = 'ps指数百分之%.4f,p图可能性非常低，ps痕迹非常少,或使用美颜等级低的自动美颜.' % data[3]
            elif data[3] >= 70:
                content['text'] = 'ps指数百分之%.4f,ps痕迹较为明显,p图可能性较高等或使用美颜等级高的自动美颜。' % data[3]
            else:
                content['text'] = 'ps指数百分之%.4f,p图可能性中等,ps痕迹存在,或使用美颜等级中等的自动美颜.' % data[3]
        return content
