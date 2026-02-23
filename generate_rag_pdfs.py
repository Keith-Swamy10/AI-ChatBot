#!/usr/bin/env python3
"""Generate 5 RAG knowledge-base PDFs for CohrenzAI chatbot training.
Self-contained script with all helpers included."""

import os
from fpdf import FPDF

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "company_docs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PRIMARY = (50, 118, 234)
DARK = (30, 30, 50)
GRAY = (100, 100, 110)
LIGHT_BG = (245, 247, 252)


class CohrenzPDF(FPDF):
    def __init__(self, title_text=""):
        super().__init__()
        self.doc_title = title_text
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*PRIMARY)
        self.cell(0, 8, "CohrenzAI", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*PRIMARY)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-20)
        self.set_draw_color(*PRIMARY)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"CohrenzAI  |  info@cohrenzai.com  |  Page {self.page_no()}/{{nb}}", align="C")

    def cover_page(self, title, subtitle=""):
        self.add_page()
        self.ln(60)
        self.set_font("Helvetica", "B", 32)
        self.set_text_color(*PRIMARY)
        self.multi_cell(0, 14, title, align="C")
        self.ln(6)
        if subtitle:
            self.set_font("Helvetica", "", 14)
            self.set_text_color(*GRAY)
            self.multi_cell(0, 8, subtitle, align="C")
        self.ln(30)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*DARK)
        self.cell(0, 7, "CohrenzAI", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 7, "Noida, Uttar Pradesh, India", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 7, "info@cohrenzai.com | +91 8273597975", align="C", new_x="LMARGIN", new_y="NEXT")

    def section_title(self, text):
        self.ln(6)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*PRIMARY)
        self.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*PRIMARY)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(4)

    def sub_title(self, text):
        self.ln(3)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*DARK)
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        self.cell(6, 6, "-")
        self.multi_cell(0, 6, text)
        self.ln(1)

    def highlight_box(self, text):
        self.set_fill_color(*LIGHT_BG)
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 7, text, fill=True)
        self.ln(3)


# ============================================================
# PDF 1: Getting Started & Integration Guide
# ============================================================
def create_integration_guide():
    pdf = CohrenzPDF()
    pdf.alias_nb_pages()
    pdf.cover_page("Getting Started &\nIntegration Guide", "Everything You Need to Deploy CohrenzAI on Your Website")

    pdf.add_page()
    pdf.section_title("What is CohrenzAI?")
    pdf.body("CohrenzAI is an AI-powered chatbot platform that you can integrate into your website using just one script tag. Once integrated, the chatbot will automatically engage your website visitors, answer their questions using your business data, capture qualified leads, and provide you with intent-driven analytics about what your visitors actually want.")
    pdf.body("CohrenzAI is not a generic chatbot. Every chatbot is trained specifically on YOUR business data - your documents, FAQs, product catalogs, pricing pages, and any other content you provide. This means your chatbot gives accurate, relevant, on-brand answers to every visitor question.")

    pdf.section_title("Who is CohrenzAI For?")
    pdf.body("CohrenzAI is built for any business that has a website and wants to:")
    pdf.bullet("Convert more website visitors into qualified leads")
    pdf.bullet("Provide 24/7 automated customer support without hiring more staff")
    pdf.bullet("Understand what their website visitors actually need and want")
    pdf.bullet("Automate repetitive inquiries like pricing, availability, and FAQ questions")
    pdf.bullet("Book demos, schedule appointments, and handle follow-ups automatically")
    pdf.bullet("Reduce response time from hours to seconds")
    pdf.body("Our clients include healthcare clinics, e-commerce stores, real estate companies, SaaS businesses, financial services firms, educational institutions, and professional service providers.")

    pdf.section_title("How Does CohrenzAI Work?")
    pdf.sub_title("Step 1: Share Your Business Data")
    pdf.body("You provide us with your business documents - PDFs, FAQs, product catalogs, pricing information, service descriptions, or any other content that your customers typically ask about. You can also point us to your website pages and we will scrape the content automatically.")
    pdf.sub_title("Step 2: We Train Your Custom AI Chatbot")
    pdf.body("Our AI-Ready Knowledge System transforms your documents into a structured, searchable knowledge base using vector embeddings and generative AI models. This process takes 24 to 48 hours. Your chatbot is trained exclusively on YOUR data, so it will never give answers about things outside your business context.")
    pdf.sub_title("Step 3: Add One Script to Your Website")
    pdf.body("Integration is incredibly simple. You add a single script tag to your website HTML. That is it. No server configuration, no backend changes, no complex setup. The script creates a beautiful floating chat button on your website that visitors can click to start a conversation.")
    pdf.sub_title("Step 4: Go Live and Start Capturing Leads")
    pdf.body("Once the script is added, your chatbot is live. It will immediately start engaging visitors, answering questions from your knowledge base, and capturing leads when visitors show buying intent.")

    pdf.add_page()
    pdf.section_title("Integration Requirements")
    pdf.body("CohrenzAI works with any website technology. Here is what you need:")
    pdf.bullet("A website where you can add HTML or JavaScript code (WordPress, Shopify, Wix, Squarespace, custom HTML, React, Next.js, or any other platform)")
    pdf.bullet("The ability to add a script tag to your website pages")
    pdf.bullet("A CohrenzAI account with your API URL and Public Key")
    pdf.body("That is all. No server-side changes. No database setup. No npm packages. No dependencies. Just one script tag.")

    pdf.section_title("Platform Compatibility")
    pdf.body("CohrenzAI works with every major website platform:")
    pdf.bullet("WordPress: Add the script via header/footer plugin or directly in your theme footer.php")
    pdf.bullet("Shopify: Add the script in Online Store, then Themes, then Edit Code, then theme.liquid before closing body tag")
    pdf.bullet("Wix: Use the Wix HTML embed widget or Custom Code section in site settings")
    pdf.bullet("Squarespace: Add via Settings, then Advanced, then Code Injection, then Footer")
    pdf.bullet("React or Next.js: Add the script in your document or app file, or use a useEffect hook")
    pdf.bullet("Custom HTML: Simply paste the script tag before the closing body tag in your HTML files")
    pdf.bullet("Any other platform: If you can add custom JavaScript, CohrenzAI will work")

    pdf.section_title("What Happens After Integration?")
    pdf.body("After you add the CohrenzAI script to your website:")
    pdf.bullet("A floating chat button appears in the bottom-right corner of your website")
    pdf.bullet("When a visitor clicks the button, a chat panel opens with a clean, professional interface")
    pdf.bullet("Visitors can type questions and get instant AI-powered answers based on your business data")
    pdf.bullet("The chatbot detects when visitors show buying interest such as asking about pricing or demos")
    pdf.bullet("When buying interest is detected, the chatbot naturally transitions to collecting the visitor contact info")
    pdf.bullet("Collected leads are automatically exported to your Google Sheets or CRM in real time")
    pdf.bullet("You get intent analysis reports showing exactly what each visitor was interested in")

    pdf.section_title("How Long Does Setup Take?")
    pdf.body("The entire process from sign-up to live chatbot typically takes 1 to 3 days:")
    pdf.bullet("Day 1: You sign up and share your business data such as documents, PDFs, and website URLs")
    pdf.bullet("Day 1-2: We process and train your custom AI chatbot on your data")
    pdf.bullet("Day 2-3: You add the one-line script to your website and go live")
    pdf.body("Most clients have their chatbot live and capturing leads within 48 hours of signing up. ShopEase India completed integration in under a single day.")

    pdf.add_page()
    pdf.section_title("Customization Options")
    pdf.sub_title("Chatbot Appearance")
    pdf.bullet("Primary color theme to match your brand colors")
    pdf.bullet("Custom chat header text and branding")
    pdf.bullet("Position on the page (bottom-right by default)")
    pdf.bullet("Chat panel dimensions and responsive behavior")
    pdf.sub_title("Chatbot Behavior")
    pdf.bullet("Welcome message shown when a visitor opens the chat")
    pdf.bullet("Lead capture trigger sensitivity")
    pdf.bullet("Which lead fields to collect such as name, email, phone, or a subset")
    pdf.bullet("Custom response tone and personality aligned with your brand voice")
    pdf.sub_title("Data Export")
    pdf.bullet("Google Sheets (real-time automatic export)")
    pdf.bullet("Email notifications for new leads")
    pdf.bullet("CRM systems (Salesforce, HubSpot, Zoho - on Premium plan)")
    pdf.bullet("Custom webhook endpoints for integration with your existing tools")

    pdf.section_title("Security During Integration")
    pdf.bullet("Your API key and public key are unique to your account")
    pdf.bullet("All communication uses HTTPS encryption")
    pdf.bullet("Visitor data is isolated per session and per client")
    pdf.bullet("No cookies are set, only localStorage for session continuity")
    pdf.bullet("The script does not access any other data on your website or visitors browsers")
    pdf.bullet("You can remove the chatbot at any time by removing the script tag")

    pdf.section_title("Need Help With Integration?")
    pdf.body("Our team is here to help. Contact us at:")
    pdf.bullet("Email: info@cohrenzai.com")
    pdf.bullet("Phone: +91 8273597975 / +91 8770278713")
    pdf.bullet("We offer free integration support for all plans including the Free tier")

    path = os.path.join(OUTPUT_DIR, "RAG_01_Integration_Guide.pdf")
    pdf.output(path)
    print(f"Created: {path}")


# ============================================================
# PDF 2: Complete Product FAQ
# ============================================================
def create_product_faq():
    pdf = CohrenzPDF()
    pdf.alias_nb_pages()
    pdf.cover_page("Frequently Asked\nQuestions", "Comprehensive Answers to Every Question About CohrenzAI")

    pdf.add_page()
    pdf.section_title("General Questions")

    pdf.sub_title("What is CohrenzAI?")
    pdf.body("CohrenzAI is an AI-powered chatbot platform that helps businesses convert website visitors into qualified leads. We deploy intelligent, intent-driven chatbots on your website that understand visitor queries, provide accurate answers from your business data, capture lead information, and analyze visitor intent - all automatically, 24 hours a day, 7 days a week.")

    pdf.sub_title("How is CohrenzAI different from other chatbots?")
    pdf.body("Unlike generic chatbots that give pre-scripted or template-based answers, CohrenzAI chatbots are trained specifically on YOUR business data. Our chatbots use advanced AI with Retrieval-Augmented Generation and vector embeddings to understand context and provide accurate, natural responses. Additionally, our chatbots actively detect buying intent, capture leads intelligently, and provide detailed intent analytics about each visitor.")

    pdf.sub_title("Who founded CohrenzAI?")
    pdf.body("CohrenzAI was co-founded by Saket Ahlawat (CEO), Keith Swamy (CEO), Vagesh Khatri (COO), and Vidit Sarin (CPO). The company is headquartered in Noida, Uttar Pradesh, India.")

    pdf.sub_title("Where is CohrenzAI located?")
    pdf.body("CohrenzAI is based in Noida, Uttar Pradesh, India. We serve clients globally.")

    pdf.sub_title("How do I contact CohrenzAI?")
    pdf.bullet("Email: info@cohrenzai.com")
    pdf.bullet("Phone: +91 8273597975 or +91 8770278713")
    pdf.bullet("Location: Noida, Uttar Pradesh, India")

    pdf.sub_title("Is CohrenzAI suitable for small businesses?")
    pdf.body("Absolutely. We offer a Free plan that lets small businesses test the platform with up to 5 users for 2 months at no cost. Our one-script integration means you do not need a technical team to get started.")

    pdf.add_page()
    pdf.section_title("Product and Features")

    pdf.sub_title("What features does CohrenzAI provide?")
    pdf.bullet("Seamless Customer Journey: 24/7 automated support, instant query resolution, intelligent FAQ handling")
    pdf.bullet("Lead Generation and Conversion: Identify qualified leads, book demos, schedule appointments automatically")
    pdf.bullet("AI-Ready Knowledge Systems: Transform PDFs and documents into structured knowledge for context-aware responses")
    pdf.bullet("Trained on Your Business Data: Every chatbot trained on YOUR data for accurate, on-brand responses")
    pdf.bullet("Simple and Secure Integration: One-script website integration with end-to-end data security")
    pdf.bullet("Internal AI Support: Deploy internal chatbots for employee support and productivity")

    pdf.sub_title("How does the chatbot answer visitor questions?")
    pdf.body("The chatbot uses Retrieval-Augmented Generation (RAG). When a visitor asks a question, the system searches your knowledge base to find the most relevant information, then uses AI to generate a natural response based on that information. Answers are always grounded in your actual business data.")

    pdf.sub_title("Can the chatbot handle multiple visitors simultaneously?")
    pdf.body("Yes. CohrenzAI handles thousands of concurrent conversations. Each visitor gets their own isolated session. The system is built on FastAPI with async processing for high concurrency.")

    pdf.sub_title("Does the chatbot work 24 hours a day?")
    pdf.body("Yes. Once deployed, the chatbot runs 24/7 with no business hour restrictions. Visitors can get instant answers at any time, even at midnight. This is especially valuable for capturing leads from visitors in different time zones.")

    pdf.sub_title("What kind of questions can the chatbot answer?")
    pdf.bullet("Product or service information and descriptions")
    pdf.bullet("Pricing details and plan comparisons")
    pdf.bullet("Business hours, location, and contact information")
    pdf.bullet("Frequently Asked Questions about your company")
    pdf.bullet("Technical specifications and feature details")
    pdf.bullet("Policy information such as returns, refunds, shipping")
    pdf.body("If a visitor asks something not covered in your data, the chatbot will honestly say it does not have that information and suggest contacting your team directly.")

    pdf.add_page()
    pdf.section_title("Lead Generation")

    pdf.sub_title("How does CohrenzAI capture leads?")
    pdf.body("CohrenzAI uses a three-trigger system:")
    pdf.bullet("Opportunistic Trigger: If a visitor shares their email or phone during conversation, the system captures it")
    pdf.bullet("Intent Trigger: When a visitor asks about pricing, demos, or services, the chatbot recognizes buying intent and collects contact information")
    pdf.bullet("Engagement Trigger: After 4 or more messages showing sustained interest, the chatbot proactively asks for contact details")
    pdf.body("The lead capture flow is natural, not pushy. The chatbot asks for name first, then email, then phone - one at a time.")

    pdf.sub_title("What information does the chatbot collect from leads?")
    pdf.bullet("Full name")
    pdf.bullet("Email address (validated)")
    pdf.bullet("Phone number (validated, supports Indian phone numbers)")
    pdf.bullet("Intent summary: AI-generated analysis of visitor interest and needs")
    pdf.bullet("Session ID and timestamp")

    pdf.sub_title("Where do captured leads go?")
    pdf.body("Leads are automatically exported to Google Sheets in real time with name, email, phone, intent summary, session ID, and timestamp. CRM integration (Salesforce, HubSpot, Zoho) is available on Premium plan.")

    pdf.sub_title("What is Intent Analysis?")
    pdf.body("Intent Analysis examines the full conversation to produce a structured report including: user interest level (exploratory, evaluative, transactional), specific products of interest, actual requirements, unmet needs, matched offerings, and behavioral signals like comparison shopping or trust-building.")

    pdf.add_page()
    pdf.section_title("Pricing and Plans")

    pdf.sub_title("How much does CohrenzAI cost?")
    pdf.bullet("Free Plan: $0/month - Up to 5 users, 2-month access, 1 month support, basic features")
    pdf.bullet("Standard Plan: $300/month - Up to 500 users, lifetime access, 4 months support, advanced lead capture, Google Sheets integration. Most popular.")
    pdf.bullet("Premium Plan: $700/month - Up to 5000+ users, lifetime access, dedicated support, full analytics, CRM integration, multi-site deployment, dedicated account manager, 99.9% SLA")

    pdf.sub_title("Is there a free trial?")
    pdf.body("Yes. The Free plan gives full access to core features for 2 months with up to 5 users. No credit card required.")

    pdf.sub_title("Can I upgrade or downgrade?")
    pdf.body("Yes, at any time. Upgrades take effect immediately. Downgrades take effect at the next billing cycle. No penalty for switching.")

    pdf.sub_title("Is there a long-term contract?")
    pdf.body("No. All plans are month-to-month. Cancel anytime. No long-term commitment required.")

    pdf.sub_title("What payment methods do you accept?")
    pdf.body("Major credit/debit cards, bank transfers, and UPI for Indian clients.")

    pdf.sub_title("Do you offer refunds?")
    pdf.body("We offer refunds on a case-by-case basis within the first 14 days of a paid subscription. Contact info@cohrenzai.com.")

    pdf.section_title("Security and Privacy")

    pdf.sub_title("Is my data secure?")
    pdf.body("Yes. We implement HTTPS encryption, encrypted databases, API key authentication, parameterized SQL queries, and session isolation. We never sell your data.")

    pdf.sub_title("Does CohrenzAI use cookies?")
    pdf.body("No. The chatbot uses localStorage for session IDs only. No tracking cookies.")

    pdf.sub_title("Is CohrenzAI compliant with data protection laws?")
    pdf.body("Yes. We comply with India's DPDPA 2023 and align with GDPR, ISO 27001, and OWASP guidelines.")

    pdf.sub_title("What happens to my data if I cancel?")
    pdf.body("Data is retained for 30 days for export, then permanently deleted.")

    path = os.path.join(OUTPUT_DIR, "RAG_02_Product_FAQ.pdf")
    pdf.output(path)
    print(f"Created: {path}")


# ============================================================
# PDF 3: Use Cases & Industry Applications
# ============================================================
def create_use_cases():
    pdf = CohrenzPDF()
    pdf.alias_nb_pages()
    pdf.cover_page("Use Cases &\nIndustry Applications", "How Businesses Across Industries Use CohrenzAI")

    pdf.add_page()
    pdf.section_title("Healthcare")
    pdf.sub_title("Challenge")
    pdf.body("Healthcare clinics and hospitals receive thousands of repetitive patient inquiries daily about appointment availability, doctor schedules, treatment details, insurance coverage, and prescription refills. Front-desk staff spend most of their time answering phone calls instead of providing in-person patient care.")
    pdf.sub_title("CohrenzAI Solution")
    pdf.body("Deploy a CohrenzAI chatbot trained on your clinic's services, doctor profiles, appointment policies, treatment information, and FAQs. The chatbot handles patient inquiries 24/7, schedules appointments automatically, and captures patient contact details for follow-up.")
    pdf.sub_title("Results")
    pdf.body("Dr. Ananya Mehta, Director of MedFirst Clinics, reports: CohrenzAI's chatbot handles over 70% of our patient inquiries automatically. Appointment bookings went up and our front-desk team can finally focus on in-person care instead of answering repetitive calls.")
    pdf.sub_title("Key Benefits for Healthcare")
    pdf.bullet("Automate appointment scheduling and booking confirmations")
    pdf.bullet("Handle patient FAQ inquiries about treatments, medications, and procedures")
    pdf.bullet("Provide after-hours support for urgent information needs")
    pdf.bullet("Capture patient contact information for follow-up appointments")
    pdf.bullet("Reduce front-desk workload by 70% or more")
    pdf.bullet("Provide treatment and medication information instantly")

    pdf.add_page()
    pdf.section_title("E-Commerce and Retail")
    pdf.sub_title("Challenge")
    pdf.body("E-commerce websites receive high volumes of visitor traffic but convert only 2-3% into actual customers. Visitors leave without purchasing because they cannot find product information quickly, have unanswered questions about sizing, shipping, or returns, or simply need guidance choosing the right product.")
    pdf.sub_title("CohrenzAI Solution")
    pdf.body("Deploy a chatbot trained on your complete product catalog, pricing, shipping policies, return policies, and customer FAQs. The chatbot acts as a virtual sales associate, guiding shoppers through product selection, answering questions instantly, and capturing contact information from high-intent visitors.")
    pdf.sub_title("Results")
    pdf.body("Rahul Kapoor, CEO of ShopEase India, reports: We integrated CohrenzAI in under a day and saw a 40% jump in qualified leads within the first month. The chatbot understands our product catalog and guides shoppers like a real sales associate. Best investment we have made.")
    pdf.sub_title("Key Benefits for E-Commerce")
    pdf.bullet("Guide shoppers through product selection with personalized recommendations")
    pdf.bullet("Answer sizing, availability, and pricing questions instantly")
    pdf.bullet("Handle shipping, return, and exchange policy inquiries")
    pdf.bullet("Capture contact information from high-intent shoppers")
    pdf.bullet("Increase qualified leads by up to 40% within the first month")
    pdf.bullet("Provide 24/7 shopping assistance for global customers")

    pdf.add_page()
    pdf.section_title("Real Estate")
    pdf.sub_title("Challenge")
    pdf.body("Real estate companies lose potential buyers and renters because inquiries come in at all hours, including evenings and weekends when agents are unavailable. Visitors want instant answers about property details, pricing, availability, and viewing schedules.")
    pdf.sub_title("CohrenzAI Solution")
    pdf.body("Train a chatbot on your property listings, pricing, floor plans, amenities, location details, and booking policies. The chatbot provides instant property information, schedules viewings, and captures lead information from interested buyers and renters.")
    pdf.sub_title("Results")
    pdf.body("Priya Sharma, Marketing Head at UrbanNest Realty, reports: Our website visitors now get instant answers about properties, pricing, and availability even at midnight. CohrenzAI helped us capture leads we were previously losing and the data security gave us complete peace of mind.")
    pdf.sub_title("Key Benefits for Real Estate")
    pdf.bullet("Provide instant property information including pricing, floor plans, and amenities")
    pdf.bullet("Schedule property viewings and site visits automatically")
    pdf.bullet("Qualify buyer and renter leads based on budget and preferences")
    pdf.bullet("Capture leads 24/7 including after business hours and weekends")
    pdf.bullet("Answer location, connectivity, and neighborhood questions")
    pdf.bullet("Handle multiple property inquiries simultaneously")

    pdf.add_page()
    pdf.section_title("SaaS and Technology Companies")
    pdf.sub_title("Challenge")
    pdf.body("SaaS companies need to handle a high volume of pre-sales inquiries about features, pricing, integrations, and technical capabilities. Product demos need to be scheduled efficiently, and free trial users need onboarding support. Sales teams spend too much time on repetitive questions instead of closing deals.")
    pdf.sub_title("CohrenzAI Solution")
    pdf.body("Deploy a chatbot trained on your product documentation, feature comparisons, pricing tiers, API documentation, and integration guides. The chatbot handles pre-sales questions, schedules demo calls, supports trial users during onboarding, and captures lead information from high-intent visitors.")
    pdf.sub_title("Key Benefits for SaaS")
    pdf.bullet("Answer feature comparison and pricing questions instantly")
    pdf.bullet("Automate demo scheduling and meeting bookings")
    pdf.bullet("Support free trial users during onboarding")
    pdf.bullet("Provide technical documentation and API information")
    pdf.bullet("Capture leads with detailed intent analysis for sales prioritization")
    pdf.bullet("Reduce time-to-first-response from hours to seconds")

    pdf.section_title("Financial Services")
    pdf.sub_title("Challenge")
    pdf.body("Financial institutions handle high volumes of inquiries about loan products, credit cards, investment options, account services, and regulatory requirements. Customers expect instant, accurate responses and seamless application processes.")
    pdf.sub_title("CohrenzAI Solution")
    pdf.body("Train a chatbot on your product offerings, eligibility criteria, interest rates, application processes, and FAQs. The chatbot provides accurate financial information, guides users through application steps, and captures qualified lead information.")
    pdf.sub_title("Key Benefits")
    pdf.bullet("Handle loan and credit card eligibility inquiries")
    pdf.bullet("Provide investment product information and comparisons")
    pdf.bullet("Guide users through application processes")
    pdf.bullet("Capture high-quality leads with detailed intent summaries")
    pdf.bullet("Ensure compliance-aware communication")

    pdf.add_page()
    pdf.section_title("Education and EdTech")
    pdf.sub_title("Challenge")
    pdf.body("Educational institutions receive overwhelming inquiry volumes during admission seasons. Prospective students and parents need instant answers about courses, fees, eligibility, campus facilities, and application deadlines.")
    pdf.sub_title("CohrenzAI Solution")
    pdf.body("Deploy a chatbot trained on your course catalog, admission requirements, fee structures, scholarship information, campus details, and academic policies. Handle admission season peaks without adding temporary staff.")
    pdf.sub_title("Key Benefits")
    pdf.bullet("Handle admissions inquiries about courses, fees, and eligibility")
    pdf.bullet("Provide scholarship and financial aid information")
    pdf.bullet("Guide prospective students through application processes")
    pdf.bullet("Answer campus facility and student life questions")
    pdf.bullet("Capture prospective student contact information for follow-up")
    pdf.bullet("Scale effortlessly during peak admission seasons")

    pdf.section_title("Professional Services")
    pdf.sub_title("Use Cases")
    pdf.body("Law firms, consulting agencies, accounting firms, and other professional services can use CohrenzAI to:")
    pdf.bullet("Handle initial consultation requests and appointment scheduling")
    pdf.bullet("Answer common questions about services, pricing, and processes")
    pdf.bullet("Capture qualified lead information from prospective clients")
    pdf.bullet("Provide information about areas of expertise and case studies")
    pdf.bullet("Manage client intake forms and preliminary questionnaires")
    pdf.bullet("Offer 24/7 availability for time-sensitive inquiries")

    path = os.path.join(OUTPUT_DIR, "RAG_03_Use_Cases.pdf")
    pdf.output(path)
    print(f"Created: {path}")


# ============================================================
# PDF 4: Onboarding, Support & Troubleshooting
# ============================================================
def create_support_guide():
    pdf = CohrenzPDF()
    pdf.alias_nb_pages()
    pdf.cover_page("Onboarding, Support &\nTroubleshooting", "Your Complete Guide to Getting the Most from CohrenzAI")

    pdf.add_page()
    pdf.section_title("Getting Started Checklist")
    pdf.body("Here is a step-by-step checklist to get your CohrenzAI chatbot up and running:")
    pdf.bullet("Step 1: Sign up for a CohrenzAI account at our website or contact info@cohrenzai.com")
    pdf.bullet("Step 2: Choose your plan (Free, Standard at $300/month, or Premium at $700/month)")
    pdf.bullet("Step 3: Gather your business documents - PDFs, FAQs, product catalogs, pricing pages, service descriptions")
    pdf.bullet("Step 4: Submit your documents to our team via email or dashboard upload")
    pdf.bullet("Step 5: Wait 24-48 hours for our team to train your custom AI chatbot on your data")
    pdf.bullet("Step 6: Receive your unique API URL and Public Key from our team")
    pdf.bullet("Step 7: Add the one-line script tag to your website before the closing body tag")
    pdf.bullet("Step 8: Test the chatbot by visiting your website and asking questions")
    pdf.bullet("Step 9: Configure Google Sheets or CRM integration for lead export")
    pdf.bullet("Step 10: Go live and start capturing leads")

    pdf.section_title("What Documents Should I Provide?")
    pdf.body("The more relevant data you provide, the better your chatbot will perform. Here are examples of useful documents:")
    pdf.bullet("Product or service description pages")
    pdf.bullet("Pricing and plans information")
    pdf.bullet("Frequently Asked Questions (FAQs)")
    pdf.bullet("Return, refund, and shipping policies")
    pdf.bullet("About us and company overview content")
    pdf.bullet("Team and leadership information")
    pdf.bullet("Case studies and testimonials")
    pdf.bullet("Technical documentation or specifications")
    pdf.bullet("Contact information and office hours")
    pdf.bullet("Blog posts or articles relevant to customer queries")
    pdf.body("You can provide these as PDF files, Word documents, or simply share your website URLs and we will scrape the content for you.")

    pdf.section_title("How to Update Your Knowledge Base")
    pdf.body("As your business evolves, you may need to update the chatbot's knowledge base with new information. Here is how:")
    pdf.bullet("Send updated or new documents to info@cohrenzai.com")
    pdf.bullet("Our team will process the updates within 24 hours")
    pdf.bullet("The chatbot will automatically start using the updated knowledge base")
    pdf.bullet("No changes needed on your website - your script tag stays the same")
    pdf.body("On Standard and Premium plans, you can request unlimited knowledge base updates. On the Free plan, you get one initial setup and one update during your 2-month access period.")

    pdf.add_page()
    pdf.section_title("Setting Up Google Sheets Lead Export")
    pdf.body("CohrenzAI can automatically export captured leads to a Google Sheet in real time. Here is how to set it up:")
    pdf.bullet("Step 1: Create a Google Sheet in your Google Drive")
    pdf.bullet("Step 2: Share the sheet with the service account email we provide during onboarding")
    pdf.bullet("Step 3: Share the sheet URL with our team")
    pdf.bullet("Step 4: We configure the automatic export on our end")
    pdf.body("Once configured, every time a lead is captured by your chatbot, a new row is automatically added to your Google Sheet with the following columns: session ID, name, email, phone, intent summary, and timestamp.")

    pdf.section_title("Managing Your Account")
    pdf.sub_title("How to upgrade your plan")
    pdf.body("Contact our team at info@cohrenzai.com to upgrade your plan. Upgrades take effect immediately and you pay the prorated difference for the current billing period.")
    pdf.sub_title("How to downgrade your plan")
    pdf.body("Contact our team to request a downgrade. Downgrades take effect at the start of the next billing cycle.")
    pdf.sub_title("How to cancel your account")
    pdf.body("Send an email to info@cohrenzai.com requesting cancellation. Your data is retained for 30 days for export, then permanently deleted. Remove the script tag from your website to remove the chatbot.")

    pdf.section_title("Common Troubleshooting")
    pdf.sub_title("The chatbot is not appearing on my website")
    pdf.body("Check the following:")
    pdf.bullet("Verify the script tag is placed before the closing body tag in your HTML")
    pdf.bullet("Make sure the data-api-url and data-public-key attributes are correctly set")
    pdf.bullet("Clear your browser cache and reload the page")
    pdf.bullet("Check your browser console for any JavaScript errors")
    pdf.bullet("Ensure your website does not have a Content Security Policy that blocks external scripts")
    pdf.bullet("If using WordPress, try disabling caching plugins temporarily")

    pdf.sub_title("The chatbot is giving wrong or irrelevant answers")
    pdf.body("This usually means the knowledge base needs updating:")
    pdf.bullet("Make sure you have provided comprehensive documents covering the topic being asked about")
    pdf.bullet("Check if the information in your documents is current and accurate")
    pdf.bullet("Send additional documents or FAQs to our team to expand the knowledge base")
    pdf.bullet("If the chatbot is answering from outdated information, send us the updated documents")

    pdf.sub_title("Leads are not appearing in Google Sheets")
    pdf.bullet("Verify the Google Sheet sharing permissions are correctly set")
    pdf.bullet("Check that the service account email has Editor access to the sheet")
    pdf.bullet("Ensure the sheet has not been moved or deleted")
    pdf.bullet("Contact our support team if the issue persists")

    pdf.add_page()
    pdf.sub_title("The chatbot response is slow")
    pdf.bullet("Response times depend on AI model processing and network latency")
    pdf.bullet("Typical response time is 2-5 seconds")
    pdf.bullet("If consistently slow, contact our team to investigate")
    pdf.bullet("Large knowledge bases may require optimization")

    pdf.sub_title("I want to change the chatbot appearance or colors")
    pdf.body("Contact our team with your brand colors and preferences. We can customize the chat button color, panel design, header text, and overall look to match your brand identity.")

    pdf.section_title("Getting Support")
    pdf.body("CohrenzAI offers multiple support channels:")
    pdf.sub_title("Email Support")
    pdf.body("Email us at info@cohrenzai.com. We respond within 24 hours on business days. Priority support for Standard and Premium plans.")
    pdf.sub_title("Phone Support")
    pdf.body("Call us at +91 8273597975 or +91 8770278713 during business hours (IST 10 AM - 6 PM, Monday to Friday).")
    pdf.sub_title("Support Coverage by Plan")
    pdf.bullet("Free Plan: 1 month of email support included")
    pdf.bullet("Standard Plan: 4 months of priority email support. Additional support at $50/month.")
    pdf.bullet("Premium Plan: 4 months of dedicated support with a dedicated account manager. Additional support at $50/month.")

    pdf.section_title("Best Practices for Maximum Results")
    pdf.bullet("Provide comprehensive and up-to-date business documents for training")
    pdf.bullet("Include your complete FAQ list - the more questions covered, the better the chatbot performs")
    pdf.bullet("Update the knowledge base whenever you launch new products, change pricing, or update policies")
    pdf.bullet("Review captured leads regularly and follow up within 24 hours for best conversion rates")
    pdf.bullet("Use intent analysis reports to identify gaps in your offerings or website content")
    pdf.bullet("Monitor chatbot conversations periodically to identify areas for improvement")
    pdf.bullet("Share customer testimonials and case studies to help the chatbot build credibility during conversations")

    path = os.path.join(OUTPUT_DIR, "RAG_04_Support_Troubleshooting.pdf")
    pdf.output(path)
    print(f"Created: {path}")


# ============================================================
# PDF 5: API Reference & Developer Guide
# ============================================================
def create_developer_guide():
    pdf = CohrenzPDF()
    pdf.alias_nb_pages()
    pdf.cover_page("API Reference &\nDeveloper Guide", "Technical Guide for Developers Integrating CohrenzAI")

    pdf.add_page()
    pdf.section_title("Overview")
    pdf.body("CohrenzAI provides a REST API that powers all chatbot interactions. While most users integrate CohrenzAI using our one-script widget, developers who want deeper integration can use our API directly. This guide covers all available endpoints, authentication, request/response formats, and advanced customization options.")

    pdf.section_title("Authentication")
    pdf.body("All API requests require authentication using two credentials:")
    pdf.bullet("API URL: Your unique API endpoint provided during onboarding")
    pdf.bullet("Public Key: Your unique public key included in the X-Public-Key header")
    pdf.body("Both credentials are provided when you sign up for a CohrenzAI account. Keep your credentials secure and never expose them in client-side code that is publicly accessible. For the chatbot widget, the public key is embedded in the script tag data attributes.")

    pdf.section_title("Base URL")
    pdf.body("Your API base URL is provided during onboarding. All endpoints are relative to this base URL. Example: https://api.cohrenzai.com/v1")

    pdf.section_title("API Endpoints")

    pdf.sub_title("POST /chat - Send a Chat Message")
    pdf.body("Send a visitor message to the chatbot and receive an AI-powered response.")
    pdf.body("Request Headers:")
    pdf.bullet("Content-Type: application/json")
    pdf.bullet("X-Public-Key: your_public_key")
    pdf.body("Request Body (JSON):")
    pdf.bullet("message (string, required): The visitor's message text")
    pdf.bullet("session_id (string, required): Unique session identifier for conversation tracking")
    pdf.body("Response Body (JSON):")
    pdf.bullet("answer (string): The AI-generated response from the chatbot")
    pdf.body("Status Codes:")
    pdf.bullet("200: Successful response")
    pdf.bullet("400: Bad request (empty message)")
    pdf.bullet("500: Server error")
    pdf.body("Example: Send a POST request to /chat with the body containing message set to 'What are your pricing plans?' and session_id set to 'session_12345'. The response will contain an answer field with the chatbot's response about pricing plans based on your knowledge base.")

    pdf.add_page()
    pdf.sub_title("GET /chats/{session_id} - Retrieve Chat History")
    pdf.body("Retrieve the conversation history for a specific session.")
    pdf.body("Path Parameters:")
    pdf.bullet("session_id (string, required): The session ID to retrieve chats for")
    pdf.body("Query Parameters:")
    pdf.bullet("k (integer, optional, default: 10): Number of recent messages to retrieve")
    pdf.body("Response Body (JSON):")
    pdf.bullet("chats (array): List of chat objects, each containing 'message' (string) and 'sender' (string, either 'user' or 'ai')")
    pdf.body("Status Codes:")
    pdf.bullet("200: Successful response with chat history")
    pdf.bullet("500: Server error")

    pdf.sub_title("GET /predict_intent/{session_id} - Get Intent Analysis")
    pdf.body("Get an AI-generated intent analysis for a specific conversation session. This endpoint analyzes all user messages in the session and produces a structured report about the visitor's interests, requirements, and behavioral signals.")
    pdf.body("Path Parameters:")
    pdf.bullet("session_id (string, required): The session ID to analyze")
    pdf.body("Response Body (JSON):")
    pdf.bullet("intent_summary (string): Structured intent analysis report covering user interest, segments of interest, actual requirements, unmet needs, matched offerings, and behavioral signals")
    pdf.body("Status Codes:")
    pdf.bullet("200: Successful response with intent analysis")
    pdf.bullet("500: Server error")

    pdf.section_title("Session Management")
    pdf.body("Sessions are the foundation of conversation tracking in CohrenzAI. Here is how they work:")
    pdf.bullet("Each conversation is identified by a unique session_id")
    pdf.bullet("The chatbot widget generates session IDs automatically in the format: session_{timestamp}_{random_string}")
    pdf.bullet("Session IDs are stored in the browser's localStorage for continuity across page navigations")
    pdf.bullet("If you are building a custom integration, you can generate your own session IDs using any unique string format")
    pdf.bullet("To start a new conversation, generate a new session_id")
    pdf.bullet("All messages sent with the same session_id are treated as part of the same conversation")
    pdf.bullet("Conversation history is used for context in AI responses (last 20 messages)")

    pdf.add_page()
    pdf.section_title("Lead Capture Flow")
    pdf.body("Understanding the lead capture flow is important for developers building custom integrations. The flow works as follows:")
    pdf.sub_title("Lead Detection Triggers")
    pdf.body("The system detects lead opportunities through three triggers:")
    pdf.bullet("1. Opportunistic: Visitor shares email or phone number during conversation")
    pdf.bullet("2. Intent Signal: Visitor mentions keywords like pricing, demo, trial, contact, consultation, services, or partnership")
    pdf.bullet("3. Engagement: After 4 or more user messages in a session")

    pdf.sub_title("Lead Capture State Machine")
    pdf.body("Once triggered, the chatbot follows a state machine to collect information:")
    pdf.bullet("NONE: Normal conversation mode, no lead capture active")
    pdf.bullet("ASKED_NAME: Chatbot has asked for the visitor's name. Waiting for name input.")
    pdf.bullet("ASKED_EMAIL: Chatbot has asked for email. Validates email format before accepting.")
    pdf.bullet("ASKED_PHONE: Chatbot has asked for phone. Validates phone format before accepting.")
    pdf.bullet("COMPLETED: All information collected. Lead is exported to Google Sheets.")
    pdf.body("The system is smart about data collection. If a visitor provides their email or phone early in the conversation before the lead flow starts, the system remembers it and skips asking for that information later. This prevents redundant questions and creates a smoother experience.")

    pdf.sub_title("Input Validation")
    pdf.body("The system validates all lead inputs:")
    pdf.bullet("Names: Detected from natural phrases like 'My name is Rahul' or 'I am Priya' or just the name by itself")
    pdf.bullet("Emails: Validated using standard email format patterns")
    pdf.bullet("Phone Numbers: Validated for Indian phone number format (10 digits with optional country code)")
    pdf.bullet("Casual messages like 'hi', 'ok', 'thanks' are recognized and not mistaken for data input")

    pdf.section_title("Building a Custom Chat Widget")
    pdf.body("If you want to build your own chat interface instead of using our default widget, here is what you need:")
    pdf.bullet("Generate unique session IDs for each conversation")
    pdf.bullet("Send POST requests to /chat with the message and session_id")
    pdf.bullet("Display the 'answer' field from the response to the user")
    pdf.bullet("Handle the conversation UI, typing indicators, and message history in your frontend")
    pdf.bullet("Optionally use GET /chats/{session_id} to restore conversation history if the user returns")
    pdf.bullet("Optionally use GET /predict_intent/{session_id} for analytics")
    pdf.body("The API handles all AI processing, lead capture, and intent analysis on the server side, so your custom widget only needs to handle the user interface.")

    pdf.add_page()
    pdf.section_title("Webhook Integration (Premium)")
    pdf.body("Premium plan users can configure webhooks to receive real-time notifications when events occur:")
    pdf.bullet("New Lead Captured: Triggered when a visitor completes the lead capture flow with name, email, and phone")
    pdf.bullet("High-Intent Conversation: Triggered when intent analysis detects a high-value prospect")
    pdf.bullet("Custom Events: Configure triggers based on specific keywords or conversation patterns")
    pdf.body("Webhooks send HTTP POST requests to your specified endpoint with JSON payloads containing event details.")

    pdf.section_title("Rate Limiting")
    pdf.body("To ensure platform stability and fair usage, API requests are subject to rate limits:")
    pdf.bullet("Free Plan: 100 requests per hour")
    pdf.bullet("Standard Plan: 1,000 requests per hour")
    pdf.bullet("Premium Plan: 10,000 requests per hour (custom limits available)")
    pdf.body("If you exceed the rate limit, the API will return a 429 status code. Implement exponential backoff in your integration to handle rate limiting gracefully.")

    pdf.section_title("Error Handling")
    pdf.body("The API returns standard HTTP status codes:")
    pdf.bullet("200: Success - Request processed successfully")
    pdf.bullet("400: Bad Request - Invalid or missing parameters (e.g., empty message)")
    pdf.bullet("401: Unauthorized - Invalid or missing authentication credentials")
    pdf.bullet("429: Too Many Requests - Rate limit exceeded")
    pdf.bullet("500: Internal Server Error - An unexpected error occurred on our side")
    pdf.body("Error responses include a 'detail' field with a human-readable error message. For production integrations, always handle error responses gracefully and provide fallback behavior for your users.")

    pdf.section_title("Best Practices for Developers")
    pdf.bullet("Always generate unique session IDs to prevent conversation mixing")
    pdf.bullet("Implement error handling and retry logic for API calls")
    pdf.bullet("Use HTTPS for all API communications")
    pdf.bullet("Do not expose your API credentials in publicly accessible code")
    pdf.bullet("Implement a typing indicator in your UI while waiting for API responses")
    pdf.bullet("Cache conversation history client-side to reduce API calls")
    pdf.bullet("Use the intent analysis endpoint to build custom analytics dashboards")

    pdf.section_title("Technical Support for Developers")
    pdf.body("Need help with your integration? Our technical team is available to assist:")
    pdf.bullet("Email: info@cohrenzai.com")
    pdf.bullet("Phone: +91 8273597975 / +91 8770278713")
    pdf.bullet("Include your account ID and session IDs when reporting issues for faster resolution")

    path = os.path.join(OUTPUT_DIR, "RAG_05_Developer_Guide.pdf")
    pdf.output(path)
    print(f"Created: {path}")


if __name__ == "__main__":
    create_integration_guide()
    create_product_faq()
    create_use_cases()
    create_support_guide()
    create_developer_guide()
    print("\nAll 5 RAG PDFs generated!")
