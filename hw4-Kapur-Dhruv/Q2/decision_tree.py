from util import entropy, information_gain, partition_classes
import numpy as np 
import ast

class DecisionTree(object):
    
    
    class node: # node class
     def __init__(self, predict = None, left = None, right = None, values = None, results = None,depth = 0):
               self.predict = predict
               self.left = left
               self.right = right
               self.values = values
               self.results = results
               self.depth = depth
    
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        #self.tree = []
        self.tree = self.node()
        
       
      
    
    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        
        X = np.array(X,dtype = object)
        y = np.array(y) 
        y = np.reshape(y,(-1,1))
        #print X.shape
        #print y.shape
        rows = np.hstack((X,y))
        #print rows
        self.tree = self.build_tree(rows,X)
        
    
   
   
    
    def build_tree(self, rows,X,depth=0): #recursive function to build the tree
      if (depth>8):
          return self.node(results=rows[0,-1])
      X = np.array(X,dtype = object)
      rows = np.array(rows, dtype = object)
      if len(rows) == 0:
        return self.node(results = 0) # the tree is empty
        
      if len(set(rows[:,-1])) == 1:   # If tree has just one row
        return self.node(results =rows[0,-1])
    
      if (X ==X[0]).all():
          return self.node(results =rows[0,-1])
      
      max_gain=0.0
      n_pred = rows[:,-1]
      #print n_pred
   
      #randomly choose m 
      m_pred =  np.random.choice(n_pred,size=int(len(n_pred)))
      
      best_pred = None
      best_sets = None

      #iterating over each  m and calculating information gain from splitting at every value for that predictor

      #for pred in n_pred:
        #val = sorted(set(rows[:,pred]))[:-1]
      prev_classes = rows[:,-1]
       
      for col in range(X.shape[1]):
           if type(X[0,col]) == type('str'):  
               index = int(((X.shape[0])/2))
               value = X[index,col]
           else:
               value = np.mean(X[:,col])
               X_left, X_right,y_left,y_right = partition_classes(X, n_pred,col,value)
               gain = information_gain(prev_classes, [y_left, y_right])
               if gain > max_gain:
                    max_gain = gain
                    best_pred = [col, value] #best predictor and value to split at
                    best_sets = [X_left, X_right,y_left,y_right] #resulting partitions from best split
 
      if max_gain > 0.01: #build tree as long as there is significant information gain in partitioning
           left_set = self.build_tree(np.hstack((best_sets[0],np.reshape(best_sets[2],(-1,1)))),best_sets[0], depth = depth+1)
           #print np.shape(best_sets[1])
           #print np.shape(best_sets[3])
           right_set = self.build_tree(np.hstack((best_sets[1],np.reshape(best_sets[3],(-1,1)))),best_sets[1],depth = depth+1)
           #root = [col,value,1,left_set.shape[1]+1]
           #return(append(root,left_set,right_set)) 
           return self.node(predict = best_pred[0], values = best_pred[1], left = left_set, right = right_set)
      else:
           return self.node(results=rows[0,-1]) #stop building tree and assign result to leaf node
         
      
    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
      result = self.traverse(record, self.tree)
      
      return result

    def traverse(self,record, tree):
      if tree.results is not None: #leaf node
        return tree.results 
      else:
        v = record[tree.predict] 
        if v <= tree.values:
          br = tree.left
        else:
          br = tree.right
        return self.traverse(record, br) #recursive function, travelling down the tree


            
        
        
        
        
        
        
        
        
        

    
