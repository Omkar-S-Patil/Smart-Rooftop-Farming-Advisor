def generate_watering_advice(soil, temp, humidity, rainfall, crop):
    if rainfall > 150:
        base = "Minimal watering required; sufficient rainfall maintains soil moisture"

    elif soil == "Black":
        if temp > 32 or humidity < 40:
            base = "Water moderately every 2-3 days"
        else:
            base = "Water lightly 2-3 times per week"

    elif soil == "Loamy":
        if temp > 32 or humidity < 40:
            base = "Water frequently (every 1-2 days)"
        else:
            base = "Maintain moderate watering every 2-3 days"

    elif soil == "Red":
        if temp > 30:
            base = "Water daily or on alternate days"
        else:
            base = "Water every 2 days"

    else:
        base = "Maintain regular watering"

    crop = crop.lower()

    crop_tips = {
        "tomato": "maintain consistent moisture for healthy fruit development.",
        "chilli": "avoid overwatering as chilli is sensitive to excess moisture.",
        "spinach": "ensure soil remains moist for proper leaf growth.",
        "coriander": "light and frequent watering improves leaf quality.",
        "fenugreek": "avoid water stagnation to prevent root damage.",
        "mint": "requires consistently moist soil for optimal growth.",
        "tulsi": "allow slight drying between watering to prevent root rot.",
        "brinjal": "maintain even moisture for proper fruit development.",
        "bottle gourd": "ensure regular watering for better vine growth.",
        "lemongrass": "requires moderate moisture but avoid excessive watering."
    }

    extra = crop_tips.get(crop, "")

    return base + "; " + extra