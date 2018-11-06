# -*- coding: utf-8 -*-
from io import open
import json
with open('json_count.txt', 'w', encoding='ascii') as fin:
    data = {}
    data['no'] = 10
    data['context']={"id":"123456","name":"CarMaster","type":"masterCar"}
    data['context']['id'] = 8970
    print(data)
    print("No=",data['no'])
    with open('json_wout1.txt', 'w', encoding='ascii') as fout:
        fout.write(json.dumps(data, separators=(',', ':')))

