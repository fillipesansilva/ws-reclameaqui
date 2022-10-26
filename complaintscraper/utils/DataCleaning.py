'''
Class responsible for detecting and correcting (or removing) corrupt or inaccurate records.
'''

class DataCleaning:

  def __call__(self, data):
    
    """
        Arguments:
        - data: dictionary based on ComplaintItem model.

        Return:
        - processed data.
    """ 
    
    data['status'] = data['status'][0]
    
    return data