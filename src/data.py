import numpy as np
from osgeo import gdal
import glob
from sklearn.model_selection import train_test_split

class Data:
    
    def __init__(self, path, random=False):
        """
        input:
            path: path to the block
            max_num: int, num of samples
            random: bool, to load samples randomly or from 0 to num_max
        """
        self.X = sorted(glob.glob(path+"images/images/*.tif"))
        self.Y = sorted(glob.glob(path+"labels/images/*.tif"))
        if len(self.X) != len(self.Y):
            raise ValueError('imgs and labels are not matched')
      
    def get_MinMax(self, path):
        file = gdal.Open(path)
        min_list = []
        max_list = []
        for i in range(1, file.RasterCount+1):
            if i < 11:
                min_list.append(0.)
                max_list.append(10000.)
            else:
                min_list.append(file.GetRasterBand(i).GetMinimum())
                max_list.append(file.GetRasterBand(i).GetMaximum())
        return min_list, max_list
        
    def img_to_array(self, input_file, min_list=None, max_list=None, dtype='float32'):
        """
        convert a raster tile into numpy array
        input:
            input_file: string, path a raster(.tif)
            normalizer: double, if input is labels with 0 or 1, it's 1.
                                if input is sentinal data (reflectance), then it's 10000.
            dtype: string, data type, default as 'float32'
        return:
            arr: numpy array, shape is [dim_y, dim_x, num_bands]
        """
        file = gdal.Open(input_file)
        if min_list != None:
            bands = [(np.array(file.GetRasterBand(i).ReadAsArray()).astype(dtype) - min_list[i-1]) / (max_list[i-1] - min_list[i-1]) for i in range(1, file.RasterCount + 1)]
        else:
            bands = [np.array(file.GetRasterBand(i).ReadAsArray()).astype(dtype) for i in range(1, file.RasterCount + 1)]
        arr = np.stack(bands, axis=2)
        return arr

    def get_XY(self, min_list, max_list, start=0, num=10, as_arr=False, random=False):
        """
        function: load max_num of XY into lists
        output: list of numpy arrays, X (images) and Y (labels)
        """
        X_out = []
        Y_out = []
        
        if random:
            idx = np.random.randint(0, len(self.X), num)
        else:
            idx = range(start, start+num)

        for i in idx:
            X_out.append(self.img_to_array(self.X[i], min_list=min_list, max_list=max_list))
            Y_out.append(self.img_to_array(self.Y[i], dtype='int'))
        if as_arr:
            return np.asarray(X_out), np.asarray(Y_out)
        else:
            return X_out, Y_out
        
    def trn_tst_split(self, test_rate, random_seed):
        """
        input:  test_rate, double, between 0 and 1,
                random_seed, randomness to generate tst and trn data
        output: lists of train and test datasets
        """
        X, Y = self.get_XY()
        X_trn, X_tst, Y_trn, Y_tst = train_test_split(X, Y, train_size=1-test_rate, test_size=test_rate, random_state=random_seed)
        return np.asarray(X_trn), np.asarray(X_tst), np.asarray(Y_trn), np.asarray(Y_tst)