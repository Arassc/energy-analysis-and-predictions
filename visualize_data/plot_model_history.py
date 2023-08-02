import matplotlib.pyplot as plt
import tensorflow as tf

def plot_history(history: tf.keras.callbacks.History,
                 train_test_ratio: float,
                 train_test_sequence: int,
                 fold_length_ratio: float,
                 fold_sequence: int,
                 units_layer_1: int,
                 units_layer_2: int,
                 fig_name: str):

    fig, ax = plt.subplots(1,2, figsize=(20,7))
    # --- LOSS: MSE ---
    ax[0].plot(history.history['loss'])
    ax[0].plot(history.history['val_loss'])
    ax[0].set_title(f'MSE')
    ax[0].set_ylabel('Loss')
    ax[0].set_xlabel('Epoch')
    ax[0].legend(['Train', 'Validation'], loc='best')
    ax[0].grid(axis="x",linewidth=0.5)
    ax[0].grid(axis="y",linewidth=0.5)

    # --- METRICS:MAE ---

    ax[1].plot(history.history['mae'])
    ax[1].plot(history.history['val_mae'])
    ax[1].set_title('MAE')
    ax[1].set_ylabel('MAE')
    ax[1].set_xlabel('Epoch')
    ax[1].legend(['Train', 'Validation'], loc='best')
    ax[1].grid(axis="x",linewidth=0.5)
    ax[1].grid(axis="y",linewidth=0.5)
    fig_name = fig_name + '_test-ratio-' + str(train_test_ratio) + '_fold-length-' + str(train_test_ratio) + \
                '_train-test-sequence-' + str(train_test_sequence) + '.png'
    plt.title(fig_name)
    fig.savefig(fig_name)
    return ax



def plot_history_loss_mse(history: tf.keras.callbacks.History,
                 train_test_ratio: float,
                 train_test_sequence: int,
                 fold_length_ratio: float,
                 fold_sequence: int,
                 units_layer_1: int,
                 units_layer_2: int):

    fig, ax = plt.subplots(1,2, figsize=(20,7))
    # --- LOSS: MSE ---
    ax[0].plot(history.history['loss'])
    ax[0].plot(history.history['val_loss'])
    ax[0].set_title(f'loss MSE, split_ratio= {train_test_ratio}, split_seq= {train_test_sequence},\
    fold_ratio= {fold_length_ratio}, fold_seq= {fold_sequence}, layer_1= {units_layer_1}, layer_2= {units_layer_2}')
    ax[0].set_ylabel('Loss')
    ax[0].set_xlabel('Epoch')
    ax[0].legend(['Train', 'Validation'], loc='best')
    ax[0].grid(axis="x",linewidth=0.5)
    ax[0].grid(axis="y",linewidth=0.5)

    # --- METRICS:MAE ---

    ax[1].plot(history.history['mse'])
    ax[1].plot(history.history['val_mse'])
    ax[1].set_title('MSE')
    ax[1].set_ylabel('MAE')
    ax[1].set_xlabel('Epoch')
    ax[1].legend(['Train', 'Validation'], loc='best')
    ax[1].grid(axis="x",linewidth=0.5)
    ax[1].grid(axis="y",linewidth=0.5)

    return ax
