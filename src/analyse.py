from pii_codex.services.analysis_service import PIIAnalysisService
import pandas as pd

def analyse(texts):
        pii_analysis_service = PIIAnalysisService()
        # # Set of example texts from README or Notebook in PII Codex module
        # texts=[
        #         "How can I reach you, Jim?",
        #         "As a democrat, I promise to uphold....",
        #         "As a Catholic, I can tell you that....",
        #         "Here is my contact information: Phone number 555-555-5555 and my email is example123@email.com",
        #         "Perfect, my number if you need me is 777-777-7777. Where is the residence and what is the earliest the crew can arrive?",
        #         "I'll be at my home at 123 Dark Data Lane, OH, 11111 after 7PM",
        #         "Cool, I'll be there!"
        #         ]

        analysis_results = pii_analysis_service.analyze_collection(texts=texts, collection_type="sample", collection_name="Test Collection")

        print("Collection Risk Score: ", analysis_results.risk_score_mean)

        # print(analysis_results.to_dict())

        return analysis_results