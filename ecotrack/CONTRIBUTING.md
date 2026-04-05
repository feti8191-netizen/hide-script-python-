# Contributing to EcoTrack 🌱

Thank you for your interest in contributing to EcoTrack! Every contribution helps make our planet a better place.

## 🤝 How to Contribute

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/ecotrack.git
cd ecotrack
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number
```

### 3. Make Your Changes

- Write clean, documented code
- Follow existing code style
- Add tests for new features
- Update documentation as needed

### 4. Test Your Changes

```bash
# Run existing tests
python -m pytest tests/ -v

# Run the demo
python src/ecotrack.py
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

**Commit Message Guidelines:**
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference any related issues
- Screenshots if applicable
- Test results

## 📋 Contribution Ideas

### Easy Wins
- ✏️ Fix typos in documentation
- 📝 Add usage examples
- 🧪 Add test cases
- 🔍 Improve error messages

### Medium Effort
- ➕ Add new emission activities
- 🌍 Add region-specific emission factors
- 📊 Add data visualization features
- 💾 Add support for CSV export

### Advanced
- 🎨 Build a web interface
- 📱 Create a mobile app
- 🔌 Add API integrations
- 📈 Implement machine learning for predictions

## 🎯 Areas We Need Help

1. **Emission Factors**: Help us add more accurate, region-specific emission factors
2. **New Categories**: Suggest and implement new emission categories
3. **User Interface**: Build a GUI or web interface
4. **Data Visualization**: Create charts and graphs for emissions data
5. **Translations**: Help translate EcoTrack to other languages
6. **Documentation**: Improve docs, add tutorials, create videos

## 📏 Code Style

- Use type hints
- Write docstrings for all public functions
- Follow PEP 8 guidelines
- Keep functions focused and small
- Use meaningful variable names

Example:
```python
def calculate_emission(category: str, activity: str, amount: float) -> float:
    """
    Calculate CO2 emissions for a given activity.
    
    Args:
        category: Emission category (transportation, energy, food, waste)
        activity: Specific activity within the category
        amount: Quantity of the activity
        
    Returns:
        Carbon emissions in kg CO2e
    """
    # Implementation here
```

## 🧪 Testing Guidelines

- Write tests for all new features
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use descriptive test names

Example:
```python
def test_calculate_car_emissions():
    """Test carbon calculation for gasoline car."""
    emissions = CarbonCalculator.calculate_emission(
        'transportation', 
        'car_gasoline', 
        10
    )
    assert emissions == 23.1  # 10 liters * 2.31 kg/liter
```

## 📞 Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas
- Check existing issues before creating new ones

## 🌟 Recognition

All contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for helping make EcoTrack better! 🌍💚

---

**Together, we can make a difference!**
