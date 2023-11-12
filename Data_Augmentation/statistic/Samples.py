import os
import matplotlib.pyplot as plt 
import xml.etree.ElementTree as ET

class_num = [0]*8
labels_dir = r'C:\Users\86137\Desktop\jsai_data\train1112_mix\labels\train'
labels_files = os.listdir(labels_dir)
labels = ["Type_a","Type_b","Type_c","Type_d","Type_e","Type_f","Type_g","Type_h"]
# labels = ["Crack","Manhole", "Net", "Pothole", "Patch-Crack", "Patch-Net", "Patch-Pothole", "other","Other"]
# xml_dir = r'C:\Users\86137\Desktop\Data\RDD2022\United_States\train\annotations\xmls'
# xml_files = os.listdir(xml_dir)

if __name__ == '__main__':

    # for file in xml_files:
    #     xml_file = xml_dir + '/' + file
    #     with open(xml_file,'r') as in_file:
    #         tree = ET.parse(in_file)
    #         root = tree.getroot()
    #         for obj in root.iter('object') :
    #             cls = obj.find('name').text
    #             # print(cls)
    #             label = -1
    #             if cls == 'D00' :
    #                 label = 1
    #             elif cls == 'D10' :
    #                 label = 0
    #             elif cls == 'D20' :
    #                 label = 3
    #             else :
    #                 label = 4
    #             class_num[label] += 1

    for file in labels_files:
        txt_file = labels_dir + '/' + file

        with open(txt_file,'r') as f:
            for line in f :
                data = line.split()
                label = int(data[0])
                class_num[label] += 1

    y = []
    
    for i in range(0,8) : 
        y.append(class_num[i])
    # print(y[7])
    print(y)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.bar(x=labels, height=y)
    ax.set_title("labels", fontsize=15)
    plt.show()
