clearvars
clc
close all

data_1a = load('annual_ECG_1a.csv');
data_1w = load('annual_ECG_1w.csv'); %"œwiadczenia wysokospecjalistyczne"

years = data_1a(:,1);
sums = data_1a(:,2) + [zeros(6,1);data_1w(:,2)];

figure(1)
bar(years, sums,0.2,'black')

title('Number of ECG diagnostics in Poland')
xlabel('year')
ylabel('sum')
grid on