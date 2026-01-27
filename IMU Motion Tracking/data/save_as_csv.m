% Load Data
load('data_2.mat')

% Tabelle aus dem Timetable erzeugen
accTable = timetable2table(Acceleration);

% CSV speichern
writetable(accTable, 'hinterkoerner_acceleration.csv');

gyro = AngularVelocity;

gyroTable = timetable2table(gyro);

writetable(gyroTable, 'hinterkoerner_gyroscope.csv');
