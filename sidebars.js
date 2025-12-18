module.exports = {
  docs: [
    'index',
    'organization',
    {
      type: 'category', 
      label: 'Programming Fundamentals',
      items: [
        'programming/paradigms',
      ],
    },
    {
      type: 'category',
      label: 'Tools & Workflow',
      items: [
        'tools-workflow/tools-workflow-overview',
        'tools-workflow/kickoff-assignment',
      ],
    },
    {
      type: 'category',
      label: 'C++ Programming',
      items: [
        'cpp/cpp-overview',
        'cpp/cpp-fundamentals',
        'cpp/cpp-control-flow',
        'cpp/cpp-oop', 
        'cpp/cpp-memory-management',
        'cpp/cpp-best-practices',
      ],
    },
    {
      type: 'category',
      label: 'Python Programming',
      items: [
        'python/python-overview',
        'python/python-data-types',
        'python/python-control-flow', 
        'python/python-oop',
        'python/python-file-handling',
        'python/python-libraries',
      ],
    },
    {
      type: 'category',
      label: 'Data Processing',
      items: [
        'data-processing/data-processing-overview',
        'data-processing/pandas-fundamentals',
        'data-processing/hdf5-storage',
        'data-processing/sample-datasets',
        'data-processing/motion-tracking-assignment',
      ],
    },
    {
      type: 'category',
      label: 'Visualization',
      items: [
        'visualization/introduction',
        'visualization/matplotlib',
        'visualization/3d-visualization-vtk',
        'visualization/meshio-file-conversion',
        'visualization/3d-visualization-pyvista',
        'visualization/mesh-visualization-workshop',
        'visualization/fem-coding-challenge',
      ],
    },
    {
      type: 'category',
      label: 'User Interfaces',
      items: [
        'user-interfaces/ui-overview',
        'user-interfaces/pyqt-basics',
        'user-interfaces/pyvista-qt-integration',
        'user-interfaces/qt-workshop',
      ],
    },
    {
      type: 'category',
      label: 'Advanced Topics',
      items: [
        'advanced-topics/cmake-overview',
        'advanced-topics/parallelization',
        'advanced-topics/final-assignment',
      ],
    },
  ],
};
