import matplotlib.pyplot as plt
from pathlib import Path

fig, ax = plt.subplots()
ax.plot([0, 1, 2, 3], [0, 1, 4, 9])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Basic Line Plot')
fig.tight_layout()
plt.show()
fig.patch.set_alpha(0.0)
ax.set_facecolor('none')

# set the directory where you want to save the plots
save_dir = Path(r"c:\Users\gahle\OneDrive\Desktop\FH\Master\3. Semester\Datenaufbereitung und Visualisierung\GIT-Kursmaterialien\visdat-course\matplotlib-practise\output")
save_dir.mkdir(parents=True, exist_ok=True)

svg_path = save_dir / "basic_line_plot.svg"
fig.savefig(str(svg_path), transparent=True)