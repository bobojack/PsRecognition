# -*- coding: utf-8 -*-
from django.shortcuts import render
from face_api import discern
import collections
# Create your views here.


def recognition(request):
    content = {'html': 'index.html', 'templates': {}}
    img_dict = {'img1': 0, 'img2': 1, 'img3': 2, 'img4': 3}
    upload_size = 4194304
    img_dict = collections.OrderedDict(sorted(img_dict.items(), key=lambda t: t[1]))
    if request.method == 'POST':
        if img_dict.keys() == request.FILES.keys():
            print(int(request.META['CONTENT_LENGTH']))
            if int(request.META['CONTENT_LENGTH']) <= upload_size:
                value = discern.img_discern(request.FILES, img_dict)
                print(value)
                bug = value['bug']
                if bug:
                    content = {'html': 'error.html', 'templates': {'text': value['text'], 'imgs': value['img']}}
                else:
                    content = {'html': 'result.html', 'templates': {'text': value['text'], 'imgs': value['img']}}
                    print(content)
            else:
                content['templates'] = {'text': '提交图片不能大大于1M', 'title': '照骗识别系统', 'imgs': img_dict}
        else:
            content['templates'] = {'text': '提交图片不能少于四张', 'title': '照骗识别系统', 'imgs': img_dict}
    else:
        content['templates'] = {'text': '作者bojack', 'title': '照骗识别系统', 'imgs': img_dict}
    return render(request, content['html'], content['templates'])
