# OrtoIoT Preset Creator

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
</p>

A standalone desktop application for creating and managing cultivation presets for the OrtoIoT Hydroponic Automation System.

## 🌟 Features

### 🎯 **Advanced Preset Creation**
- **Static Presets**: Fixed settings throughout the growth cycle
- **Progressive Presets**: Multi-phase growth with automatic transitions
- **Comprehensive Automation Settings**: Temperature, humidity, lighting, irrigation, and more

### 🏷️ **Smart Categorization System**
- **Cannabis**: Indica, Sativa, Ruderalis, Hybrid subcategories
- **Vegetables**: Leafy greens, fruiting plants, culinary herbs
- **Flowers**: Annuals, perennials with seasonal variations
- **Specialty**: Mushrooms, microgreens, and exotic plants

### 🔧 **Professional Tools**
- **Visual Editor**: Intuitive interface for all automation parameters
- **Real-time Preview**: JSON preview of your preset
- **Batch Operations**: Export multiple presets by category
- **Validation System**: Automatic checks for preset integrity
- **Import/Export**: Full compatibility with OrtoIoT v4.0+

### 🎨 **Modern Interface**
- **Responsive Design**: Adaptable to different screen sizes
- **CustomTkinter Support**: Modern, sleek appearance
- **Keyboard Shortcuts**: Efficient workflow
- **Search & Filter**: Quick preset discovery

## 📸 Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────────────┐
│ File  Edit  Tools  Help                    🔍 Search: _____ │
├─────────────────────────────────────────────────────────────┤
│ 🆕 New  💾 Save  📤 Export  ✅ Validate                     │
├─────────────────┬───────────────────────────────────────────┤
│ Preset Library  │ Basic Info | Automation | Phases | Preview│
│ ├─ Cannabis     │                                           │
│ │  ├─ 🌿 Indica │ Name: Northern Lights                     │
│ │  └─ 🌿 Sativa │ Category: Cannabis > Indica              │
│ ├─ Vegetables   │ Type: Static                              │
│ └─ Flowers      │                                           │
│                 │ 🌡️ Temperature: 24°C ✅                   │
│ 12 presets      │ 💧 Humidity: 60% ✅                       │
└─────────────────┴───────────────────────────────────────────┘
```

## 🚀 Quick Start

### Option 1: Download Executable (Recommended)
1. Download the latest release from [Releases](https://github.com/ortoiot/preset-creator/releases)
2. Extract the ZIP file
3. Run `OrtoIoT-Preset-Creator.exe`

### Option 2: Run from Source
```bash
git clone https://github.com/ortoiot/preset-creator.git
cd preset-creator
pip install -r requirements.txt
python preset_creator.py
```

## 📦 Installation

### System Requirements
- **Windows**: 10/11 (64-bit)
- **Linux**: Ubuntu 18.04+ or equivalent
- **macOS**: 10.14+ (64-bit)
- **Python**: 3.8+ (if running from source)

### Dependencies
```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `customtkinter>=5.2.0` - Modern UI components
- `pillow>=9.0.0` - Image processing

## 🛠️ Building from Source

### Windows
```cmd
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "OrtoIoT-Preset-Creator" preset_creator.py
```

### Linux/macOS
```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "OrtoIoT-Preset-Creator" preset_creator.py
```

### Advanced Build
```bash
# Use the provided spec file for advanced configuration
pyinstaller pyinstaller.spec
```

## 📘 User Guide

### Creating Your First Preset

1. **Start New Preset**
   - Click `🆕 New Preset` or press `Ctrl+N`
   - Fill in basic information (name, description, category)

2. **Configure Automation Settings**
   - Switch to "Automation Settings" tab
   - Enable desired automations (temperature, humidity, etc.)
   - Set target values and parameters

3. **Save and Export**
   - Click `💾 Save` to add to library
   - Click `📤 Export` to create OrtoIoT-compatible file

### Automation Types

| Automation | Parameters | Description |
|------------|------------|-------------|
| 🌡️ Temperature | Target (°C), Hysteresis | Climate control |
| 💧 Humidity | Target (%), Hysteresis | Moisture management |
| 💨 CO2 | Target (ppm), Hysteresis | Carbon dioxide levels |
| ⚡ EC | Target (mS/cm), Hysteresis | Electrical conductivity |
| 🚿 Irrigation | Duration (min), Interval (h) | Watering schedule |
| 💡 Lighting | Start time, Duration (h) | Light cycle |
| 🔆 Lamp | Distance (cm) | Lamp positioning |
| 🌪️ Ventilation | Duration (min), Interval (h) | Air circulation |
| 🌿 Foliar | Frequency (days), Duration (min) | Foliar feeding |

### Category System

#### Cannabis
- **Indica**: Pure indica, indica-dominant hybrids
- **Sativa**: Pure sativa, sativa-dominant hybrids  
- **Ruderalis**: Autoflowering varieties
- **Hybrid**: Balanced hybrids

#### Vegetables
- **Leafy Greens**: Lettuce, spinach, kale, arugula
- **Fruiting Plants**: Tomatoes, peppers, cucumbers
- **Herbs**: Basil, cilantro, parsley, oregano

#### Flowers
- **Annuals**: Seasonal flowering plants
- **Perennials**: Long-term flowering plants

#### Specialty
- **Mushrooms**: Gourmet and medicinal varieties
- **Microgreens**: Fast-growing nutrient-dense greens

## 🔄 Integration with OrtoIoT

### Exporting Presets
1. Select preset(s) to export
2. Choose export format:
   - **Single Preset**: Individual JSON file
   - **Batch Export**: Multiple presets by category
   - **Complete Library**: All presets in one file

### Importing to OrtoIoT
1. In OrtoIoT web interface, go to Presets page
2. Click "Import" button
3. Select the exported JSON file
4. Confirm import

### File Formats

**Single Preset Export:**
```json
{
  "preset": {
    "id": "uuid",
    "name": "Northern Lights",
    "category": "cannabis",
    "subcategory": "indica",
    "settings": { ... }
  },
  "export_info": {
    "created_with": "OrtoIoT Preset Creator v1.0",
    "compatible_with": "OrtoIoT v4.0+"
  }
}
```

**Batch Export:**
```json
{
  "data": {
    "version": "2.0",
    "presets": { ... }
  },
  "export_info": {
    "preset_count": 5,
    "category": "cannabis"
  }
}
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New preset |
| `Ctrl+O` | Open library |
| `Ctrl+S` | Save library |
| `Ctrl+E` | Export current preset |
| `Ctrl+I` | Import preset |
| `Ctrl+D` | Duplicate preset |
| `Delete` | Delete selected preset |
| `F5` | Refresh preset list |
| `Ctrl+F` | Focus search box |

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/ortoiot/preset-creator.git
cd preset-creator
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m pytest tests/
```

### Reporting Issues
- Use GitHub Issues for bug reports
- Include steps to reproduce
- Attach sample preset files if relevant

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Wiki](https://github.com/ortoiot/preset-creator/wiki)
- **Community**: [Discord](https://discord.gg/ortoiot)
- **Issues**: [GitHub Issues](https://github.com/ortoiot/preset-creator/issues)
- **Email**: support@ortoiot.com

## 🎯 Roadmap

### v1.1 (Next Release)
- [ ] Progressive preset editor
- [ ] Preset templates
- [ ] Advanced validation rules
- [ ] Preset sharing community

### v1.2 (Future)
- [ ] Multi-language support
- [ ] Cloud sync
- [ ] Preset recommendations
- [ ] Advanced genetics database

## 🏆 Acknowledgments

- **OrtoIoT Team** - Core development
- **Community Contributors** - Feedback and testing
- **CustomTkinter** - Modern UI framework
- **Python Community** - Excellent ecosystem

---

<p align="center">
  Made with ❤️ by the OrtoIoT Team<br>
  <a href="https://ortoiot.com">OrtoIoT.com</a> | 
  <a href="https://github.com/ortoiot">GitHub</a> | 
  <a href="https://discord.gg/ortoiot">Discord</a>
</p>