# amuse2_joint_ucb.py  (sovrascrivi / integra amuse2.py)
import math
import statistics
import csv
import time
#import matplotlib.pyplot as plt
#from matplotlib import pyplot as plt

# Configurazione esperimento
n_max_steps = 100
n_max_episodes = 2

# Definizione modulazioni e livelli potenza (modifica secondo il tuo PHY)
MODS = ["BPSK", "8PSK", "16PSK"]    # esempio: 3 modulazioni (come il tuo codice originale)
POWERS = [20, 63, 126]               # dBm -- adatta alla tua scala

# Costruzione azioni congiunte (index -> (mod_idx, pow_idx))
ACTIONS = []
for mi in range(len(MODS)):
    for pi in range(len(POWERS)):
        ACTIONS.append((mi, pi))
NUM_ACTIONS = len(ACTIONS)

# Parametri UCB1
exploration_param = 2.0

# Statistiche UCB1
action_counts = [0] * NUM_ACTIONS
total_rewards = [0.0] * NUM_ACTIONS

# Logging globale episodi
total_mean_throughput = []
total_cumulative_reward = []

# Funzione di selezione UCB1 (identica a quella originale ma con NUM_ACTIONS)
def select_action():
    # se esiste un'azione non esplorata, sceglila
    for a in range(NUM_ACTIONS):
        if action_counts[a] == 0:
            return a
    total_counts = sum(action_counts)
    ucb_values = [
        (total_rewards[a] / action_counts[a]) + exploration_param * math.sqrt(math.log(total_counts) / action_counts[a])
        for a in range(NUM_ACTIONS)
    ]
    return ucb_values.index(max(ucb_values))


n_episode = 0
while n_episode < n_max_episodes:
    with open('done.csv', 'w', newline='') as done_file:
        csv.writer(done_file).writerow([0])

    internal_step = 1
    n_step = 1
    cumulative_reward = 0.0
    throughput_list = []

    reward_per_step =[]

    while n_step < n_max_steps:
        action = select_action()
        mod_idx, pow_idx = ACTIONS[action]
        mod = MODS[mod_idx]
        pwr = POWERS[pow_idx]

        # Scrivo azione in actions.csv: step, action_idx, mod_idx, pow_idx, power_value
        with open('actions.csv', 'w', newline='') as actions_file:
            time.sleep(0.2)
            actions_writer = csv.writer(actions_file)
            actions_writer.writerow([internal_step, action, mod_idx, pow_idx, pwr])
            print(f"[INFO] wrote actions.csv: step={internal_step}, action={action}, mod={mod}, pwr={pwr}")

        # attendo reward da DESERT
        while True:
            with open('rewards.csv') as rewards_file_check:
                rewards_reader_check = csv.reader(rewards_file_check)
                row = next(rewards_reader_check)
                step = int(row[0])
                reward = float(row[1])
                print(f"[INFO] read rewards.csv: step={step}, reward={reward}")

            if step == internal_step:
                cumulative_reward += reward
                throughput_list.append(reward)
                done = True if (n_step + 1) == n_max_steps else False
                break
            if step < internal_step:
                # DESERT non ha ancora aggiornato
                pass
            if step > internal_step:
                print(f"[ERROR] step in rewards.csv ({step}) > internal_step ({internal_step})")
                with open('done.csv') as done_file:
                    done_reader = csv.reader(done_file)
                    row = next(done_reader)
                    if row[0] == '1':
                        print("[END] Detected done=1, exiting.")
                        break
                pass
            time.sleep(0.2)

        # Aggiorno UCB counters
        action_counts[action] += 1
        total_rewards[action] += reward

        internal_step += 1
        n_step += 1

        # sincronizzazione come prima
        while True:
            with open('synchronization.csv') as synchro_check:
                synchro_reader_check = csv.reader(synchro_check)
                row = next(synchro_reader_check)
                synchro_step = int(row[0])
                print(f"Read {synchro_step} in synchronization.csv, I was expecting {internal_step}")
                if synchro_step == internal_step or (n_step == n_max_steps):
                    print("[OK] breaking from synchro check loop")
                    print(f"[INFO] step: {n_step}, n_max_steps: {n_max_steps}")
                    if (n_step == n_max_steps):
                        print("[INFO] Reached max steps, writing done=1")
                        with open('done.csv', 'w', newline='') as done_file:
                            csv.writer(done_file).writerow([1])
                        time.sleep(3)
                    break
            time.sleep(1)
        #acquisizione dati per plotting
        reward_per_step.append(reward)
    # fine episodio
    #plot reward
    with open('reward_per_step.csv',"a",newline='') as reward_file:
        reward_writer = csv.writer(reward_file)
        reward_writer.writerow(reward_per_step)
    '''
    plt.plot(range(1, n_max_steps), reward_per_step, marker='o')
    plt.title('Reward per Step')
    plt.xlabel('Step')
    plt.ylabel('Reward')
    plt.grid(True)
    plt.show()
    '''    
    mean_throughput = statistics.mean(throughput_list) if throughput_list else 0.0
    total_cumulative_reward.append(cumulative_reward)
    total_mean_throughput.append(mean_throughput)

    print(f"[END] Episode {n_episode} cumulative_reward={cumulative_reward}, mean_throughput={mean_throughput}")

    n_episode += 1

print(f"[FINAL] Total cumulative reward: {total_cumulative_reward}")
print(f"[FINAL] Total mean throughput: {total_mean_throughput}")

