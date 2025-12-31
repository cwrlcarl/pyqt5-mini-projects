from pokemon_type import TYPE_COLORS


def set_type_style(label, type_name):
        color = TYPE_COLORS.get(type_name, '#9d9fa1')
        bg_color = hex_to_rgba(color, 0.15)
        
        label.setStyleSheet(f"""                            
            QLabel {{
                max-height: 20px;
                padding: 1px 8px;
                font-size: 13px;
                border-radius: 10px;
                border: 1px solid {color};
                background-color: {bg_color};
                color: {color};
            }}
        """)


def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'rgba({r}, {g}, {b}, {alpha})'


def convert_weight(hectogram):
    kilogram = hectogram / 10
    pound = kilogram * 2.20462
    return f"{pound:.1f} lbs"


def convert_height(decimeter):
    meter = decimeter / 10
    feet = meter * 3.28084
    inch = (feet - int(feet)) * 12
    return f"{feet:.0f}'{inch:.0f}\""