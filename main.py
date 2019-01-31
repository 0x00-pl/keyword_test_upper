import os
import time

import numpy as np
import serial

import play


def msg_to_device(msg, ser=None):
    if ser:
        print('>>', msg)
        ser.write(msg.encode('utf8'))
    else:
        print(msg)


def msg_from_device(ser=None):
    if ser:
        res = ser.readline().decode('utf8')
        print('<<', res)
        if 'VAD' in res or res=='':
            return res
        else:
            return msg_from_device(ser)
    else:
        return input()


def test_score(sound_path1, sound_path2, ser=None):
    msg_to_device('~' + sound_path1 + '@', ser)
    play.play_sound(sound_path1)
    time.sleep(0.3)
    msg_to_device('!' + sound_path2 + '@', ser)
    play.play_sound(sound_path2)
    time.sleep(0.3)
    return msg_from_device(ser)


def test_all(filepath_list, ser=None, cb=None):
    ret = []
    length = len(filepath_list)
    total_test = length * (length - 1)
    for i in range(length - 1):
        for j in range(i, length):
            res = test_score(filepath_list[i], filepath_list[j], ser)
            ret.append(res)
            if cb:
                cb(res)
            print('[test] {}/{}'.format(len(ret), total_test))

    return ret


def read_all(root_path='kanzhitongxue'):
    ret = []
    for prefix_path, dirs, files in os.walk(root_path):
        for filename in files:
            file_path = os.path.join(prefix_path, filename)
            ret.append(file_path)
    return ret


def dump_to_file(line):
    with open('dump.txt', 'a') as df:
        df.write(line)


def list_ports():
    import serial.tools.list_ports

    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'MyCDCDevice' in p.description:
            print(p)


def main():
    dump_to_file('=======================================')
    list_ports()
    filepath_list = read_all('kanzhitongxue/neg')
    with serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=5) as ser:
        res = test_all(filepath_list, ser, cb=dump_to_file)
    np.save('output.npy', res)


if __name__ == '__main__':
    main()
