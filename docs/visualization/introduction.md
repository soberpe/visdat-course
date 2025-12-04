
# Introduction to Data Visualization

Data visualization is both a science and an art. It transforms raw data into graphical representations that reveal patterns, relationships, and insights, supporting exploration, analysis, and communication. In every scientific, engineering, or business context, effective visualization is essential for making data understandable and actionable.

## Academic Foundations
Visualization bridges the gap between raw data and human perception. By encoding information visually, we enable insight, discovery, and informed decision-making.

:::note Terminology
**Exploratory analysis** uses visualization to find patterns, trends, and outliers. **Explanatory analysis** uses visualization to communicate findings and support arguments.
:::

Visualization is fundamental for:
- Generating and testing hypotheses
- Validating results
- Communicating complex ideas clearly

## Types of Data
Understanding the nature of your data is the first step toward effective visualization. Common data types include:

- **Quantitative**: Numeric values, such as temperature or pressure, that can be measured and compared.
- **Categorical**: Groups or labels, such as species or region, that classify observations.
- **Time Series**: Data indexed by time, useful for tracking changes and trends.
- **Spatial/3D**: Data with geometric or spatial coordinates, often visualized in two or three dimensions.

:::info Background
Different data types require different visualization techniques. For example, time series data is often shown with line plots, while spatial data may require maps or 3D renderings.
:::

## Data vs View Concept
One of the most important principles in scientific visualization is the separation of **data** and **view**.

- **Data** refers to the underlying numbers, measurements, or categories—the facts you want to analyze.
- **View** is the graphical representation: plots, charts, maps, or any visual encoding of the data.

Changing the view does not alter the data; it only changes how the data is presented. This separation is critical for reproducibility, maintainability, and clarity in scientific computing.

:::tip Best Practice
Always perform data transformations, filtering, and analysis on the data itself (e.g., in a pandas DataFrame), not on the graphical elements. This ensures your workflow is transparent and repeatable.
:::

### Why Data/View Separation Matters
By keeping all operations within the data layer, you can:
- Reproduce and audit your analysis easily
- Switch between visualization libraries or styles with minimal code changes
- Avoid accidental distortion of results
- Build scalable and robust pipelines for research and production

The visualization layer should only encode the current state of the data, never modify it. This approach supports collaboration and makes your work easier to share and extend.

## Principles of Effective Visualization
High-quality visualizations are built on a foundation of clear principles:

- **Accuracy**: Represent data truthfully and avoid misleading scales or distortions.
- **Integrity**: Show data honestly, without cherry-picking or omitting important context.
- **Aesthetics**: Use design elements to support understanding, not distract from the message.
- **Cognitive Science**: Leverage how humans perceive color, shape, and pattern to make visualizations intuitive and accessible.

Each principle helps ensure that your visualizations are not only attractive, but also meaningful and trustworthy.

## Common Pitfalls
Even experienced practitioners can fall into common traps. Be aware of:

- **Misleading axes or scales**: Manipulating axes can exaggerate or hide trends.
- **Overplotting**: Displaying too much data in one view can obscure patterns.
- **Poor color choices**: Colors that are hard to distinguish or inaccessible to those with color vision deficiencies.

:::warning
Always check your visualizations for clarity and accessibility. Misleading or cluttered graphics can undermine your analysis and credibility.
:::

## 2D and 3D Visualization
Most visualizations are two-dimensional, such as scatter plots, line charts, bar graphs, and heatmaps. These are powerful tools for exploring and presenting data.

However, some scientific and engineering problems require three-dimensional visualization. 3D visualization is essential for spatial, geometric, or volumetric data—such as medical imaging, engineering simulations, or geographic information systems.

:::info Context
Python offers robust libraries for both 2D and 3D visualization. Mastering these tools will prepare you for a wide range of scientific and technical applications.
:::

Popular libraries for 3D visualization include:
- **VTK** (Visualization Toolkit): A powerful library for complex scientific and engineering visualizations.
- **PyVista**: A user-friendly interface built on VTK, making 3D plotting more accessible.

## Popular Python Libraries
Several Python libraries form the backbone of scientific visualization:

- **matplotlib**: The foundational plotting library for 2D graphics.
- **seaborn**: Built on matplotlib, it simplifies statistical data visualization.
- **plotly**: Enables interactive, web-based visualizations.
- **pandas**: Provides a DataFrame plotting interface, leveraging matplotlib for quick visual exploration.
- **VTK**: Supports advanced 3D visualization for scientific data.
- **PyVista**: Makes 3D plotting approachable and efficient.

Throughout this course, you will learn how to use these libraries to create effective visualizations for both 2D and 3D data. Building a strong foundation in these tools will empower you to tackle real-world scientific and engineering challenges with confidence.
