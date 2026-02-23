#!/usr/bin/env python3
"""Generate 5 RAG knowledge-base PDFs for CohrenzAI chatbot training."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_pdfs import CohrenzPDF, OUTPUT_DIR


# ============================================================
# PDF 1: Getting Started & Integration Guide
# ============================================================
def create_integration_guide():
    pdf = CohrenzPDF("Integration Guide")
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
    pdf.body("Integration is incredibly simple. You add a single script tag to your website HTML. That's it. No server configuration, no backend changes, no complex setup. The script creates a beautiful floating chat button on your website that visitors can click to start a conversation.")
    pdf.body("The script tag looks like this:")
    pdf.body('<script data-api-url="YOUR_API_URL" data-public-key="YOUR_PUBLIC_KEY" src="https://cdn.cohrenzai.com/widget.js"></script>')
    pdf.body("You just replace YOUR_API_URL with the API endpoint we provide and YOUR_PUBLIC_KEY with your unique public key. Paste it before the closing </body> tag of your website.")
    pdf.sub_title("Step 4: Go Live and Start Capturing Leads")
    pdf.body("Once the script is added, your chatbot is live. It will immediately start engaging visitors, answering questions from your knowledge base, and capturing leads when visitors show buying intent.")

    pdf.add_page()
    pdf.section_title("Integration Requirements")
    pdf.body("CohrenzAI works with any website technology. Here is what you need:")
    pdf.bullet("A website where you can add HTML/JavaScript code (WordPress, Shopify, Wix, Squarespace, custom HTML, React, Next.js, or any other platform)")
    pdf.bullet("The ability to add a script tag to your website pages")
    pdf.bullet("A CohrenzAI account with your API URL and Public Key")
    pdf.body("That's all. No server-side changes. No database setup. No npm packages. No dependencies. Just one script tag.")

    pdf.section_title("Platform Compatibility")
    pdf.body("CohrenzAI works with every major website platform:")
    pdf.bullet("WordPress: Add the script via header/footer plugin or directly in your theme's footer.php")
    pdf.bullet("Shopify: Add the script in Online Store > Themes > Edit Code > theme.liquid before </body>")
    pdf.bullet("Wix: Use the Wix HTML embed widget or Custom Code section in site settings")
    pdf.bullet("Squarespace: Add via Settings > Advanced > Code Injection > Footer")
    pdf.bullet("React/Next.js: Add the script in your _document.js or _app.js file, or use a useEffect hook")
    pdf.bullet("Custom HTML: Simply paste the script tag before </body> in your HTML files")
    pdf.bullet("Any other platform: If you can add custom JavaScript, CohrenzAI will work")

    pdf.section_title("What Happens After Integration?")
    pdf.body("After you add the CohrenzAI script to your website:")
    pdf.bullet("A floating chat button (blue circle with chat icon) appears in the bottom-right corner of your website")
    pdf.bullet("When a visitor clicks the button, a chat panel opens with a clean, professional interface")
    pdf.bullet("Visitors can type questions and get instant AI-powered answers based on your business data")
    pdf.bullet("The chatbot intelligently detects when visitors show buying interest (asking about pricing, demos, services)")
    pdf.bullet("When buying interest is detected, the chatbot naturally transitions to collecting the visitor's name, email, and phone number")
    pdf.bullet("Collected leads are automatically exported to your Google Sheets or CRM in real time")
    pdf.bullet("You get intent analysis reports showing exactly what each visitor was interested in")

    pdf.section_title("How Long Does Setup Take?")
    pdf.body("The entire process from sign-up to live chatbot typically takes 1 to 3 days:")
    pdf.bullet("Day 1: You sign up and share your business data (documents, PDFs, website URLs)")
    pdf.bullet("Day 1-2: We process and train your custom AI chatbot on your data")
    pdf.bullet("Day 2-3: You add the one-line script to your website and go live")
    pdf.body("Most clients have their chatbot live and capturing leads within 48 hours of signing up. ShopEase India completed integration in under a single day.")

    pdf.add_page()
    pdf.section_title("Customization Options")
    pdf.sub_title("Chatbot Appearance")
    pdf.body("The chatbot widget can be customized to match your brand:")
    pdf.bullet("Primary color theme to match your brand colors")
    pdf.bullet("Custom chat header text and branding")
    pdf.bullet("Position on the page (bottom-right by default)")
    pdf.bullet("Chat panel dimensions and responsive behavior")
    pdf.sub_title("Chatbot Behavior")
    pdf.body("You can customize how the chatbot behaves:")
    pdf.bullet("Welcome message shown when a visitor opens the chat")
    pdf.bullet("Lead capture trigger sensitivity (how quickly it asks for contact info)")
    pdf.bullet("Which lead fields to collect (name, email, phone - or a subset)")
    pdf.bullet("Custom response tone and personality aligned with your brand voice")
    pdf.sub_title("Data Export")
    pdf.body("Lead data can be exported to:")
    pdf.bullet("Google Sheets (real-time automatic export)")
    pdf.bullet("Email notifications (get notified when a new lead is captured)")
    pdf.bullet("CRM systems (Salesforce, HubSpot, Zoho - on Premium plan)")
    pdf.bullet("Custom webhook endpoints for integration with your existing tools")

    pdf.section_title("Security During Integration")
    pdf.body("CohrenzAI takes security seriously during and after integration:")
    pdf.bullet("Your API key and public key are unique to your account and cannot be used by others")
    pdf.bullet("All communication between the chatbot widget and our servers uses HTTPS encryption")
    pdf.bullet("Visitor conversation data is isolated per session and per client")
    pdf.bullet("No cookies are set - only localStorage is used for session continuity")
    pdf.bullet("The script does not access any other data on your website or your visitors' browsers")
    pdf.bullet("You can remove the chatbot at any time by simply removing the script tag")

    pdf.section_title("Need Help With Integration?")
    pdf.body("Our team is here to help you get set up. If you have any questions about integration or need assistance, reach out to us:")
    pdf.bullet("Email: info@cohrenzai.com")
    pdf.bullet("Phone: +91 8273597975 / +91 8770278713")
    pdf.bullet("We offer free integration support for all plans, including the Free tier")

    path = os.path.join(OUTPUT_DIR, "RAG_01_Integration_Guide.pdf")
    pdf.output(path)
    print(f"Created: {path}")


# ============================================================
# PDF 2: Complete Product FAQ
# ============================================================
def create_product_faq():
    pdf = CohrenzPDF("Product FAQ")
    pdf.alias_nb_pages()
    pdf.cover_page("Frequently Asked Questions", "Comprehensive Answers to Every Question About CohrenzAI")

    pdf.add_page()
    pdf.section_title("General Questions")

    pdf.sub_title("What is CohrenzAI?")
    pdf.body("CohrenzAI is an AI-powered chatbot platform that helps businesses convert website visitors into qualified leads. We deploy intelligent, intent-driven chatbots on your website that understand visitor queries, provide accurate answers from your business data, capture lead information, and analyze visitor intent - all automatically, 24 hours a day, 7 days a week.")

    pdf.sub_title("How is CohrenzAI different from other chatbots?")
    pdf.body("Unlike generic chatbots that give pre-scripted or template-based answers, CohrenzAI chatbots are trained specifically on YOUR business data. Our chatbots use advanced AI (Retrieval-Augmented Generation with vector embeddings) to understand context and provide accurate, natural responses. Additionally, our chatbots don't just answer questions - they actively detect buying intent, capture leads intelligently, and provide you with detailed intent analytics about each visitor.")

    pdf.sub_title("Who founded CohrenzAI?")
    pdf.body("CohrenzAI was co-founded by Saket Ahlawat (CEO), Keith Swamy (CEO), Vagesh Khatri (COO), and Vidit Sarin (CPO). The company is headquartered in Noida, Uttar Pradesh, India.")

    pdf.sub_title("Where is CohrenzAI located?")
    pdf.body("CohrenzAI is based in Noida, Uttar Pradesh, India. We serve clients globally and our platform works for businesses anywhere in the world.")

    pdf.sub_title("How do I contact CohrenzAI?")
    pdf.body("You can reach us through multiple channels:")
    pdf.bullet("Email: info@cohrenzai.com")
    pdf.bullet("Phone: +91 8273597975")
    pdf.bullet("Phone: +91 8770278713")
    pdf.bullet("Website: https://cohrenzai.com")
    pdf.bullet("Location: Noida, Uttar Pradesh, India")

    pdf.sub_title("Is CohrenzAI suitable for small businesses?")
    pdf.body("Absolutely. CohrenzAI is designed for businesses of all sizes. We offer a Free plan that lets small businesses test the platform with up to 5 users for 2 months at no cost. Our one-script integration means you don't need a technical team to get started.")

    pdf.sub_title("Does CohrenzAI work for businesses outside India?")
    pdf.body("Yes. CohrenzAI works for businesses globally. While we are headquartered in India, our platform can be deployed on any website worldwide. The chatbot can handle queries in English, and we are working on multi-language support.")

    pdf.add_page()
    pdf.section_title("Product & Features")

    pdf.sub_title("What features does CohrenzAI provide?")
    pdf.body("CohrenzAI provides six core features:")
    pdf.bullet("Seamless Customer Journey: 24/7 automated support, instant query resolution, and intelligent FAQ handling")
    pdf.bullet("Lead Generation and Conversion: Identify qualified leads, book demos, schedule appointments, and manage follow-ups automatically")
    pdf.bullet("AI-Ready Knowledge Systems: Transform your PDFs and documents into structured knowledge for accurate, context-aware responses")
    pdf.bullet("Trained on Your Business Data: Every chatbot is trained on YOUR data for accurate, relevant, on-brand responses")
    pdf.bullet("Simple and Secure Integration: One-script website integration with end-to-end data security")
    pdf.bullet("Internal AI Support: Deploy internal chatbots for employee support and productivity")

    pdf.sub_title("How does the chatbot answer visitor questions?")
    pdf.body("The chatbot uses a technology called Retrieval-Augmented Generation (RAG). When a visitor asks a question, the system searches your knowledge base (built from your documents and website content) to find the most relevant information, then uses AI to generate a natural, conversational response based on that information. This ensures answers are always grounded in your actual business data, not made up.")

    pdf.sub_title("Can the chatbot handle multiple visitors at the same time?")
    pdf.body("Yes. CohrenzAI can handle thousands of concurrent conversations simultaneously. Each visitor gets their own isolated session, so conversations never overlap or interfere with each other. The system is built on FastAPI with async processing for high concurrency.")

    pdf.sub_title("Does the chatbot work 24/7?")
    pdf.body("Yes. Once deployed, the chatbot runs 24 hours a day, 7 days a week. There are no business hour restrictions. Visitors can get instant answers and submit their contact information at any time - even at midnight. This is especially valuable for capturing leads from visitors in different time zones.")

    pdf.sub_title("What kind of questions can the chatbot answer?")
    pdf.body("The chatbot can answer any question that is covered by the data you provide. Common examples include:")
    pdf.bullet("Product or service information and descriptions")
    pdf.bullet("Pricing details and plan comparisons")
    pdf.bullet("Business hours, location, and contact information")
    pdf.bullet("Frequently Asked Questions about your company")
    pdf.bullet("Technical specifications and feature details")
    pdf.bullet("Policy information (returns, refunds, shipping, etc.)")
    pdf.bullet("Eligibility requirements and application processes")
    pdf.body("If a visitor asks something not covered in your data, the chatbot will politely say it doesn't have that information and suggest they contact your team directly.")

    pdf.sub_title("What happens if the chatbot cannot answer a question?")
    pdf.body("If the chatbot does not have relevant information in the knowledge base to answer a question, it will honestly tell the visitor that it doesn't have the answer and suggest contacting the team directly via email or phone. The chatbot never makes up information or hallucinate answers outside of your provided data.")

    pdf.add_page()
    pdf.section_title("Lead Generation")

    pdf.sub_title("How does CohrenzAI capture leads?")
    pdf.body("CohrenzAI uses a sophisticated three-trigger system to capture leads at the right moment:")
    pdf.bullet("Opportunistic Trigger: If a visitor voluntarily shares their email or phone number during conversation, the system captures it immediately")
    pdf.bullet("Intent Trigger: When a visitor asks about pricing, demos, consultations, or services, the chatbot recognizes buying intent and naturally transitions to collecting contact information")
    pdf.bullet("Engagement Trigger: After 4 or more messages (showing sustained interest), the chatbot proactively but politely asks for contact details")
    pdf.body("The lead capture flow is designed to feel natural, not pushy. The chatbot asks for name first, then email, then phone number - one at a time, in a conversational way.")

    pdf.sub_title("What information does the chatbot collect from leads?")
    pdf.body("The chatbot collects the following information from each lead:")
    pdf.bullet("Full name")
    pdf.bullet("Email address (validated for correct format)")
    pdf.bullet("Phone number (validated for correct format, supports Indian phone numbers with country code)")
    pdf.bullet("Intent summary: An AI-generated analysis of what the visitor was interested in and what they need")
    pdf.bullet("Session ID and timestamp for tracking")

    pdf.sub_title("Where do captured leads go?")
    pdf.body("Captured leads are automatically exported to Google Sheets in real time. Each lead entry includes the visitor's name, email, phone number, intent summary, session ID, and timestamp. You can also configure leads to be sent to CRM systems like Salesforce, HubSpot, or Zoho on the Premium plan. Email notifications for new leads are also available.")

    pdf.sub_title("What is Intent Analysis?")
    pdf.body("Intent Analysis is CohrenzAI's proprietary AI feature that examines the full conversation between a visitor and your chatbot to produce a structured report. The report includes:")
    pdf.bullet("User Interest: Whether the visitor is interested in your offerings, and the level of interest (exploratory, evaluative, transactional, partnership)")
    pdf.bullet("Segment/Product of Interest: Which specific products or services the visitor asked about")
    pdf.bullet("Actual Requirement: What the visitor is ultimately trying to achieve")
    pdf.bullet("Unmet Needs: What the visitor wants that your company may not currently offer")
    pdf.bullet("Matched Offerings: Which of your existing offerings align with the visitor's needs")
    pdf.bullet("Behavioral Signals: Trust-building behavior, comparison shopping, research phase indicators")
    pdf.body("This information helps your sales and marketing teams prioritize leads and tailor their outreach for maximum conversion.")

    pdf.sub_title("Can I disable lead collection?")
    pdf.body("Yes. Lead collection can be configured based on your preferences. You can adjust the sensitivity of triggers, choose which fields to collect, or disable lead capture entirely if you only want the chatbot for customer support.")

    pdf.add_page()
    pdf.section_title("Integration & Technical")

    pdf.sub_title("How do I integrate CohrenzAI into my website?")
    pdf.body("Integration takes just one step: add a single script tag to your website. The script tag includes your unique API URL and public key. Once added, the chatbot widget automatically appears on your website. No server-side changes, no databases, no backend work needed on your end.")

    pdf.sub_title("Does it work with WordPress?")
    pdf.body("Yes. CohrenzAI works perfectly with WordPress. You can add the script tag using a simple header/footer plugin like 'Insert Headers and Footers', or by editing your theme's footer.php file directly. Many WordPress users are up and running within minutes.")

    pdf.sub_title("Does it work with Shopify?")
    pdf.body("Yes. For Shopify, go to Online Store > Themes > Edit Code, find the theme.liquid file, and paste the CohrenzAI script tag just before the closing </body> tag. That's it.")

    pdf.sub_title("Does it work with React or Next.js?")
    pdf.body("Yes. For React applications, you can load the script dynamically using a useEffect hook in your root component. For Next.js, add it in _document.js or use the next/script component. We provide detailed code examples for both frameworks.")

    pdf.sub_title("Does it work with Wix or Squarespace?")
    pdf.body("Yes. For Wix, use the Custom Code section in your site settings or add an HTML embed widget. For Squarespace, go to Settings > Advanced > Code Injection and paste the script in the Footer section.")

    pdf.sub_title("Can I use CohrenzAI on multiple websites?")
    pdf.body("On Free and Standard plans, CohrenzAI is licensed for use on one website/project. On the Premium plan, you can deploy the chatbot on multiple websites with separate or shared knowledge bases. Multi-site deployment is also available as an add-on for Standard plans.")

    pdf.sub_title("What technology does CohrenzAI use?")
    pdf.body("CohrenzAI is built on a modern technology stack: FastAPI (Python) for the backend API, FAISS (Facebook AI Similarity Search) for vector similarity search, Azure OpenAI for natural language processing and response generation, LangChain for AI pipeline orchestration, and MySQL for data storage. The chatbot widget is pure JavaScript with zero dependencies.")

    pdf.sub_title("Is there an API I can use?")
    pdf.body("Yes. CohrenzAI provides a REST API with the following endpoints:")
    pdf.bullet("POST /chat: Send a message and receive an AI response. Requires message and session_id in the request body.")
    pdf.bullet("GET /chats/{session_id}: Retrieve conversation history for a specific session.")
    pdf.bullet("GET /predict_intent/{session_id}: Get the AI-generated intent analysis for a specific conversation.")
    pdf.body("All API calls require authentication via API key. Detailed API documentation is available upon signup.")

    pdf.add_page()
    pdf.section_title("Pricing & Plans")

    pdf.sub_title("How much does CohrenzAI cost?")
    pdf.body("CohrenzAI offers three plans:")
    pdf.bullet("Free Plan: $0/month - Up to 5 users, 2-month access, 1 month support, basic features. Perfect for trying out the platform.")
    pdf.bullet("Standard Plan: $300/month - Up to 500 users, lifetime access, 4 months support included, advanced lead capture with intent analysis, Google Sheets integration. Most popular plan.")
    pdf.bullet("Premium Plan: $700/month - Up to 5000+ users, lifetime access, 4 months dedicated support, full analytics, CRM integration, multi-site deployment, dedicated account manager, custom AI model tuning, 99.9% SLA.")

    pdf.sub_title("Is there a free trial?")
    pdf.body("Yes. The Free plan gives you full access to core chatbot features for 2 months with up to 5 users. No credit card required. This allows you to evaluate the platform completely risk-free before committing to a paid plan.")

    pdf.sub_title("Can I upgrade or downgrade my plan?")
    pdf.body("Yes. You can upgrade or downgrade at any time. Upgrades take effect immediately and you pay the prorated difference. Downgrades take effect at the start of the next billing cycle. There is no penalty for switching plans.")

    pdf.sub_title("Is there a long-term contract?")
    pdf.body("No. All CohrenzAI plans are month-to-month with no long-term contract required. You can cancel at any time. We believe in earning your business every month through the value we deliver.")

    pdf.sub_title("What payment methods do you accept?")
    pdf.body("We accept major credit cards, debit cards, bank transfers, and UPI payments for Indian clients. All payments are processed securely through trusted payment processors. We do not store your credit card details.")

    pdf.sub_title("What does the support include?")
    pdf.body("Support includes help with integration, troubleshooting, chatbot customization, data upload, knowledge base updates, and performance optimization. The Free plan includes 1 month of support. Standard and Premium plans include 4 months, with additional support available at $50/month.")

    pdf.sub_title("Do you offer refunds?")
    pdf.body("We offer refunds on a case-by-case basis within the first 14 days of a paid subscription if you are not satisfied with the service. Please contact our team at info@cohrenzai.com to discuss.")

    pdf.add_page()
    pdf.section_title("Security & Privacy")

    pdf.sub_title("Is my data secure with CohrenzAI?")
    pdf.body("Yes. Security is a core priority at CohrenzAI. We implement end-to-end encryption for all data in transit using HTTPS/TLS 1.2+. Your business data and visitor conversations are stored in encrypted databases. API keys authenticate all requests. We use parameterized SQL queries to prevent injection attacks. Session data is isolated per conversation and per client.")

    pdf.sub_title("Does CohrenzAI sell my data?")
    pdf.body("Absolutely not. CohrenzAI never sells, rents, or trades your data or your visitors' data to any third party. Your business data is used exclusively to train YOUR chatbot and provide YOUR services. Period.")

    pdf.sub_title("Who can see my visitors' conversations?")
    pdf.body("Only you (the business owner) can access your visitors' conversations through your CohrenzAI dashboard or API. Conversations are isolated per session and per client. CohrenzAI staff may access data only for troubleshooting purposes with your explicit consent.")

    pdf.sub_title("Does the chatbot use cookies?")
    pdf.body("No. The CohrenzAI chatbot widget does not use cookies. It uses the browser's localStorage to store a session ID for conversation continuity. This session ID is a random, anonymized identifier that does not contain any personal information.")

    pdf.sub_title("Is CohrenzAI compliant with data protection laws?")
    pdf.body("Yes. CohrenzAI complies with India's Digital Personal Data Protection Act (DPDPA) 2023 and aligns with international standards including GDPR principles, ISO 27001 practices, and OWASP security guidelines. We provide data access, correction, and deletion rights to all users.")

    pdf.sub_title("What happens to my data if I cancel?")
    pdf.body("When you cancel your account, your data is retained for 30 days to give you time to export anything you need. After 30 days, all your data - including documents, conversation logs, leads, and embeddings - is permanently deleted from our systems.")

    path = os.path.join(OUTPUT_DIR, "RAG_02_Product_FAQ.pdf")
    pdf.output(path)
    print(f"Created: {path}")


if __name__ == "__main__":
    create_integration_guide()
    create_product_faq()
    print("Done RAG batch 1!")
