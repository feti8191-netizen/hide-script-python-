# EcoTrack Usage Examples

This directory contains practical examples of how to use EcoTrack.

## Basic Usage

```python
from src.ecotrack import EcoTracker, CarbonCalculator

# Create a tracker
tracker = EcoTracker(user_name="John Doe")

# Track your daily commute (50 liters of gasoline per month)
tracker.add_entry(
    category='transportation',
    activity='car_gasoline',
    amount=50,
    unit='liters',
    notes='Monthly commute'
)

# Track home electricity usage
tracker.add_entry(
    category='energy',
    activity='electricity_grid',
    amount=350,
    unit='kWh',
    notes='Monthly electricity bill'
)

# Track food consumption
tracker.add_entry(
    category='food',
    activity='beef',
    amount=3,
    unit='kg',
    notes='Weekly beef consumption'
)

# View total emissions
print(f"Total: {tracker.get_total_emissions()} kg CO2e")

# Get personalized tips
for tip in tracker.get_reduction_tips():
    print(tip)
```

## Monthly Tracking Example

```python
from src.ecotrack import EcoTracker
from datetime import datetime

tracker = EcoTracker("Monthly Tracker")

# Week 1
tracker.add_entry('transportation', 'car_gasoline', 15, 'liters')
tracker.add_entry('food', 'chicken', 2, 'kg')

# Week 2
tracker.add_entry('transportation', 'bus', 50, 'km')
tracker.add_entry('energy', 'natural_gas', 25, 'm³')

# Week 3
tracker.add_entry('transportation', 'car_gasoline', 12, 'liters')
tracker.add_entry('food', 'vegetables', 5, 'kg')

# Week 4
tracker.add_entry('energy', 'electricity_grid', 100, 'kWh')
tracker.add_entry('waste', 'recycling', 8, 'kg')

# Generate monthly report
report = tracker.get_monthly_report(2024, 1)
print(f"Month: {report['period']}")
print(f"Total: {report['total_emissions']} kg CO2e")
print(f"By Category: {report['by_category']}")
```

## Compare Different Scenarios

```python
from src.ecotrack import CarbonCalculator

# Scenario 1: Gasoline car for 1000 km (assuming 8L/100km)
gas_car = CarbonCalculator.calculate_emission('transportation', 'car_gasoline', 80)

# Scenario 2: Electric car for 1000 km (assuming 20 kWh/100km)
electric_car = CarbonCalculator.calculate_emission('transportation', 'electric_car', 200)

# Scenario 3: Public transport for 1000 km
bus = CarbonCalculator.calculate_emission('transportation', 'bus', 1000)

# Scenario 4: Cycling for 1000 km
bike = CarbonCalculator.calculate_emission('transportation', 'bicycle', 1000)

print("Transportation comparison for 1000 km:")
print(f"Gasoline car: {gas_car} kg CO2e")
print(f"Electric car: {electric_car} kg CO2e")
print(f"Bus: {bus} kg CO2e")
print(f"Bicycle: {bike} kg CO2e")
print(f"Savings (car vs bike): {gas_car - bike} kg CO2e")
```

## Food Choices Impact

```python
from src.ecotrack import CarbonCalculator

# Weekly protein choices (per kg)
beef_impact = CarbonCalculator.calculate_emission('food', 'beef', 1)
chicken_impact = CarbonCalculator.calculate_emission('food', 'chicken', 1)
vegetables_impact = CarbonCalculator.calculate_emission('food', 'vegetables', 1)

print("Protein source impact (per kg):")
print(f"Beef: {beef_impact} kg CO2e")
print(f"Chicken: {chicken_impact} kg CO2e")
print(f"Vegetables: {vegetables_impact} kg CO2e")
print(f"\nIf you replace 1kg beef with vegetables: save {beef_impact - vegetables_impact} kg CO2e!")
```

## Save and Resume Tracking

```python
from src.ecotrack import EcoTracker

# Day 1: Start tracking
tracker = EcoTracker("Persistent User")
tracker.add_entry('transportation', 'car_gasoline', 20, 'liters')
tracker.save_to_file('my_tracking.json')

# Day 2: Load and continue
tracker = EcoTracker.load_from_file('my_tracking.json')
tracker.add_entry('energy', 'electricity_grid', 15, 'kWh')
tracker.save_to_file('my_tracking.json')

# Check progress
print(f"Total tracked: {tracker.get_total_emissions()} kg CO2e")
print(f"Entries: {len(tracker.entries)}")
```

## Energy Source Comparison

```python
from src.ecotrack import CarbonCalculator

# Monthly electricity consumption: 500 kWh
grid_power = CarbonCalculator.calculate_emission('energy', 'electricity_grid', 500)
solar_power = CarbonCalculator.calculate_emission('energy', 'solar', 500)
wind_power = CarbonCalculator.calculate_emission('energy', 'wind', 500)

print("Monthly energy impact (500 kWh):")
print(f"Grid electricity: {grid_power} kg CO2e")
print(f"Solar: {solar_power} kg CO2e")
print(f"Wind: {wind_power} kg CO2e")
print(f"\nSwitching to solar saves: {grid_power} kg CO2e per month!")
```

---

Try these examples and modify them to fit your lifestyle! 🌱
