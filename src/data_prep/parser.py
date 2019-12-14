import csv
import xml.etree.ElementTree as ET

normal_text = []
bully_text = []

del_marks = ['"', '\'', '\n', '\r', '<br>', 'Q: ', 'A: ', '&amp;', '&quot;']

tree = ET.parse('../../data/XMLMergedFile.xml')
root = tree.getroot()
for child in root:
    for post in child.findall('POST'):
        text = post.find('TEXT').text
        for mark in del_marks:
            text = text.replace(mark, '')
        text = text.replace('&#039;', "'")
        for label in post.findall('LABELDATA'):
            bully = False
            for boo in label.findall('CYBERBULLYWORD'):
                if boo.text is not None:
                    if 'n/a' not in boo.text.lower():
                        bully = True
                        boo_text = boo.text
                        for mark in del_marks:
                            boo_text = boo_text.replace(mark, '')
                        boo_text = boo_text.replace('&#039;', '\'')
                        if boo_text not in bully_text:
                            if len(boo_text) < 1024:
                                bully_text.append(boo_text)
            if not bully:
                if text not in normal_text:
                    if len(text) < 1024:
                        normal_text.append(text)

with open('test_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(0, len(normal_text)//4):
        t = normal_text[i]
        writer.writerow([t, 'neutral'])
    for i in range(0, len(bully_text)//4):
        t = bully_text[i]
        writer.writerow([t, 'bully'])

with open('train_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(normal_text)//4, len(normal_text)):
        t = normal_text[i]
        writer.writerow([t, 'neutral'])
    for i in range(len(bully_text)//4, len(bully_text)):
        t = bully_text[i]
        writer.writerow([t, 'bully'])
