# EcoTrack - Carbon Footprint Calculator & Tracker 🌍

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Track your carbon emissions, understand your environmental impact, and get personalized tips to reduce your carbon footprint.**

## 🌟 Features

- **Multi-Category Tracking**: Track emissions from transportation, energy consumption, food choices, and waste
- **Accurate Calculations**: Based on scientifically-backed emission factors
- **Personalized Insights**: Get custom reduction tips based on your emission patterns
- **Data Export/Import**: Save and load your tracking data in JSON format
- **Monthly Reports**: Generate detailed reports of your monthly emissions
- **Easy to Extend**: Modular design makes it easy to add new categories and activities

## 📦 Installation

### From Source

```bash
git clone https://github.com/yourusername/ecotrack.git
cd ecotrack
pip install -e .
```

### Requirements

- Python 3.8 or higher
- No external dependencies required (uses only standard library)

## 🚀 Quick Start

```python
from src.ecotrack import EcoTracker

# Create a new tracker
tracker = EcoTracker(user_name="YourName")

# Add emission entries
tracker.add_entry('transportation', 'car_gasoline', 50, 'liters', 'Weekly commute')
tracker.add_entry('energy', 'electricity_grid', 300, 'kWh', 'Monthly electricity')
tracker.add_entry('food', 'beef', 5, 'kg', 'Monthly consumption')

# View your total emissions
print(f"Total: {tracker.get_total_emissions()} kg CO2e")

# Get emissions by category
for category, emissions in tracker.get_emissions_by_category().items():
    print(f"{category}: {emissions} kg CO2e")

# Get personalized reduction tips
for tip in tracker.get_reduction_tips():
    print(tip)

# Save your data
tracker.save_to_file('my_carbon_data.json')
```

## 📖 Usage Examples

### Available Categories and Activities

```python
from src.ecotrack import CarbonCalculator

# Get all categories
categories = CarbonCalculator.get_categories()
print(categories)  # ['transportation', 'energy', 'food', 'waste']

# Get activities for a category
activities = CarbonCalculator.get_available_activities('transportation')
print(activities)
# ['car_gasoline', 'car_diesel', 'electric_car', 'bus', 'train', ...]
```

### Calculate Specific Emissions

```python
from src.ecotrack import CarbonCalculator

# Calculate emissions for driving 100 km with a gasoline car
# Note: You need to convert km to liters based on your car's efficiency
emissions = CarbonCalculator.calculate_emission('transportation', 'car_gasoline', 10)
print(f"10 liters of gasoline = {emissions} kg CO2e")
```

### Generate Monthly Report

```python
from datetime import datetime

report = tracker.get_monthly_report(year=2024, month=1)
print(f"Month: {report['period']}")
print(f"Total Emissions: {report['total_emissions']} kg CO2e")
print(f"Entries: {report['entries_count']}")
print("By Category:", report['by_category'])
print("Top Activities:", report['top_activities'])
```

### Load Saved Data

```python
from src.ecotrack import EcoTracker

# Load previously saved data
tracker = EcoTracker.load_from_file('my_carbon_data.json')
print(f"Welcome back, {tracker.user_name}!")
print(f"Total tracked emissions: {tracker.get_total_emissions()} kg CO2e")
```

## 📊 Emission Factors

EcoTrack uses the following emission factors (kg CO2e per unit):

### Transportation
- Car (gasoline): 2.31 kg CO2e/liter
- Car (diesel): 2.68 kg CO2e/liter
- Electric car: 0.53 kg CO2e/kWh
- Bus: 0.105 kg CO2e/km
- Train: 0.041 kg CO2e/km
- Flight (domestic): 0.255 kg CO2e/km
- Flight (international): 0.195 kg CO2e/km
- Motorcycle: 0.113 kg CO2e/km
- Bicycle/Walking: 0 kg CO2e/km

### Energy
- Electricity (grid): 0.53 kg CO2e/kWh
- Natural gas: 2.0 kg CO2e/m³
- Heating oil: 2.68 kg CO2e/liter
- Solar/Wind: 0 kg CO2e/kWh

### Food
- Beef: 27.0 kg CO2e/kg
- Lamb: 39.0 kg CO2e/kg
- Pork: 12.0 kg CO2e/kg
- Chicken: 6.9 kg CO2e/kg
- Vegetables: 0.5 kg CO2e/kg
- Fruits: 0.3 kg CO2e/kg

### Waste
- Landfill: 0.57 kg CO2e/kg
- Recycling: 0.1 kg CO2e/kg
- Composting: 0.05 kg CO2e/kg

*Note: Emission factors are approximate and may vary by region. Sources include IPCC, EPA, and various lifecycle assessment studies.*

## 🧪 Running Tests

```bash
python -m pytest tests/
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute

1. **Add new emission activities** - Help expand our database
2. **Improve calculations** - Share more accurate emission factors
3. **Add features** - Suggest and implement new functionality
4. **Write documentation** - Help others understand and use EcoTrack
5. **Report bugs** - Found an issue? Let us know!
6. **Spread the word** - Share EcoTrack with others

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ecotrack.git
cd ecotrack

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/ -v
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Emission factors sourced from IPCC Guidelines, EPA, and peer-reviewed lifecycle assessment studies
- Inspired by global climate action initiatives
- Built with ❤️ by the open-source community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ecotrack/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ecotrack/discussions)
- **Email**: eco@example.com (replace with actual contact)

## 🌱 Join the Movement

Every small action counts. By tracking your carbon footprint, you're taking the first step toward a more sustainable future. Share your progress, challenge yourself to reduce emissions, and inspire others to join the climate action movement!

---

**Made with 🌍 for a sustainable future**

*“The greatest threat to our planet is the belief that someone else will save it.” – Robert Swan*
