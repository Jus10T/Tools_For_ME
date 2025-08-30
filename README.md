# Tools For ME

A comprehensive PyQt6-based engineering toolkit designed for mechanical engineers, providing essential calculation tools and reference materials for structural analysis, thermodynamics, and unit conversions.

![Tools For ME](assets/icons/gearcalc.png)

## Features

### 🏗️ **Beam Analysis Tool**
- **Structural Analysis**: Complete finite element analysis for beam structures
- **Support Types**: Pinned, roller, and fixed supports
- **Loading Conditions**: Point loads, moment loads, and distributed loads
- **Interactive Design**: Visual beam modeling with load/support placement
- **Unit Systems**: Full support for both English and Metric/SI units
- **Results Output**: Displacement, rotation, shear, and moment calculations

### 🌡️ **Thermodynamics Reference**
- **Steam Tables**: Comprehensive SI and English unit thermodynamic property tables
- **Reference Charts**: Psychrometric charts and property diagrams
- **Unit Conversion**: Built-in thermodynamic unit conversion factors
- **PDF Viewer**: Integrated PDF viewer for engineering reference tables
- **Interactive Navigation**: Zoom controls and table selection interface

### 🔄 **Unit Converter**
- **Multiple Categories**: Length, area, mass/weight, pressure/stress, energy, time, and temperature
- **Dual Unit Systems**: Complete English and Metric/SI unit support
- **Real-time Conversion**: Instant conversion as you type
- **Engineering Focus**: Units commonly used in mechanical engineering
- **High Precision**: Support for scientific notation and high-precision calculations

## Installation

### Prerequisites
- Python 3.8 or higher
- PyQt6

### Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Equations-for-ME
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Dependencies

```
PyQt6==6.9.1
PyQt6-Qt6==6.9.1
PyQt6_sip==13.10.2
numpy
```

## Project Structure

```
Equations-for-ME/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── assets/                    # Application assets
│   ├── icons/                # UI icons and images
│   └── pdfs/                 # Reference PDF documents
│       └── thermopdfs/       # Thermodynamics tables
├── src/                      # Source code
│   ├── core/                 # Core calculations and models
│   │   ├── calculations/     # Unit factors and conversions
│   │   ├── models/          # Engineering models
│   │   └── misc_indexing/   # Steam table indexing
│   └── ui/                  # User interface
│       ├── dialogs/         # Dialog windows
│       ├── pages/           # Main application pages
│       ├── style/           # UI styling
│       └── mainwindow.py    # Main application window
```

## Usage Guide

### Beam Analysis
1. **Select Unit System**: Choose between English or Metric/SI units
2. **Define Beam Properties**:
   - Length
   - Modulus of Elasticity
   - Moment of Inertia
3. **Create Beam Model**: Click "MAKE" to generate the finite element model
4. **Add Supports**: Use the support buttons to add pinned, roller, or fixed supports
5. **Apply Loads**: Add point loads, moments, or distributed loads
6. **Run Analysis**: Click "RUN" to solve and view results

### Thermodynamics Reference
1. **Select Table Type**: Choose from unit conversion factors, thermodynamic tables, ideal gas summaries, psychrometric charts, or isentropic tables
2. **Choose Unit System**: For thermodynamic tables, select between Metric/SI or English units
3. **Navigate**: Use zoom controls (+/-) to adjust view
4. **Reference**: View comprehensive engineering reference materials

### Unit Conversion
1. **Select Category**: Choose the type of unit to convert (length, mass, pressure, etc.)
2. **Enter Value**: Input the value you want to convert
3. **Select Units**: Choose input and output units from the dropdowns
4. **View Result**: Conversion happens automatically as you type

## Technical Details

### Beam Analysis Engine
- **Finite Element Method**: Uses Euler-Bernoulli beam theory
- **Element Type**: 2-DOF beam elements (vertical displacement and rotation)
- **Matrix Assembly**: Global stiffness matrix assembly with boundary condition application
- **Solver**: Direct matrix inversion for displacement calculation
- **Load Types**: Supports concentrated and distributed loading

### Thermodynamics Integration
- **PDF Integration**: PyQt6 PDF viewer for seamless reference access
- **Table Management**: Organized thermodynamic property tables
- **Unit-Aware**: Automatic unit system selection for appropriate tables

### Architecture
- **Model-View Pattern**: Clean separation between calculation logic and UI
- **Modular Design**: Independent pages for different engineering tools
- **Extensible Framework**: Easy to add new calculation modules

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- New engineering calculation modules
- UI improvements
- Additional reference materials
- Documentation enhancements



## Contact

@tylerjus10@gmail.com
https://www.linkedin.com/in/justin-tyler-913ab834a/

---

**Tools For ME** - Making mechanical engineering calculations accessible and efficient.
