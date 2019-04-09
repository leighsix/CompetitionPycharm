import Setting_Simulation_Value
import Interconnected_Network_Visualization
import numpy as np
from IPython.display import display, HTML
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d.axes3d import *
from sympy import *
import Layer_A_Modeling
import Layer_B_Modeling


class MakingMovie:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.InterNetwork = Interconnected_Network_Visualization.Interconnected_Network_Visualization()

    def making_movie_for_interconneted_dynamics(self, layer_A, layer_B, img_file_name, save_file_name):
        ims = [np.array(self.InterNetwork.draw_interconnected_network(layer_A, layer_B, img_file_name))]


        self.plot_movie_mp4(image_array, save_file_name)




    def plot_movie_mp4(self, image_array, save_file_name):
        dpi = 72.0
        xpixels, ypixels = image_array[0].shape[0], image_array[0].shape[1]
        fig = plt.figure(figsize=(ypixels/dpi, xpixels/dpi), dpi=dpi)
        im = plt.figimage(image_array[0])
        def animate(i):
            im.set_array(image_array[i])
            return (im,)
        anim = animation.FuncAnimation(fig, animate, frames=len(image_array), repeat=False, interval=500)
        anim.save(save_file_name)
        display(HTML(anim.to_html5_video()))

fig = plt.figure()
ims = [np.array(drawing_graph('dynamic_image.png'))]
limited_time = 1000
total = 0
while True :
    im = animation_interconnected_dynamics('dynamic_image.png')
    ims.append(np.array(im))
    total += 1
    if (np.all(A > 0) == 1 and np.all(B > 0) == 1) or (np.all(A < 0)== 1 and np.all(B < 0)== 1) or (total == limited_time) :
        break
im = animation_interconnected_dynamics('dynamic_image.png')
ims.append(np.array(im))
IMS = np.array(ims)
plot_movie_mp4(IMS,'dynamic_images_no_leader(128（BA), 128(RR), ganma=0.5, beta=2).mp4')







if __name__ == "__main__":
    print("Making the movie for competition")
    making_interconnected_edges()
    static_variable(0.5, 2)
    fig = plt.figure()
    ims = [np.array(drawing_graph('dynamic_image.png'))]
    limited_time = 1000
    total = 0
    while True:
        im = animation_interconnected_dynamics('dynamic_image.png')
        ims.append(np.array(im))
        total += 1
        if (np.all(A > 0) == 1 and np.all(B > 0) == 1) or (np.all(A < 0) == 1 and np.all(B < 0) == 1) or (
                total == limited_time):
            break
    im = animation_interconnected_dynamics('dynamic_image.png')
    ims.append(np.array(im))
    IMS = np.array(ims)
    plot_movie_mp4(IMS, 'dynamic_images_no_leader(128（BA), 128(RR), ganma=0.5, beta=2).mp4')