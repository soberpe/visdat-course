import vtk as vtk

# 1. Create source (geometry)
cone = vtk.vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

# 2. Create mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

# 3. Create actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# 4. Create renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)  # RGB background

# 5. Create render window
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(800, 600)

# 6. Create interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)

# Set trackball camera style
style = vtk.vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(style)

# Create and configure camera
camera = vtk.vtkCamera()
camera.SetFocalPoint(0.0, 0.0, 0.0)
camera.SetPosition(5.0, 5.0, 5.0)
camera.SetViewUp(0.0, 1.0, 0.0)
camera.SetClippingRange(0.1, 100.0)

# Apply camera to renderer
renderer.SetActiveCamera(camera)
renderer.ResetCamera()

# Or modify existing camera
camera = renderer.GetActiveCamera()
camera.Azimuth(45)   # Rotate around scene
camera.Elevation(30)  # Change viewing angle
camera.Zoom(1.5)      # Zoom in

# Create directional light (default)
light = vtk.vtkLight()
light.SetPosition(camera.GetPosition())
light.SetFocalPoint(camera.GetFocalPoint())
light.SetColor(1.0, 1.0, 1.0)  # White light
light.SwitchOn()

renderer.AddLight(light)

# Create positional light (spotlight effect)
spotlight = vtk.vtkLight()
spotlight.PositionalOn()
spotlight.SetPosition(5.0, 5.0, 5.0)
spotlight.SetFocalPoint(0.0, 0.0, 0.0)
spotlight.SetConeAngle(30)  # Spotlight cone angle
spotlight.SetColor(1.0, 0.0, 0.0)  # Red light

renderer.AddLight(spotlight)

# 7. Initialize and start
renderWindow.Render()
interactor.Start()
