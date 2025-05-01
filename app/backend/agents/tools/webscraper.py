from semantic_kernel.functions import kernel_function
import json

# Kernel Functions Plugin
class Web_Tools:
    @kernel_function(
        name="neurocheck_search",
        description="Get NeuroCheck information from the FAQ page."
    )
    async def webscraper(self, query: str):
        faqs = [
        {
            "question": "What is the NeuroCheck™ Home Test Kit?",
            "answer": "The NeuroCheck™ Home Test Kit is an at-home finger-prick blood test that measures biomarkers associated with early neurological inflammation and cognitive decline risk. It's designed to help individuals assess their brain health from the comfort of home."
        },
        {
            "question": "Who should use this test?",
            "answer": "NeuroCheck™ is ideal for adults over 45, those with a family history of neurodegenerative conditions, or anyone experiencing early signs of brain fog or memory changes who wants proactive insight into their neurological health."
        },
        {
            "question": "Is this a diagnostic test?",
            "answer": "No, NeuroCheck™ is not a diagnostic test. It is a screening tool that measures risk indicators and biomarkers related to neurological inflammation. It is intended to support early awareness and should be followed up with a healthcare provider."
        },
        {
            "question": "What biomarkers does it test for?",
            "answer": "NeuroCheck™ tests for key neurological health indicators such as C-reactive protein (CRP), TNF-alpha, Neurofilament Light Chain (NfL), Brain-Derived Neurotrophic Factor (BDNF), and markers of oxidative stress."
        },
        {
            "question": "How do I collect the sample?",
            "answer": "The kit includes a sterile lancet and a blood collection card. You'll prick your finger, apply a few drops of blood, and mail the sample back using prepaid packaging. The process takes less than 10 minutes."
        },
        {
            "question": "Is it safe?",
            "answer": "Yes, the NeuroCheck™ collection method is safe, minimally invasive, and uses FDA-registered components. Samples are processed in CLIA-certified labs to ensure high accuracy and safety standards."
        },
        {
            "question": "How long does it take to get results?",
            "answer": "Once your sample arrives at our lab, you will receive results within 5 business days via our secure online portal. You'll also receive a personalized report with insights and guidance."
        },
        {
            "question": "Can I share the results with my doctor?",
            "answer": "Absolutely. Your results are downloadable and formatted for easy sharing with your doctor. You can also opt to have your report sent directly to your healthcare provider."
        },
        {
            "question": "Does insurance cover it?",
            "answer": "NeuroCheck™ is not currently covered by insurance, but many customers use their HSA or FSA to pay for the test. We are working on expanding insurance coverage in the future."
        },
        {
            "question": "What happens after I get my results?",
            "answer": "You’ll receive a report that includes your biomarker levels, interpretation of the results, and recommended next steps. You’ll also have the option to schedule a telehealth consultation with one of our partnered neurologists or health coaches."
        }
        ]

        return json.dumps(faqs)