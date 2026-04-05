#!/usr/bin/env python3
"""
EcoTrack - Carbon Footprint Calculator and Tracker
An open-source tool to help individuals and organizations measure and reduce their carbon emissions.

Copyright (c) 2024 EcoTrack Contributors
Licensed under MIT License
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
import json


@dataclass
class EmissionEntry:
    """Represents a single carbon emission entry."""
    category: str
    activity: str
    amount: float
    unit: str
    date: datetime
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            'category': self.category,
            'activity': self.activity,
            'amount': self.amount,
            'unit': self.unit,
            'date': self.date.isoformat(),
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EmissionEntry':
        return cls(
            category=data['category'],
            activity=data['activity'],
            amount=data['amount'],
            unit=data['unit'],
            date=datetime.fromisoformat(data['date']),
            notes=data.get('notes')
        )


class CarbonCalculator:
    """Calculate carbon emissions based on various activities."""
    
    # Emission factors (kg CO2e per unit)
    EMISSION_FACTORS = {
        'transportation': {
            'car_gasoline': 2.31,  # kg CO2e per liter
            'car_diesel': 2.68,    # kg CO2e per liter
            'electric_car': 0.53,  # kg CO2e per kWh
            'bus': 0.105,          # kg CO2e per km
            'train': 0.041,        # kg CO2e per km
            'flight_domestic': 0.255,  # kg CO2e per km
            'flight_international': 0.195,  # kg CO2e per km
            'motorcycle': 0.113,   # kg CO2e per km
            'bicycle': 0.0,        # kg CO2e per km
            'walking': 0.0         # kg CO2e per km
        },
        'energy': {
            'electricity_grid': 0.53,  # kg CO2e per kWh (varies by region)
            'natural_gas': 2.0,        # kg CO2e per m³
            'heating_oil': 2.68,       # kg CO2e per liter
            'propane': 1.51,           # kg CO2e per liter
            'coal': 2.86,              # kg CO2e per kg
            'solar': 0.0,              # kg CO2e per kWh
            'wind': 0.0                # kg CO2e per kWh
        },
        'food': {
            'beef': 27.0,      # kg CO2e per kg
            'lamb': 39.0,      # kg CO2e per kg
            'pork': 12.0,      # kg CO2e per kg
            'chicken': 6.9,    # kg CO2e per kg
            'fish': 9.9,       # kg CO2e per kg
            'eggs': 4.8,       # kg CO2e per kg
            'dairy': 3.2,      # kg CO2e per kg
            'rice': 2.7,       # kg CO2e per kg
            'vegetables': 0.5, # kg CO2e per kg
            'fruits': 0.3,     # kg CO2e per kg
            'grains': 0.4      # kg CO2e per kg
        },
        'waste': {
            'landfill': 0.57,    # kg CO2e per kg waste
            'recycling': 0.1,    # kg CO2e per kg recycled
            'composting': 0.05,  # kg CO2e per kg composted
            'incineration': 0.3  # kg CO2e per kg burned
        }
    }
    
    @classmethod
    def calculate_emission(cls, category: str, activity: str, amount: float) -> float:
        """
        Calculate CO2 emissions for a given activity.
        
        Args:
            category: Emission category (transportation, energy, food, waste)
            activity: Specific activity within the category
            amount: Quantity of the activity
            
        Returns:
            Carbon emissions in kg CO2e
        """
        if category not in cls.EMISSION_FACTORS:
            raise ValueError(f"Unknown category: {category}")
        
        if activity not in cls.EMISSION_FACTORS[category]:
            raise ValueError(f"Unknown activity: {activity} in category {category}")
        
        emission_factor = cls.EMISSION_FACTORS[category][activity]
        return round(amount * emission_factor, 3)
    
    @classmethod
    def get_available_activities(cls, category: str) -> List[str]:
        """Get list of available activities for a category."""
        if category not in cls.EMISSION_FACTORS:
            raise ValueError(f"Unknown category: {category}")
        return list(cls.EMISSION_FACTORS[category].keys())
    
    @classmethod
    def get_categories(cls) -> List[str]:
        """Get list of all emission categories."""
        return list(cls.EMISSION_FACTORS.keys())


class EcoTracker:
    """Main tracker class for managing carbon footprint data."""
    
    def __init__(self, user_name: str = "User"):
        self.user_name = user_name
        self.entries: List[EmissionEntry] = []
        self.created_at = datetime.now()
    
    def add_entry(self, category: str, activity: str, amount: float, 
                  unit: str = "units", notes: Optional[str] = None) -> EmissionEntry:
        """Add a new emission entry."""
        emission = CarbonCalculator.calculate_emission(category, activity, amount)
        entry = EmissionEntry(
            category=category,
            activity=activity,
            amount=emission,
            unit="kg CO2e",
            date=datetime.now(),
            notes=notes
        )
        self.entries.append(entry)
        return entry
    
    def get_total_emissions(self) -> float:
        """Get total carbon emissions."""
        return round(sum(entry.amount for entry in self.entries), 3)
    
    def get_emissions_by_category(self) -> Dict[str, float]:
        """Get emissions grouped by category."""
        category_totals = {}
        for entry in self.entries:
            category_totals[entry.category] = category_totals.get(entry.category, 0) + entry.amount
        return {k: round(v, 3) for k, v in category_totals.items()}
    
    def get_emissions_by_date(self, start_date: datetime, end_date: datetime) -> float:
        """Get emissions within a date range."""
        total = sum(
            entry.amount for entry in self.entries
            if start_date <= entry.date <= end_date
        )
        return round(total, 3)
    
    def get_monthly_report(self, year: int, month: int) -> Dict:
        """Generate a monthly emissions report."""
        monthly_entries = [
            entry for entry in self.entries
            if entry.date.year == year and entry.date.month == month
        ]
        
        return {
            'user': self.user_name,
            'period': f"{year}-{month:02d}",
            'total_emissions': round(sum(e.amount for e in monthly_entries), 3),
            'entries_count': len(monthly_entries),
            'by_category': self._get_category_breakdown(monthly_entries),
            'top_activities': self._get_top_activities(monthly_entries, limit=5)
        }
    
    def _get_category_breakdown(self, entries: List[EmissionEntry]) -> Dict[str, float]:
        """Get category breakdown for given entries."""
        breakdown = {}
        for entry in entries:
            breakdown[entry.category] = breakdown.get(entry.category, 0) + entry.amount
        return {k: round(v, 3) for k, v in breakdown.items()}
    
    def _get_top_activities(self, entries: List[EmissionEntry], limit: int = 5) -> List[Dict]:
        """Get top emitting activities."""
        activity_totals = {}
        for entry in entries:
            key = f"{entry.category}:{entry.activity}"
            activity_totals[key] = activity_totals.get(key, 0) + entry.amount
        
        sorted_activities = sorted(activity_totals.items(), key=lambda x: x[1], reverse=True)
        return [
            {'activity': key, 'emissions': round(value, 3)}
            for key, value in sorted_activities[:limit]
        ]
    
    def save_to_file(self, filename: str) -> None:
        """Save tracker data to JSON file."""
        data = {
            'user_name': self.user_name,
            'created_at': self.created_at.isoformat(),
            'entries': [entry.to_dict() for entry in self.entries]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'EcoTracker':
        """Load tracker data from JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        tracker = cls(user_name=data['user_name'])
        tracker.created_at = datetime.fromisoformat(data['created_at'])
        tracker.entries = [EmissionEntry.from_dict(entry) for entry in data['entries']]
        return tracker
    
    def get_reduction_tips(self) -> List[str]:
        """Provide personalized reduction tips based on emission patterns."""
        tips = []
        category_emissions = self.get_emissions_by_category()
        
        if category_emissions.get('transportation', 0) > 0:
            tips.extend([
                "🚗 Consider carpooling or using public transportation",
                "🚲 Try cycling or walking for short distances",
                "⚡ If you have an electric vehicle, charge during off-peak hours",
                "✈️ Reduce air travel when possible; consider video conferences"
            ])
        
        if category_emissions.get('energy', 0) > 0:
            tips.extend([
                "💡 Switch to LED bulbs and energy-efficient appliances",
                "🌞 Consider installing solar panels",
                "🌡️ Optimize heating/cooling settings",
                "🔌 Unplug devices when not in use"
            ])
        
        if category_emissions.get('food', 0) > 0:
            tips.extend([
                "🥗 Reduce meat consumption, especially beef and lamb",
                "🛒 Buy local and seasonal produce",
                "🍽️ Reduce food waste by planning meals",
                "🌱 Try plant-based alternatives"
            ])
        
        if category_emissions.get('waste', 0) > 0:
            tips.extend([
                "♻️ Increase recycling and composting",
                "🛍️ Reduce single-use plastics",
                "📦 Choose products with minimal packaging",
                "🔄 Repair and reuse items instead of replacing"
            ])
        
        if not tips:
            tips.append("🌟 Start tracking your emissions to get personalized tips!")
        
        return tips


def main():
    """Demo function showing EcoTrack capabilities."""
    print("=" * 60)
    print("🌍 EcoTrack - Carbon Footprint Calculator")
    print("=" * 60)
    
    # Create a new tracker
    tracker = EcoTracker(user_name="EcoWarrior")
    
    # Add some sample entries
    print("\n📝 Adding sample emission entries...")
    
    tracker.add_entry('transportation', 'car_gasoline', 50, 'liters', 'Weekly commute')
    tracker.add_entry('transportation', 'flight_domestic', 800, 'km', 'Business trip')
    tracker.add_entry('energy', 'electricity_grid', 300, 'kWh', 'Monthly electricity')
    tracker.add_entry('energy', 'natural_gas', 100, 'm³', 'Heating')
    tracker.add_entry('food', 'beef', 5, 'kg', 'Monthly consumption')
    tracker.add_entry('food', 'vegetables', 20, 'kg', 'Monthly consumption')
    tracker.add_entry('waste', 'landfill', 30, 'kg', 'Monthly waste')
    
    # Display results
    print(f"\n📊 Total Emissions: {tracker.get_total_emissions()} kg CO2e")
    
    print("\n📈 Emissions by Category:")
    for category, emissions in tracker.get_emissions_by_category().items():
        print(f"   {category.capitalize()}: {emissions} kg CO2e")
    
    print("\n💡 Personalized Reduction Tips:")
    for tip in tracker.get_reduction_tips():
        print(f"   {tip}")
    
    # Save to file
    tracker.save_to_file('ecotrack_data.json')
    print("\n💾 Data saved to ecotrack_data.json")
    
    print("\n" + "=" * 60)
    print("Ready to track your carbon footprint! 🌱")
    print("=" * 60)


if __name__ == "__main__":
    main()
