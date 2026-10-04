"""
NyayaSetu — Verified Legal Knowledge Base Seed Data
====================================================
Contains verified, official Indian statutory and procedural information
for Problem-to-Action Guidance in Phase 2.

All records are grounded in verified government acts, portals, and helplines:
- The Consumer Protection Act, 2019
- Transfer of Property Act, 1882 / Real Estate (Regulation and Development) Act, 2016
- Family Courts Act, 1984 / Section 125 CrPC / Section 144 BNSS
- Code on Wages, 2019 / Industrial Disputes Act, 1947
- Right to Information Act, 2005
- Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) / IT Act, 2000
- Protection of Women from Domestic Violence Act, 2005 (PWDVA)
- Legal Services Authorities Act, 1987 (NALSA)
"""

import json
from app import db
from app.models import LegalCategory, LegalGuidance, Helpline


CATEGORIES_DATA = [
    {
        "slug": "consumer",
        "name_en": "Consumer Rights & Service Deficiency",
        "name_hi": "उपभोक्ता अधिकार और सेवा में कमी",
        "description_en": "Defective products, refusal of refund, deceptive warranties, unfair trade practices, and e-commerce disputes.",
        "description_hi": "दोषपूर्ण उत्पाद, रिफंड से इनकार, भ्रामक वारंटी, अनुचित व्यापार व्यवहार और ई-कॉमर्स विवाद।",
        "icon": "🛍️",
        "guidance": [
            {
                "title_en": "Step-by-Step Action Guide for Consumer Complaints",
                "title_hi": "उपभोक्ता शिकायतों के लिए चरणबद्ध कार्रवाई मार्गदर्शिका",
                "body_en": "Under the Consumer Protection Act 2019, consumers have the right to seek replacement, refund, or damages for defective products or deficient services. The law establishes District, State, and National Consumer Dispute Redressal Commissions with simplified procedures.",
                "body_hi": "उपभोक्ता संरक्षण अधिनियम 2019 के तहत, उपभोक्ताओं को दोषपूर्ण उत्पादों या सेवाओं में कमी के लिए प्रतिस्थापन, रिफंड या मुआवजे की मांग करने का अधिकार है। कानून सरल प्रक्रियाओं के साथ जिला, राज्य और राष्ट्रीय उपभोक्ता विवाद निवारण आयोग स्थापित करता है।",
                "action_steps_en": json.dumps([
                    "Preserve all transaction records: receipts, tax invoices, order IDs, warranty cards, photos/videos of defects, and written correspondence.",
                    "Send a formal written notice or email to the vendor's grievance officer giving 15 to 30 days to resolve the issue.",
                    "Register a grievance on the National Consumer Helpline (Call 1915, SMS 8800001915, or visit consumerhelpline.gov.in).",
                    "If unresolved, file a formal complaint online via the official e-Daakhil portal (edaakhil.nic.in) or visit your District Consumer Disputes Redressal Commission."
                ]),
                "action_steps_hi": json.dumps([
                    "सभी लेनदेन रिकॉर्ड सुरक्षित रखें: रसीदें, टैक्स इनवॉइस, ऑर्डर आईडी, वारंटी कार्ड, दोष के फोटो/वीडियो और लिखित पत्राचार।",
                    "विक्रेता के शिकायत निवारण अधिकारी को समस्या समाधान हेतु 15 से 30 दिनों का समय देते हुए औपचारिक लिखित नोटिस या ईमेल भेजें।",
                    "राष्ट्रीय उपभोक्ता हेल्पलाइन पर शिकायत दर्ज करें (1915 पर कॉल करें, 8800001915 पर एसएमएस करें, या consumerhelpline.gov.in पर जाएं)।",
                    "यदि समाधान न हो, तो आधिकारिक ई-दाखिल पोर्टल (edaakhil.nic.in) के माध्यम से ऑनलाइन शिकायत दर्ज करें या जिला उपभोक्ता आयोग में जाएं।"
                ]),
                "source_name": "Consumer Protection Act, 2019 & Ministry of Consumer Affairs, Government of India",
                "source_url": "https://consumerhelpline.gov.in",
                "verified": True,
                "order_index": 1,
            }
        ]
    },
    {
        "slug": "property",
        "name_en": "Property, Tenancy & Land Disputes",
        "name_hi": "संपत्ति, किरायेदारी और भूमि विवाद",
        "description_en": "Tenant-landlord disputes, illegal eviction, security deposit disputes, land encroachment, and builder delays.",
        "description_hi": "मकान मालिक-किरायेदार विवाद, अवैध बेदखली, सुरक्षा जमा विवाद, भूमि अतिक्रमण और बिल्डर द्वारा देरी।",
        "icon": "🏠",
        "guidance": [
            {
                "title_en": "Action Procedure for Tenancy and Property Issues",
                "title_hi": "किरायेदारी और संपत्ति विवादों के लिए कार्रवाई प्रक्रिया",
                "body_en": "Tenancy disputes are governed by State Rent Control Acts, Model Tenancy Act principles, and the Transfer of Property Act, 1882. Real estate purchase disputes fall under the Real Estate (Regulation and Development) Act, 2016 (RERA). Arbitrary eviction without due legal notice is unlawful.",
                "body_hi": "किरायेदारी विवाद राज्य किराया नियंत्रण अधिनियमों, मॉडल किरायेदारी अधिनियम और संपत्ति हस्तांतरण अधिनियम 1882 द्वारा शासित होते हैं। रियल एस्टेट खरीद विवाद रेरा (RERA) 2016 के अंतर्गत आते हैं। उचित कानूनी प्रक्रिया के बिना मनमानी बेदखली गैरकानूनी है।",
                "action_steps_en": json.dumps([
                    "Review your written rent agreement or lease deed, payment receipts, and bank transfer statements.",
                    "Communicate formally in writing; do not rely solely on verbal statements. Document rent payment records.",
                    "For builder delays or project deviations, file a complaint directly with your State RERA Authority portal.",
                    "For unlawful eviction threats, approach your District Legal Services Authority (DLSA) for pre-litigation mediation before civil litigation."
                ]),
                "action_steps_hi": json.dumps([
                    "अपने लिखित किराया समझौते या लीज डीड, भुगतान रसीद और बैंक ट्रांसफर विवरण की समीक्षा करें।",
                    "केवल मौखिक बातचीत पर निर्भर न रहें; सभी संवाद औपचारिक रूप से लिखित में रखें।",
                    "बिल्डर द्वारा देरी या समझौते के उल्लंघन के मामले में अपने राज्य के रेरा (RERA) पोर्टल पर शिकायत दर्ज करें।",
                    "अवैध बेदखली की स्थिति में सिविल मुकदमे से पहले जिला विधिक सेवा प्राधिकरण (DLSA) से मध्यस्थता हेतु संपर्क करें।"
                ]),
                "source_name": "Transfer of Property Act, 1882 & Real Estate (Regulation and Development) Act, 2016 (RERA)",
                "source_url": "https://mohua.gov.in",
                "verified": True,
                "order_index": 1,
            }
        ]
    },
    {
        "slug": "family",
        "name_en": "Family, Maintenance & Matrimonial Issues",
        "name_hi": "पारिवारिक मामले, भरण-पोषण और वैवाहिक विवाद",
        "description_en": "Matrimonial disputes, maintenance claims, child custody, guardianship, and senior citizen maintenance.",
        "description_hi": "वैवाहिक विवाद, भरण-पोषण (गुजारा भत्ता), बच्चों की कस्टडी, और वरिष्ठ नागरिक भरण-पोषण।",
        "icon": "👨‍👩‍👦",
        "guidance": [
            {
                "title_en": "Legal Guidance for Family Disputes & Maintenance",
                "title_hi": "पारिवारिक विवादों और भरण-पोषण के लिए कानूनी मार्गदर्शन",
                "body_en": "Family matters are handled by Family Courts with primary emphasis on reconciliation and conciliation. Spousal and child maintenance can be claimed under Section 125 CrPC (Section 144 BNSS) or personal laws. Senior citizens can seek maintenance under the Senior Citizens Maintenance Act, 2007.",
                "body_hi": "पारिवारिक मामलों की सुनवाई फैमिली कोर्ट (पारिवारिक न्यायालय) द्वारा मुख्य रूप से सुलह और समझौते पर ध्यान केंद्रित करते हुए की जाती है। धारा 125 सीआरपीसी (धारा 144 बीएनएसएस) या पर्सनल लॉ के तहत भरण-पोषण का दावा किया जा सकता है।",
                "action_steps_en": json.dumps([
                    "Gather identification, marriage certificate/proof, birth certificates of children, and income documentation.",
                    "Approach the Family Court Counsellor or District Legal Services Authority (DLSA) for confidential mediation.",
                    "For urgent living expenses, file an application for interim maintenance under Section 144 BNSS / Section 125 CrPC.",
                    "Senior citizens facing abandonment can apply directly to the Sub-Divisional Magistrate (SDM) Maintenance Tribunal."
                ]),
                "action_steps_hi": json.dumps([
                    "पहचान पत्र, विवाह प्रमाण, बच्चों के जन्म प्रमाण पत्र और आय संबंधी दस्तावेज एकत्र करें।",
                    "गोपनीय सुलह व मध्यस्थता के लिए पारिवारिक न्यायालय परामर्शदाता या जिला विधिक सेवा प्राधिकरण (DLSA) से संपर्क करें।",
                    "तत्काल गुजारा भत्ते हेतु धारा 144 बीएनएसएस / धारा 125 सीआरपीसी के तहत अंतरिम भरण-पोषण का आवेदन करें।",
                    "उपेक्षित वरिष्ठ नागरिक सीधे एसडीएम (SDM) भरण-पोषण अधिकरण में आवेदन कर सकते हैं।"
                ]),
                "source_name": "Family Courts Act, 1984 & Maintenance and Welfare of Parents and Senior Citizens Act, 2007",
                "source_url": "https://nalsa.gov.in",
                "verified": True,
                "order_index": 1,
            }
        ]
    },
    {
        "slug": "labour",
        "name_en": "Employment, Wages & Workplace Rights",
        "name_hi": "रोजगार, वेतन और कार्यस्थल अधिकार",
        "description_en": "Withheld salary, wrongful termination, illegal deductions, maternity benefits, and provident fund (EPF) issues.",
        "description_hi": "रुका हुआ वेतन, अनुचित बर्खास्तगी, अवैध कटौती, मातृत्व लाभ और भविष्य निधि (EPF) विवाद।",
        "icon": "💼",
        "guidance": [
            {
                "title_en": "Action Steps for Wage and Employment Grievances",
                "title_hi": "वेतन और रोजगार शिकायतों के लिए कदम",
                "body_en": "Employees and workers are protected against arbitrary wage withholding under the Payment of Wages Act / Code on Wages, 2019. The Industrial Disputes Act, 1947 provides protection against unlawful termination without retrenchment compensation or statutory notice.",
                "body_hi": "वेतन भुगतान अधिनियम और वेतन संहिता 2019 के तहत कर्मचारियों को वेतन रोके जाने से सुरक्षा प्राप्त है। औद्योगिक विवाद अधिनियम 1947 बिना वैधानिक नोटिस या मुआवजे के अनुचित निष्कासन के खिलाफ सुरक्षा प्रदान करता है।",
                "action_steps_en": json.dumps([
                    "Secure employment contracts, appointment letters, monthly salary slips, bank statements, and attendance records.",
                    "Submit a formal demand letter via registered post/email to the employer management detailing unpaid amounts.",
                    "Lodge a grievance on the Ministry of Labour's official portal (SAMADHAN portal: samadhan.labour.gov.in) or EPFiGMS for PF issues.",
                    "Approach the local Labour Commissioner or Labour Conciliation Officer having jurisdiction over the workplace."
                ]),
                "action_steps_hi": json.dumps([
                    "नियुक्ति पत्र, मासिक वेतन पर्ची, बैंक स्टेटमेंट और उपस्थिति रिकॉर्ड सुरक्षित रखें।",
                    "बकाया राशि का विवरण देते हुए नियोक्ता को ईमेल/पंजीकृत डाक से औपचारिक मांग पत्र भेजें।",
                    "श्रम मंत्रालय के समाधान पोर्टल (samadhan.labour.gov.in) पर या पीएफ हेतु EPFiGMS पर शिकायत दर्ज करें।",
                    "कार्यस्थल क्षेत्र के स्थानीय श्रम आयुक्त या श्रम सुलह अधिकारी से संपर्क करें।"
                ]),
                "source_name": "Code on Wages, 2019 & Industrial Disputes Act, 1947, Ministry of Labour and Employment",
                "source_url": "https://samadhan.labour.gov.in",
                "verified": True,
                "order_index": 1,
            }
        ]
    },
    {
        "slug": "rti",
        "name_en": "Right to Information (RTI)",
        "name_hi": "सूचना का अधिकार (RTI)",
        "description_en": "Seeking information from public authorities, non-responsive PIO, delayed records, and RTI appeals.",
        "description_hi": "सरकारी विभागों से सूचना प्राप्त करना, जन सूचना अधिकारी से उत्तर न मिलना, और आरटीआई अपील।",
        "icon": "📋",
        "guidance": [
            {
                "title_en": "How to File and Follow Up an RTI Application",
                "title_hi": "RTI आवेदन कैसे दाखिल करें और फॉलो-अप लें",
                "body_en": "Under the Right to Information Act, 2005, every Indian citizen can request records, inspection of works, and documents from government offices and public authorities. The Public Information Officer (PIO) is mandated to provide information within 30 days (48 hours for life and liberty matters).",
                "body_hi": "सूचना का अधिकार अधिनियम 2005 के तहत प्रत्येक भारतीय नागरिक सरकारी कार्यालयों से रिकॉर्ड, दस्तावेजों और कार्य के निरीक्षण की मांग कर सकता है। जन सूचना अधिकारी (PIO) को 30 दिनों के भीतर सूचना प्रदान करना अनिवार्य है।",
                "action_steps_en": json.dumps([
                    "Clearly specify the exact documents or records requested; avoid vague questions or requests for opinions.",
                    "For central government bodies, apply online at rtionline.gov.in with a nominal fee of ₹10 (BPL applicants exempt).",
                    "For state government bodies, submit application to the designated Public Information Officer (PIO) via speed post or state RTI portal.",
                    "If no response within 30 days or if rejected, file a First Appeal to the designated First Appellate Authority within 30 days."
                ]),
                "action_steps_hi": json.dumps([
                    "मांगे गए दस्तावेजों का स्पष्ट और विशिष्ट विवरण लिखें; अस्पष्ट प्रश्नों या सलाह मांगने से बचें।",
                    "केंद्र सरकार के विभागों के लिए rtionline.gov.in पर ₹10 के शुल्क के साथ ऑनलाइन आवेदन करें (BPL आवेदक शुल्क मुक्त)।",
                    "राज्य विभागों हेतु निर्धारित जन सूचना अधिकारी (PIO) को स्पीड पोस्ट या राज्य पोर्टल से आवेदन भेजें।",
                    "30 दिनों में उत्तर न मिलने पर अगले 30 दिनों के भीतर प्रथम अपीलीय प्राधिकारी के समक्ष प्रथम अपील दाखिल करें।"
                ]),
                "source_name": "Right to Information Act, 2005 & Department of Personnel and Training (DoPT)",
                "source_url": "https://rtionline.gov.in",
                "verified": True,
                "order_index": 1,
            }
        ]
    },
    {
        "slug": "criminal",
        "name_en": "Criminal Incidents, Fraud & Police Procedure",
        "name_hi": "आपराधिक घटनाएं, धोखाधड़ी और पुलिस प्रक्रिया",
        "description_en": "Cyber financial fraud, theft, assault, harassment, filing an FIR, and police refusal to register complaint.",
        "description_hi": "साइबर वित्तीय धोखाधड़ी, चोरी, मारपीट, उत्पीड़न, एफआईआर (FIR) दर्ज करना और पुलिस द्वारा शिकायत न लेना।",
        "icon": "⚖️",
        "guidance": [
            {
                "title_en": "Citizen Guidance for Complaints, FIR & Cyber Crime",
                "title_hi": "शिकायत, एफआईआर और साइबर अपराध हेतु नागरिक मार्गदर्शिका",
                "body_en": "Under the Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) / CrPC, police are legally required to register an FIR for cognizable offences. For financial cyber fraud, timely reporting within the 'golden hour' enables financial freezing of illicit transactions.",
                "body_hi": "भारतीय नागरिक सुरक्षा संहिता (BNSS) के तहत संज्ञेय अपराधों के लिए एफआईआर दर्ज करना पुलिस का कानूनी दायित्व है। वित्तीय साइबर धोखाधड़ी में प्रारंभिक घंटों में शिकायत दर्ज कराने से बैंक लेनदेन रोका जा सकता है।",
                "action_steps_en": json.dumps([
                    "For immediate personal safety or emergency assistance, dial 112 immediately.",
                    "For online financial fraud, call 1930 immediately or lodge complaint at cybercrime.gov.in with transaction details.",
                    "Visit the local Police Station to submit a signed written complaint. Always obtain an official dated acknowledgement stamp.",
                    "If police refuse to register an FIR for a cognizable offence, send the complaint by registered post to the Superintendent of Police (SP) or file a private complaint before the Magistrate under BNSS."
                ]),
                "action_steps_hi": json.dumps([
                    "तत्काल सुरक्षा या आपातकालीन स्थिति के लिए तुरंत 112 डायल करें।",
                    "ऑनलाइन वित्तीय धोखाधड़ी होने पर तुरंत 1930 पर कॉल करें या लेन-देन विवरण के साथ cybercrime.gov.in पर रिपोर्ट करें।",
                    "स्थानीय पुलिस थाने में हस्ताक्षरित लिखित शिकायत दें। थाने से मुहर लगी पावती (रिसीविंग) अवश्य प्राप्त करें।",
                    "यदि पुलिस एफआईआर दर्ज करने से मना करे, तो पुलिस अधीक्षक (SP) को पंजीकृत डाक से शिकायत भेजें या मजिस्ट्रेट के समक्ष आवेदन करें।"
                ]),
                "source_name": "Bharatiya Nagarik Suraksha Sanhita, 2023 & Ministry of Home Affairs, Government of India",
                "source_url": "https://cybercrime.gov.in",
                "verified": True,
                "order_index": 1,
            }
        ]
    },
    {
        "slug": "domestic_violence",
        "name_en": "Domestic Violence & Women Safety",
        "name_hi": "घरेलू हिंसा और महिला सुरक्षा",
        "description_en": "Physical, emotional, verbal or economic abuse in domestic relationships, dowry harassment, and urgent protection.",
        "description_hi": "घरेलू संबंधों में शारीरिक, मानसिक, भावनात्मक या आर्थिक हिंसा, दहेज उत्पीड़न और तत्काल सुरक्षा।",
        "icon": "🛡️",
        "guidance": [
            {
                "title_en": "Immediate Protection and Rights under PWDVA 2005",
                "title_hi": "घरेलू हिंसा अधिनियम 2005 के तहत तत्काल सुरक्षा और अधिकार",
                "body_en": "The Protection of Women from Domestic Violence Act, 2005 (PWDVA) grants women the legal right to protection orders, shared residence in the matrimonial home, emergency monetary relief, and custody orders through Magistrate courts and designated Protection Officers.",
                "body_hi": "घरेलू हिंसा से महिलाओं का संरक्षण अधिनियम 2005 महिलाओं को मजिस्ट्रेट कोर्ट और संरक्षण अधिकारियों के माध्यम से सुरक्षा आदेश, साझा घर में रहने का अधिकार, अंतरिम मौद्रिक राहत और बच्चों की कस्टडी का अधिकार देता है।",
                "action_steps_en": json.dumps([
                    "Ensure immediate physical safety: dial 112 (Emergency) or 181 / 1091 (Women Helpline).",
                    "Reach out to the District Protection Officer (PO) or nearest One Stop Centre (Sakhi Centre) for shelter, medical aid, and legal assistance.",
                    "File a Domestic Incident Report (DIR) with the Protection Officer or approach the Judicial Magistrate directly under Section 12 of PWDVA.",
                    "Avail free legal representation through the District Legal Services Authority (DLSA) under Section 12 of the Legal Services Authorities Act."
                ]),
                "action_steps_hi": json.dumps([
                    "तत्काल सुरक्षा सुनिश्चित करें: 112 (आपातकाल) या 181 / 1091 (महिला हेल्पलाइन) पर कॉल करें।",
                    "आश्रय, चिकित्सा सहायता और कानूनी सलाह के लिए जिला संरक्षण अधिकारी या निकटतम वन स्टॉप सेंटर (सखी केंद्र) से संपर्क करें।",
                    "संरक्षण अधिकारी के साथ घरेलू घटना रिपोर्ट (DIR) दर्ज करें या सीधे मजिस्ट्रेट के समक्ष धारा 12 के तहत आवेदन प्रस्तुत करें।",
                    "विधिक सेवा प्राधिकरण अधिनियम के तहत जिला विधिक सेवा प्राधिकरण (DLSA) से निःशुल्क वकील प्राप्त करें।"
                ]),
                "source_name": "Protection of Women from Domestic Violence Act, 2005 & Ministry of Women and Child Development",
                "source_url": "https://wcd.nic.in",
                "verified": True,
                "order_index": 1,
            }
        ]
    },
    {
        "slug": "other",
        "name_en": "General Legal Aid & Civic Grievance",
        "name_hi": "सामान्य विधिक सहायता और नागरिक शिकायत",
        "description_en": "General civil rights, matters not covered in specific categories, and free legal assistance for underprivileged citizens.",
        "description_hi": "सामान्य नागरिक अधिकार, अनिर्दिष्ट मामले, और वंचित नागरिकों के लिए निःशुल्क कानूनी सहायता।",
        "icon": "⚖️",
        "guidance": [
            {
                "title_en": "Accessing Free Legal Services under NALSA",
                "title_hi": "नालसा (NALSA) के तहत निःशुल्क कानूनी सहायता प्राप्त करना",
                "body_en": "Under Article 39A of the Constitution of India and the Legal Services Authorities Act, 1987, free and competent legal services are guaranteed to women, children, persons in custody, SC/ST citizens, industrial workmen, and citizens with annual income below statutory thresholds.",
                "body_hi": "भारतीय संविधान के अनुच्छेद 39A और विधिक सेवा प्राधिकरण अधिनियम 1987 के तहत महिलाओं, बच्चों, हिरासत में लिए गए व्यक्तियों, एससी/एसटी नागरिकों और कम आय वाले व्यक्तियों को निःशुल्क कानूनी सहायता की गारंटी दी गई है।",
                "action_steps_en": json.dumps([
                    "Call the National Legal Services Authority (NALSA) toll-free helpline at 15100.",
                    "Visit the Front Office of your District Legal Services Authority (DLSA) located inside the District Court complex.",
                    "Submit an application on plain paper stating your problem along with identity and income proof (if applicable).",
                    "A panel legal aid advocate will be assigned to represent your case free of charge."
                ]),
                "action_steps_hi": json.dumps([
                    "राष्ट्रीय विधिक सेवा प्राधिकरण (NALSA) की टोल-फ्री हेल्पलाइन 15100 पर संपर्क करें।",
                    "जिला न्यायालय परिसर में स्थित जिला विधिक सेवा प्राधिकरण (DLSA) के फ्रंट ऑफिस में जाएं।",
                    "पहचान और आय प्रमाण (यदि लागू हो) के साथ सादे कागज पर समस्या लिखते हुए आवेदन दें।",
                    "आपके मामले की पैरवी के लिए निःशुल्क पैनल अधिवक्ता नियुक्त किया जाएगा।"
                ]),
                "source_name": "Legal Services Authorities Act, 1987 & National Legal Services Authority (NALSA)",
                "source_url": "https://nalsa.gov.in",
                "verified": True,
                "order_index": 1,
            }
        ]
    }
]

HELPLINES_DATA = [
    {
        "name_en": "National Emergency Helpline",
        "name_hi": "राष्ट्रीय आपातकालीन हेल्पलाइन",
        "number": "112",
        "scope_en": "Single emergency number for police, fire, and ambulance across India.",
        "scope_hi": "पूरे भारत में पुलिस, दमकल और एम्बुलेंस के लिए एकल आपातकालीन नंबर।",
        "relevant_categories": "criminal,domestic_violence,other",
        "source_url": "https://112.gov.in"
    },
    {
        "name_en": "National Legal Aid Toll-Free (NALSA)",
        "name_hi": "राष्ट्रीय कानूनी सहायता टोल-फ्री (NALSA)",
        "number": "15100",
        "scope_en": "Pan-India free legal advice and representation assistance for eligible citizens.",
        "scope_hi": "पात्र नागरिकों के लिए अखिल भारतीय निःशुल्क कानूनी सलाह और प्रतिनिधित्व सहायता।",
        "relevant_categories": "",
        "source_url": "https://nalsa.gov.in"
    },
    {
        "name_en": "National Consumer Helpline (NCH)",
        "name_hi": "राष्ट्रीय उपभोक्ता हेल्पलाइन",
        "number": "1915",
        "scope_en": "Dedicated national grievance redressal for consumer fraud, defective goods, and service issues.",
        "scope_hi": "उपभोक्ता धोखाधड़ी, खराब उत्पादों और सेवा समस्याओं के लिए समर्पित राष्ट्रीय शिकायत निवारण।",
        "relevant_categories": "consumer",
        "source_url": "https://consumerhelpline.gov.in"
    },
    {
        "name_en": "Cyber Crime Financial Fraud Helpline",
        "name_hi": "साइबर अपराध वित्तीय धोखाधड़ी हेल्पलाइन",
        "number": "1930",
        "scope_en": "Immediate reporting for online banking, UPI fraud, and financial cybercrimes.",
        "scope_hi": "ऑनलाइन बैंकिंग, यूपीआई धोखाधड़ी और वित्तीय साइबर अपराधों की तत्काल रिपोर्टिंग।",
        "relevant_categories": "criminal",
        "source_url": "https://cybercrime.gov.in"
    },
    {
        "name_en": "Women in Distress Helpline",
        "name_hi": "महिला संकट हेल्पलाइन",
        "number": "181",
        "scope_en": "24/7 emergency response, counselling, and shelter referral for women facing violence.",
        "scope_hi": "हिंसा का सामना कर रही महिलाओं के लिए 24/7 आपातकालीन प्रतिक्रिया, परामर्श और आश्रय।",
        "relevant_categories": "domestic_violence,family",
        "source_url": "https://wcd.nic.in"
    },
    {
        "name_en": "National Commission for Women Helpline",
        "name_hi": "राष्ट्रीय महिला आयोग हेल्पलाइन",
        "number": "7827170170",
        "scope_en": "Assistance for domestic violence, dowry harassment, and gender discrimination.",
        "scope_hi": "घरेलू हिंसा, दहेज उत्पीड़न और लैंगिक भेदभाव के मामलों में सहायता।",
        "relevant_categories": "domestic_violence,family",
        "source_url": "https://ncw.nic.in"
    },
    {
        "name_en": "National Labour Helpline / Shram Suvidha",
        "name_hi": "राष्ट्रीय श्रम हेल्पलाइन",
        "number": "1800-180-1111",
        "scope_en": "Information and grievances regarding wages, labour laws, and EPF/ESIC.",
        "scope_hi": "वेतन, श्रम कानून और ईपीएफ/ईएसआईसी के संबंध में जानकारी और शिकायतें।",
        "relevant_categories": "labour",
        "source_url": "https://shramsuvidha.gov.in"
    },
    {
        "name_en": "Senior Citizens National Helpline",
        "name_hi": "वरिष्ठ नागरिक राष्ट्रीय हेल्पलाइन",
        "number": "14567",
        "scope_en": "Elderline: legal guidance, rescue, and maintenance aid for senior citizens.",
        "scope_hi": "एल्डरलाइन: वरिष्ठ नागरिकों के लिए कानूनी मार्गदर्शन, बचाव और भरण-पोषण सहायता।",
        "relevant_categories": "family,other",
        "source_url": "https://elderline.dosje.gov.in"
    }
]


def seed_knowledge_base():
    """
    Seed initial verified legal categories, guidance records, and helplines.
    Idempotent: updates existing records or inserts new ones.
    """
    for cat_data in CATEGORIES_DATA:
        cat = LegalCategory.query.filter_by(slug=cat_data["slug"]).first()
        if not cat:
            cat = LegalCategory(
                slug=cat_data["slug"],
                name_en=cat_data["name_en"],
                name_hi=cat_data["name_hi"],
                description_en=cat_data["description_en"],
                description_hi=cat_data["description_hi"],
                icon=cat_data["icon"]
            )
            db.session.add(cat)
            db.session.flush()
        else:
            cat.name_en = cat_data["name_en"]
            cat.name_hi = cat_data["name_hi"]
            cat.description_en = cat_data["description_en"]
            cat.description_hi = cat_data["description_hi"]
            cat.icon = cat_data["icon"]

        # Guidance items
        for g_data in cat_data.get("guidance", []):
            existing_g = LegalGuidance.query.filter_by(
                category_id=cat.id,
                title_en=g_data["title_en"]
            ).first()
            if not existing_g:
                new_g = LegalGuidance(
                    category_id=cat.id,
                    title_en=g_data["title_en"],
                    title_hi=g_data["title_hi"],
                    body_en=g_data["body_en"],
                    body_hi=g_data["body_hi"],
                    action_steps_en=g_data["action_steps_en"],
                    action_steps_hi=g_data["action_steps_hi"],
                    source_name=g_data["source_name"],
                    source_url=g_data["source_url"],
                    verified=g_data.get("verified", True),
                    order_index=g_data.get("order_index", 1)
                )
                db.session.add(new_g)

    # Helplines
    for h_data in HELPLINES_DATA:
        existing_h = Helpline.query.filter_by(number=h_data["number"]).first()
        if not existing_h:
            new_h = Helpline(
                name_en=h_data["name_en"],
                name_hi=h_data["name_hi"],
                number=h_data["number"],
                scope_en=h_data["scope_en"],
                scope_hi=h_data["scope_hi"],
                relevant_categories=h_data["relevant_categories"],
                source_url=h_data["source_url"]
            )
            db.session.add(new_h)
        else:
            existing_h.name_en = h_data["name_en"]
            existing_h.name_hi = h_data["name_hi"]
            existing_h.scope_en = h_data["scope_en"]
            existing_h.scope_hi = h_data["scope_hi"]
            existing_h.relevant_categories = h_data["relevant_categories"]
            existing_h.source_url = h_data["source_url"]

    db.session.commit()
