import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="paper")

def plot_training_curve(state, out):
    plt.plot(state['train_loss'], label='train_loss')
    plt.plot(state['valid_loss'], label='valid_loss')
    plt.legend()
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.show()
    plt.savefig(out)