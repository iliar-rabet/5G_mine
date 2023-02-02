import matplotlib.pyplot as plt
import numpy as np

ypoints = np.array([3, 8, 1, 10])
line1 = np.array([
 0.11587532556746602,
 0.11578948733159784,
 0.1155036855611039,
 0.11496719211448259,
 0.11469866536715778,
 0.11418064502086074,
 0.11357581456357935,
 0.11266250307744748,
 0.11250075972554692,
 0.11224458970733536,
 0.11152934592141801,
 0.1113644000909224,
 0.1099459880108845,
 0.10997702647694732,
 0.10997521788975076,
 0.10982923539684271
    ])

line2 = np.array([
 0.31641285586332263,
 0.31641285586332263,
 0.31614078992447503,
 0.31614078992447503,
 0.31614078992447503,
 0.31614078992447503,
 0.31585465004640345,
 0.3118328539913606,
 0.30919164047241865,
 0.3058145654132289,
 0.3023843393062693,
 0.3007801432648893,
 0.29536092960727883,
 0.29166579270284326,
 0.28730979161824827,
 0.2850534030709908
])


line3 = np.array([
 0.726321689508619,
 0.7224250902961497,
 0.7205964254737113,
 0.7176679468496785,
 0.7143361455804894,
 0.7118872231230057,
 0.7104885511192863,
 0.7015290838059189,
 0.6944264788954435,
 0.6833904404365616,
 0.6764250868218594,
 0.6696059258337541,
 0.6546195179011715,
 0.6428997482118542,
 0.6338156989127461,
 0.631757120587604
])

line4 = np.array([
 0.8089484141879191,
 0.8039074471675625,
 0.8045454846521147,
 0.8025300994208667,
 0.8001886568620852,
 0.7991167167034836,
 0.7973664592662923,
 0.7951566610711394,
 0.7948534243954009,
 0.7844246976935138,
 0.7860644612515705,
 0.7817719602726968,
 0.7925671402225299,
 0.8078429270066753,
 0.8271246977671849,
 0.8275361922787934
])

plt.plot(line1,'--bo',label="Perm:1 Temp:0")
plt.plot(line2,'-gD',label="Perm:2 Temp:0")
plt.plot(line3,'-rp',label="Perm:3 Temp:0")
plt.plot(line4,'-ys',label="Perm:3 Temp:1")
plt.legend()
plt.ylabel('Coverage Probability')
plt.xlabel('Period')
plt.show()