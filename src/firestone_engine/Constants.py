class Constants(object):

    STATE = ['运行中','暂停','已提交','异常','已完成','撤销','T0已买入']

    INDEX = ['000001','sz','hs300','sz50','zxb','399006']


    @classmethod
    def map_code(self, name, code):
        if(name == '上证指数'):
            return Constants.INDEX[0]
        elif(name == '创业板指'):
            return Constants.INDEX[5]
        return code
            