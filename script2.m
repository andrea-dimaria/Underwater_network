%% Initialization
close
clear
clc
%% Loading files
%execute this section or the next one
energy = csvread("energy_per_step.csv");
reward = csvread("reward_per_step.csv");
thr = csvread("throughput_per_step.csv");
modulation = csvread("modulation_per_step.csv");
power = csvread("power_per_step.csv");

%% Loading workspace
load underwater

%% Calculating mean values


mean_energy = mean(energy);
mean_reward = mean(reward);
mean_thr = mean(thr);
mean_mod = mode(modulation);
mean_power = mode(power);

%% Plotting 

figure
plot(mean_energy, "LineWidth",1.5)
hold on
xlabel("Timestep")
ylabel("dB re μPa @ 1 m")
title("Mean Energy Consumption")
hold off

figure
plot(mean_reward,"LineWidth",1.5,"Color","yellow")
hold on
xlabel("Timestep")
ylabel("Reward")
title("Mean reward")
hold off

figure
plot(mean_thr, 'LineWidth', 1.5, "Color","red");
hold on
xlabel("Timestep");
ylabel("Throughput");
title("Mean Throughput");
hold off;

figure
plot(mean_mod,"LineWidth",1.5, "Color", "cyan");
hold on
xlabel("Timestep");
ylabel("Modulation");
title("Mode Modulation Scheme");
yticks([0:3])
yticklabels(["BPSK", "8PSK", "16PSK"])
hold off

figure
plot(mean_power,"LineWidth",1.5, "Color", "magenta")
hold on
xlabel("Timestep");
ylabel("Power level");
title("Mode Power level");
yticks([136, 156, 176]);
hold off


