# EcoTrack Documentation

Welcome to the EcoTrack documentation! This guide will help you understand and use the project effectively.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [API Reference](#api-reference)
5. [Contributing](#contributing)
6. [FAQ](#faq)

## Introduction

EcoTrack is an open-source carbon footprint calculator that helps individuals and organizations measure their environmental impact across four main categories:

- **Transportation**: Cars, flights, public transit, cycling
- **Energy**: Electricity, heating, renewable sources
- **Food**: Meat, dairy, vegetables, grains
- **Waste**: Landfill, recycling, composting

### Why Track Your Carbon Footprint?

- Understand your environmental impact
- Identify areas for improvement
- Set reduction goals
- Track progress over time
- Make informed lifestyle choices

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install from Source

```bash
git clone https://github.com/yourusername/ecotrack.git
cd ecotrack
pip install -e .
```

### Verify Installation

```bash
python -c "from src.ecotrack import EcoTracker; print('EcoTrack installed successfully!')"
```

## Quick Start

### Basic Example

```python
from src.ecotrack import EcoTracker

# Create a tracker
tracker = EcoTracker("Your Name")

# Add entries
tracker.add_entry('transportation', 'car_gasoline', 40, 'liters')
tracker.add_entry('energy', 'electricity_grid', 300, 'kWh')
tracker.add_entry('food', 'beef', 5, 'kg')

# View results
print(f"Total emissions: {tracker.get_total_emissions()} kg CO2e")

# Get tips
for tip in tracker.get_reduction_tips():
    print(tip)
```

### Command Line Usage

```bash
# Run the demo
python src/ecotrack.py
```

## API Reference

### EmissionEntry

Data class representing a single emission entry.

**Attributes:**
- `category` (str): Emission category
- `activity` (str): Specific activity
- `amount` (float): CO2 emissions in kg
- `unit` (str): Unit of measurement
- `date` (datetime): Entry date
- `notes` (str, optional): Additional notes

**Methods:**
- `to_dict()`: Convert to dictionary
- `from_dict(data)`: Create from dictionary

### CarbonCalculator

Utility class for calculating emissions.

**Methods:**
- `calculate_emission(category, activity, amount)`: Calculate CO2 emissions
- `get_categories()`: Get all available categories
- `get_available_activities(category)`: Get activities for a category

**Example:**
```python
from src.ecotrack import CarbonCalculator

# Calculate emissions
emissions = CarbonCalculator.calculate_emission(
    'transportation', 
    'car_gasoline', 
    50
)
print(f"{emissions} kg CO2e")

# Get categories
categories = CarbonCalculator.get_categories()

# Get activities
activities = CarbonCalculator.get_available_activities('transportation')
```

### EcoTracker

Main class for tracking emissions.

**Constructor:**
```python
tracker = EcoTracker(user_name="Your Name")
```

**Methods:**

#### add_entry(category, activity, amount, unit="units", notes=None)
Add a new emission entry.

```python
entry = tracker.add_entry(
    'transportation',
    'car_gasoline',
    50,
    'liters',
    'Monthly commute'
)
```

#### get_total_emissions()
Get total emissions in kg CO2e.

```python
total = tracker.get_total_emissions()
```

#### get_emissions_by_category()
Get emissions grouped by category.

```python
by_category = tracker.get_emissions_by_category()
for category, emissions in by_category.items():
    print(f"{category}: {emissions} kg CO2e")
```

#### get_monthly_report(year, month)
Generate a monthly report.

```python
report = tracker.get_monthly_report(2024, 1)
print(report['total_emissions'])
print(report['by_category'])
print(report['top_activities'])
```

#### save_to_file(filename)
Save tracker data to JSON file.

```python
tracker.save_to_file('my_data.json')
```

#### load_from_file(filename)
Load tracker data from JSON file.

```python
tracker = EcoTracker.load_from_file('my_data.json')
```

#### get_reduction_tips()
Get personalized reduction tips.

```python
tips = tracker.get_reduction_tips()
for tip in tips:
    print(tip)
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed contribution guidelines.

### Quick Start for Contributors

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/ecotrack.git
cd ecotrack

# Setup development environment
python -m venv venv
source venv/bin/activate
pip install -e .
pip install pytest

# Run tests
python -m pytest tests/ -v
```

## FAQ

### Q: How accurate are the emission factors?

A: Our emission factors are based on scientific research from sources like IPCC and EPA. However, actual emissions can vary by region and specific circumstances.

### Q: Can I add custom activities?

A: Yes! You can extend the `EMISSION_FACTORS` dictionary in `CarbonCalculator` with your own activities and factors.

### Q: Is my data private?

A: Yes! All data is stored locally on your device. We don't collect or transmit any personal information.

### Q: Can I export my data?

A: Yes! Use `save_to_file()` to export your data as JSON. You can also load it back with `load_from_file()`.

### Q: How often should I track my emissions?

A: We recommend tracking regularly - weekly or monthly - to get accurate insights into your habits and progress.

### Q: What units should I use?

A: Use the units specified in the emission factors:
- Transportation: liters (fuel), km (distance), kWh (electric)
- Energy: kWh (electricity), m³ (gas), liters (oil)
- Food: kg (weight)
- Waste: kg (weight)

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ecotrack/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ecotrack/discussions)

---

**Start tracking your carbon footprint today! 🌍**
