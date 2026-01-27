import matplotlib.pyplot as plt
import numpy as np

# Hinweis: Speichere die Datei als .py. In VS Code kannst du jede Section (# %%) einzeln
# mit "Run Cell" ausführen (Play‑Icon oder Shift+Enter).

# %% Mehrere Linien in einer Achse
# Kurzes Beispiel: zwei Linien mit Legende und Titel
x = [1, 2, 3, 4]
plt.figure()                  # neue Figur (optional)
plt.plot(x, [1, 4, 9, 16], 'r-', label='quadratisch')   # plot1
plt.plot(x, [1, 2, 3, 4], 'b--', label='linear')        # plot2
plt.legend()
plt.title('Mehrere Linien in einer Achse')
plt.show()

# %% Mehrere Linien mit verschiedenen Markern und Linienstilen
# evenly sampled time at 200ms intervals
t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles
plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
plt.title('Mehrere Linien: verschiedene Stile')
plt.show()

# %% Plotting with keyword strings (Beispiel mit dict data)
# Erzeugt Scatter mit Farben und Größen aus einem Dictionary
data = {'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)}
data['b'] = data['a'] + 10 * np.random.randn(50)
data['d'] = np.abs(data['d']) * 100

plt.figure()
plt.scatter('a', 'b', c='c', s='d', data=data)
plt.xlabel('entry a')
plt.ylabel('entry b')
plt.title('Scatter mit Keyword-Argumenten und dict')
plt.show()

# %% Plotting with categorical variables
# Balken, Scatter und Linienplot für kategoriale x-Werte
names = ['group_a', 'group_b', 'group_c']
values = [1, 10, 100]

plt.figure(figsize=(9, 3))

plt.subplot(131)
plt.bar(names, values)
plt.title('Bar')

plt.subplot(132)
plt.scatter(names, values)
plt.title('Scatter')

plt.subplot(133)
plt.plot(names, values)
plt.title('Line')

plt.suptitle('Categorical Plotting')
plt.tight_layout()
plt.show()

# %% Controlling line properties
# Beispiele für Linienbreite, Antialiasing und setp
x = np.linspace(0, 10, 200)
y = np.sin(x)
x1 = np.linspace(0, 10, 50)
y1 = np.sin(x1) + 0.5
x2 = np.linspace(0, 10, 50)
y2 = 0.5 * np.cos(x2)

plt.figure(figsize=(8, 4))
# einfacher Plot mit veränderter Linienbreite
plt.plot(x, y, linewidth=2.0, label='sin(x)')

# Zugriff auf die Linie als Objekt und Antialiasing ausschalten
line, = plt.plot(x, y, '-', label='sin(x) (object)')
line.set_antialiased(False)

# mehrere Linien auf einmal plotten
lines = plt.plot(x1, y1, x2, y2)

# setp mit Keyword-Argumenten
plt.setp(lines, color='r', linewidth=2.0)

# oder MATLAB-Style String-Paare (gleiches Ergebnis)
plt.setp(lines, 'color', 'r', 'linewidth', 2.0)

plt.legend()
plt.title('Controlling line properties')
plt.xlabel('x')
plt.ylabel('y')
plt.tight_layout()
plt.show()

# %% Working with multiple figures and Axes (self-contained)
# Funktion definieren und zwei Subplots in einer Figur zeigen
def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)

plt.figure()
plt.subplot(211)
plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')
plt.title('Exponentiell abklingende Schwingung (Datenpunkte und Linie)')

plt.subplot(212)
plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
plt.title('Reine Cosinus-Funktion')
plt.tight_layout()
plt.show()

# %% Mehrere Figuren / Subplots-Handling (kurzes Beispiel)
plt.figure(1)                # erste Figur
plt.subplot(211)
plt.plot([1, 2, 3])
plt.subplot(212)
plt.plot([4, 5, 6])

plt.figure(2)                # zweite Figur
plt.plot([4, 5, 6])          # erzeugt standardmäßig einen Subplot

plt.figure(1)                # wechsle zurück zur ersten Figur
plt.subplot(211)             # mache subplot(211) wieder aktuell
plt.title('Easy as 1, 2, 3')

# %% Histogramm-Beispiel mit Textannotation
mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)

plt.figure()
n, bins, patches = plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.show()

# %% Annotieren eines lokalen Maximums
plt.figure()
t = np.arange(0.0, 5.0, 0.01)
s = np.cos(2*np.pi*t)
line, = plt.plot(t, s, lw=2)

plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.ylim(-2, 2)
plt.title('Annotation Beispiel')
plt.show()

# %% Verschiedene Achsenskalierungen
# Reproduzierbare Zufallszahlen erzeugen
np.random.seed(19680801)

# Zufallsdaten im Intervall (0,1) erzeugen und sortieren
y = np.random.normal(loc=0.5, scale=0.4, size=1000)
y = y[(y > 0) & (y < 1)]
y.sort()
x = np.arange(len(y))

plt.figure(figsize=(8, 6))

# linear
plt.subplot(221)
plt.plot(x, y)
plt.yscale('linear')
plt.title('linear')
plt.grid(True)

# log
plt.subplot(222)
plt.plot(x, y)
plt.yscale('log')
plt.title('log')
plt.grid(True)

# symmetric log
plt.subplot(223)
plt.plot(x, y - y.mean())
plt.yscale('symlog', linthresh=0.01)
plt.title('symlog')
plt.grid(True)

# logit
plt.subplot(224)
plt.plot(x, y)
plt.yscale('logit')
plt.title('logit')
plt.grid(True)

# Adjust the subplot layout for readability
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95,
                    hspace=0.25, wspace=0.35)

plt.show()