import numpy as np    
from scipy.fft import fft    
from sklearn.base import TransformerMixin
    
def psd(X):    
    """    
    :param: X is a matrix (samples x genes)    
    """    
    s, g = X.shape # samples x genes    
    corr = np.corrcoef(X,rowvar=False) # yields g x g corrcoef matrix ...    
    aat = np.matmul(X,corr) # s x g matrix, equivalent to aa' in Trans_PSD.m     
    pst = np.abs(fft(np.abs(aat)))/g # s x g matrix, equivalent to ps'     
    pro_pst = pst / np.sum(pst,1)[:,np.newaxis]    
    Aaat = np.multiply(pro_pst,np.log2(pro_pst))    
    aaat = -(np.mean(Aaat,0)-Aaat)    
    Yt = (aaat - aaat.min(0)[np.newaxis,:])/(aaat.max(0)-aaat.min(0))[np.newaxis,:] # min/max scaling across genes    
    return Yt   

class PSD(TransformerMixin):

    def __init__(self):
        self.samples = None
        self.features = None

    def fit(X, y=None):
    """Fit the PSD model with X

    Parameters
    ----------
    X : array-like, shape(n_samples, n_features)

    y : None
        Ignored
    """
    
        self.samples, self.features = X.shape
        self.corr = np.corrcoef(X,rowvar=False) 
        
        pass

    def transform(X)
        tmp = np.matmul(X,self.corr) 
        tmp = np.abs(fft(np.abs(tmp)))/g 
        tmp = tmp / np.sum(tmp,1)[:,np.newaxis]    
        tmp = np.multiply(tmp,np.log2(tmp))    
        tmp = -(np.mean(tmp,0)-tmp)    
        return (tmp - tmp.min(0)[np.newaxis,:])/(tmp.max(0)-tmp.min(0))[np.newaxis,:] # min/max scaling across genes    
