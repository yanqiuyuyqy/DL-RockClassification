import numpy as np
import glob

def split2Tiles(path, arr, x_size=256, y_size=256, suffix='block1'):
    xx, yy = arr.shape[1], arr.shape[2]
    x_num = int(xx/x_size)
    y_num = int(yy/y_size)
    print('split into {0} tiles'.format(x_num*y_num))
    count = 0
    for i in range(x_num):
        for j in range(y_num):
            tmp = arr[:, x_size*i: x_size*(i+1), y_size*j: y_size*(j+1)]
            np.save(path+'{0}_{1}'.format(suffix, count), tmp)
            count += 1
            
def split_trn_vld_tst(path, vld_rate=0.2, tst_rate=0.1, random=True, seed=10):
    np.random.seed(seed)
    x_IDs = sorted(glob.glob(path+'X/*.npy'))
    y_IDs = sorted(glob.glob(path+'Y/*.npy'))
    if len(x_IDs) != len(y_IDs):
        raise ValueError('imgs and labels are not matched!')
    num = len(x_IDs)
    vld_num = int(num*vld_rate)
    tst_num = int(num*tst_rate)
    idx = np.arange(num)
    if random:
        np.random.shuffle(idx)
    X_tst = [x_IDs[k] for k in idx[:tst_num]]
    X_vld = [x_IDs[k] for k in idx[tst_num:tst_num+vld_num]]
    X_trn = [x_IDs[k] for k in idx[tst_num+vld_num:]]
    Y_tst = [y_IDs[k] for k in idx[:tst_num]]
    Y_vld = [y_IDs[k] for k in idx[tst_num:tst_num+vld_num]]
    Y_trn = [y_IDs[k] for k in idx[tst_num+vld_num:]]
    return X_trn, Y_trn, X_vld, Y_vld, X_tst, Y_tst