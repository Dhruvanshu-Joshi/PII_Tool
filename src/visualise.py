import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import time  # Import time module for delay
# from pii_codex.services.analysis_service import PIIAnalysisService

# # Data extracted from the output
# pii_analysis_service = PIIAnalysisService()

# texts = [
#     "How can I reach you, Jim?",
#     "As a democrat, I promise to uphold....",
#     "As a Catholic, I can tell you that....",
#     "Here is my contact information: Phone number 555-555-5555 and my email is example123@email.com",
#     "Perfect, my number if you need me is 777-777-7777. Where is the residence and what is the earliest the crew can arrive?",
#     "I'll be at my home at 123 Dark Data Lane, OH, 11111 after 7PM",
#     "Cool, I'll be there!"
# ]

# analysis_results = pii_analysis_service.analyze_collection(texts=texts, collection_type="sample", collection_name="Test Collection")

def visualise(texts, analysis_results):
    # Print Collection Risk Score
    print(f"Collection Risk Score: {analysis_results.risk_score_mean:.2f}")

    # Print Detailed Analysis Results
    print("\nDetailed Analysis Results:")
    for result in analysis_results.to_dict()['analyses']:
        print(f"\nOriginal Text: {texts[result['index']]}")
        print(f"Sanitized Text: {result['sanitized_text']}")
        print(f"Risk Score Mean: {result['risk_score_mean']:.2f}")
        print("Detected PII:")
        for pii in result['analysis']:
            pii_type = pii.get('pii_type_detected', None)
            if pii_type:  # Print only if pii_type is not None
                risk_level = pii.get('risk_level', 'Unknown')
                risk_level_definition = pii.get('risk_level_definition', 'Unknown')
                score = pii.get('score', 'N/A')
                start_index = pii.get('start', 'N/A')
                end_index = pii.get('end', 'N/A')
                
                print(f"  - PII Type Detected: {pii_type}")
                print(f"    Risk Level: {risk_level} ({risk_level_definition})")
                print(f"    Score: {score if score != 'N/A' else 'N/A'}")
                print(f"    Start Index: {start_index}")
                print(f"    End Index: {end_index}")

    # Print Detected PII Types and Frequencies
    pii_types = analysis_results.to_dict()['detected_pii_types']
    pii_frequencies = analysis_results.to_dict()['detected_pii_type_frequencies']

    print("\nDetected PII Types and Frequencies:")
    for pii_type, frequency in pii_frequencies.items():
        print(f"  - {pii_type}: {frequency} occurrence(s)")

    analysis_dict = analysis_results.to_dict()

    # print(analysis_dict)

    # Extract risk scores
    risk_scores = analysis_dict['risk_scores']

    # Extract detected PII types
    pii_types = list(analysis_dict['detected_pii_types'])

    # Extract PII frequencies
    pii_frequencies = [analysis_dict['detected_pii_type_frequencies'][pii_type] for pii_type in pii_types]

    # Check the length of each array
    print("Length of risk_scores:", len(risk_scores))
    print("Length of pii_types:", len(pii_types))
    print("Length of pii_frequencies:", len(pii_frequencies))
    print("Length of texts:", len(texts))  # Assuming 'texts' refers to the original text data

    max_length = max(len(texts), len(risk_scores), len(pii_types), len(pii_frequencies))

    # Pad lists with None or appropriate values to make them of the same length
    risk_scores += [None] * (max_length - len(risk_scores))
    pii_types += [None] * (max_length - len(pii_types))
    pii_frequencies += [None] * (max_length - len(pii_frequencies))

    # Create a DataFrame for easier manipulation
    df = pd.DataFrame({
        'Text': texts,
        'Risk Score': risk_scores,
        # 'PII Type': ['PERSON', 'NRP', 'NRP', 'PHONE_NUMBER', 'PHONE_NUMBER', 'LOCATION', None]
        'PII Type': pii_types
    })

    # Visualization 1: Heatmap for Risk Scores
    plt.figure(figsize=(10, 6))
    risk_matrix = np.array(risk_scores).reshape(1, -1)
    sns.heatmap(risk_matrix, annot=True, cmap="coolwarm", cbar=False, fmt=".2f")
    plt.title('Risk Score Heatmap')
    plt.xticks(np.arange(len(risk_scores)), [f'Text {i+1}' for i in range(len(risk_scores))], rotation=45, ha='right')
    plt.yticks([])
    plt.show()

    # Visualization 2: Scatter Plot of PII Type vs Risk Score
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='PII Type', y='Risk Score', hue='Risk Score', palette="coolwarm", s=100)
    plt.title('PII Type vs Risk Score')
    plt.xticks(rotation=45)
    plt.show()

    # Visualization 3: Count Plot for PII Frequencies
    plt.figure(figsize=(10, 6))
    sns.barplot(x=pii_types, y=pii_frequencies, palette="coolwarm")
    plt.title('Count of PII Types Detected')
    plt.ylabel('Count')
    plt.xlabel('PII Type')
    plt.xticks(rotation=45)
    plt.show()

    # Visualization 4: Box Plot for Risk Scores
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='Risk Score', palette="coolwarm")
    plt.title('Risk Score Distribution')
    plt.xlabel('Risk Score')
    plt.show()

    # Visualization 5: Radar Chart for Risk Scores
    angles = np.linspace(0, 2 * np.pi, len(risk_scores), endpoint=False).tolist()
    risk_scores_radar = np.concatenate((risk_scores, [risk_scores[0]]))  # Repeat the first value to close the circle
    angles_radar = np.concatenate((angles, [angles[0]]))

    # Create a polar projection for the radar chart
    plt.figure(figsize=(10, 6))
    ax_radar = plt.subplot(projection='polar')
    ax_radar.plot(angles_radar, risk_scores_radar, color='red', linewidth=2)
    ax_radar.fill(angles_radar, risk_scores_radar, color='red', alpha=0.25)
    plt.title('Radar Chart for Risk Scores')
    plt.yticks([])  # Optional: Remove radial labels

    # manager = plt.get_current_fig_manager()
    # manager.full_screen_toggle()
    plt.show()

    # Remove None values and corresponding frequencies
    filtered_pii_types = [pii_type for pii_type in pii_types if pii_type is not None]
    filtered_pii_frequencies = [freq for pii_type, freq in zip(pii_types, pii_frequencies) if pii_type is not None]

    # Ensure that the lengths match
    assert len(filtered_pii_types) == len(filtered_pii_frequencies), "Lengths of filtered types and frequencies must match."

    # Visualization 6: Pie Chart for PII Frequencies
    plt.figure(figsize=(10, 6))
    plt.pie(filtered_pii_frequencies, labels=filtered_pii_types, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("coolwarm", len(filtered_pii_types)))
    plt.title('Detected PII Types')
    plt.show()
