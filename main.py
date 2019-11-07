import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import numpy as np

def adder(a,b):
	upperCode = "`include \"fulladder16bit.v\"\nmodule top;\nreg [15:0] a,b;\nreg ci;\nwire [15:0] sum;\nwire co;\nfulladder16bit f(a,b,ci,sum,co);\ninitial\nbegin\n"
	variable = "a=16'd"+str(a)+";b=16'd"+str(b)+";ci=1'b0;\n";
	lowerCode  ="end\ninitial\nbegin\n\n$monitor(\"%d\",sum);\nend\nendmodule\n"

	testBench = upperCode+variable+lowerCode
	f=open("adder.v","w")
	f.write(testBench)
	f.close()
	cmd = "iverilog "+"adder.v "
	os.system(cmd)
	cmd ="./a.out > adderResult.txt"
	os.system(cmd)
	f =open("adderResult.txt","r")
	res = f.read()
	res=res.strip()
	return int(res)



X = np.array([[1, 2],
              [1.5, 1.8],
              [5, 8 ],
              [8, 8],
              [1, 0.6],
              [9,11],
              [1,3],
              [8,9],
              [0,3],
              [5,4],
              [6,4],])

##plt.scatter(X[:,0], X[:,1], s=150)
##plt.show()

colors = 10*["g","r","c","b","k"]

def manhatan(a,b):
    print(a,b)
    print(type(a),type(b))
    a1 =a[0]
    a2 =a[1]
    b1=b[0]
    b2=b[1]
    dist = abs(a1-b1)+abs(a2-b2)
    return dist


class K_Means:
    def __init__(self, k=2, tol=0.001, max_iter=5):
        self.k = k
        self.tol = tol
        self.max_iter = max_iter

    def fit(self,data):

        self.centroids = {}

        for i in range(self.k):
            self.centroids[i] = data[i]

        for i in range(self.max_iter):
            self.classifications = {}

            for i in range(self.k):
                self.classifications[i] = []

            for featureset in data:
                # print("h",featureset,self.centroids)
                distances = [manhatan(featureset,self.centroids[centroid]) for centroid in self.centroids]
                classification = distances.index(min(distances))
                self.classifications[classification].append(featureset)

            prev_centroids = dict(self.centroids)

            for classification in self.classifications:
                self.centroids[classification] = np.average(self.classifications[classification],axis=0)

            optimized = True

            for c in self.centroids:
                original_centroid = prev_centroids[c]
                current_centroid = self.centroids[c]
                if np.sum((current_centroid-original_centroid)/original_centroid*100.0) > self.tol:
                    print(np.sum((current_centroid-original_centroid)/original_centroid*100.0))
                    optimized = False

            if optimized:
                break

    def predict(self,data):
        distances = [manhatan(data,self.centroids[centroid]) for centroid in self.centroids]
        classification = distances.index(min(distances))
        return classification


clf = K_Means()
clf.fit(X)

for centroid in clf.centroids:
    plt.scatter(clf.centroids[centroid][0], clf.centroids[centroid][1],
                marker="o", color="k", s=150, linewidths=5)

for classification in clf.classifications:
    color = colors[classification]
    for featureset in clf.classifications[classification]:
        plt.scatter(featureset[0], featureset[1], marker="x", color=color, s=150, linewidths=5)

##unknowns = np.array([[1,3],
##                     [8,9],
##                     [0,3],
##                     [5,4],
##                     [6,4],])
## 
##for unknown in unknowns:
##    classification = clf.predict(unknown)
##    plt.scatter(unknown[0], unknown[1], marker="*", color=colors[classification], s=150, linewidths=5)
##

plt.show()
