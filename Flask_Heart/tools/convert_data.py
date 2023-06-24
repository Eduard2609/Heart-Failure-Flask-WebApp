

def convert_data(data):
    mapping = {
    'sex': {'male': 1, 'female': 0},
    'fasting_bs': {'yes': 1, 'no': 0},
    'exercise_angina': {'yes': 1, 'no': 0},
    'chest_pain_type': {'ASY': [1, 0, 0, 0], 'ATA': [0, 1, 0, 0], 'NAP': [0, 0, 1, 0], 'TA': [0, 0, 0, 1]},
    'resting_ecg': {'LVH': [1, 0, 0], 'normal': [0, 1, 0], 'ST': [0, 0, 1]},
    'st_slope': {'down': [1, 0, 0], 'flat': [0, 1, 0], 'up': [0, 0, 1]}
}  
    converted = [
        int(data['age']),
        mapping['sex'][data['sex']],
        int(data['resting_bp']),
        int(data['cholesterol']),
        mapping['fasting_bs'][data['fasting_bs']],
        int(data['max_hr']),
        mapping['exercise_angina'][data['exercise_angina']],
        float(data['oldpeak']),
        *mapping['chest_pain_type'][data['chest_pain_type']],
        *mapping['resting_ecg'][data['resting_ecg']],
        *mapping['st_slope'][data['st_slope']]
    ]

    return converted

