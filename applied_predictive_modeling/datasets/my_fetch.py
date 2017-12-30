import rpy2.robjects as robjects
import pandas.rpy.common as com
import pandas as pd
import os


for name in os.listdir('.'):
    if name.endswith('.RData'):
        name_ = os.path.splitext(name)[0]
        dir_path = os.path.join(os.getcwd(), name_)
        print "dir_path:", dir_path
        # creat sub-directory
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        #file_path = os.path.join(root, name)
        robj = robjects.r.load(name)
        # check out subfiles in the data frame
        for var in robj:
            myRData = com.load_data(var)
            # convert to DataFrame
            if not isinstance(myRData, pd.DataFrame):
                myRData = pd.DataFrame(myRData)
            var_path = os.path.join(dir_path,var+'.csv')
            print "var_path:", var_path
            myRData.to_csv(var_path)
        #os.remove(os.path.join(dir_path, name)) # clean up
    print 'success'