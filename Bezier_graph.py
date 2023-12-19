import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

Path = mpath.Path

fig, ax = plt.subplots()
pp1 = mpatches.PathPatch(
    Path([(1, 47), (2, 39), (3, 46), (4,41),(5,63)],
         [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3]),
    fc="none", transform=ax.transData)
    # Path([(0.0, 0.0), (0.25, 0.025), (1, 0), (1, 1), (0,1), (0, 0)],
    #      [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY]),
    # fc="none", transform=ax.transData)

ax.add_patch(pp1)
ax.plot([1], [47], "ro",[2], [39], "ro",[3], [46], "ro",[4], [41], "ro",[5], [63], "ro") # mark the spots
ax.set_title('Courage and Fear pattern')

plt.show()