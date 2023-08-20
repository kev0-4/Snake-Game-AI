from IPython import display
import matplotlib.pyplot as plt


plt.ion()


def plot(scores, mean_scores):
    material_blue = '#2196F3'
    material_red = '#F44336'
    display.clear_output(wait=True)
    plt.style.use('seaborn-darkgrid')
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training Progress')
    plt.xlabel('Number of Games', color = material_blue)
    plt.ylabel('Score', color = material_blue)
    plt.plot(scores, color = material_blue)
    plt.plot(mean_scores, color = material_red)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(.1)
